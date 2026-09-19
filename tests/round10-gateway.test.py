"""Exercise the actual round-ten Nginx authentication configuration over loopback.

Run with NGINX_BIN=/absolute/path/to/nginx python3 tests/round10-gateway.test.py.
Requires nginx, htpasswd, and sha256sum; no image or application is deployed.
The production startup script creates the real password file and session token.
Only filesystem paths, listener ports, and the final image entrypoint are replaced.
"""
import base64
import http.client
import http.server
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
GATEWAY = ROOT / 'shared/round10-gateway'
PASSWORD = 'OwnerPassword0123456789'
ROTATED_PASSWORD = 'NewOwnerPassword9876543210'
NGINX = os.environ.get('NGINX_BIN') or shutil.which('nginx')


class Echo(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({'path': self.path, 'headers': dict(self.headers)}).encode()
        self.send_response(401 if self.path == '/upstream-401' else 200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def unused_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def basic(password=PASSWORD, username='admin'):
    return 'Basic ' + base64.b64encode(f'{username}:{password}'.encode()).decode()


class GatewayAuthentication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not NGINX or not Path(NGINX).is_file():
            raise RuntimeError('Set NGINX_BIN to a real Nginx executable; runtime tests cannot be skipped.')
        for command in ('htpasswd', 'sha256sum'):
            if not shutil.which(command):
                raise RuntimeError(f'Required production startup dependency is unavailable: {command}')
        cls.upstream = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Echo)
        cls.thread = threading.Thread(target=cls.upstream.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.upstream.shutdown()
        cls.upstream.server_close()
        cls.thread.join(timeout=3)

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix='round10-gateway-test-')
        self.directory = Path(self.scratch.name)
        self.process = None
        self.addCleanup(self.scratch.cleanup)
        self.addCleanup(self.stop_gateway)
        self.port = unused_port()
        self.start_gateway(PASSWORD)

    def production_startup(self, password, **overrides):
        # Replace only the filesystem destinations and image entrypoint. The real
        # validation, htpasswd call, and cookie derivation run without alteration.
        dump = self.directory / 'capture-entrypoint.py'
        dump.write_text('#!' + sys.executable + '\nimport json, os\nprint(json.dumps(dict(os.environ)))\n')
        dump.chmod(0o755)
        startup = (GATEWAY / 'start.sh').read_text()
        startup = startup.replace('/etc/nginx/htpasswd', str(self.directory / 'htpasswd'))
        startup = startup.replace('/docker-entrypoint.sh', str(dump))
        env = {
            **os.environ, 'UPSTREAM_HOST': '127.0.0.1',
            'UPSTREAM_PORT': str(self.upstream.server_address[1]),
            'OWNER_AUTH': 'true', 'OWNER_SCOPE': 'all', 'ACCESS_PASSWORD': password,
            **overrides,
        }
        return subprocess.run(['sh', '-c', startup], env=env, capture_output=True, text=True)

    def start_gateway(self, password):
        result = self.production_startup(password)
        self.assertEqual(result.returncode, 0, result.stderr)
        env = json.loads(result.stdout)
        self.token = env['ACCESS_COOKIE_TOKEN']
        self.assertRegex(self.token, r'^[a-f0-9]{64}$')
        template = (GATEWAY / 'default.conf.template').read_text()
        # Equivalent to envsubst's restricted substitution in the image. Nginx
        # request variables, such as $http_authorization, remain intact.
        template = re.sub(r'\$\{([A-Z_]+)\}', lambda match: env[match.group(1)], template)
        template = template.replace('listen 8080;', f'listen 127.0.0.1:{self.port};')
        template = template.replace('listen [::]:8080;', '')
        template = template.replace('/etc/nginx/htpasswd', str(self.directory / 'htpasswd'))
        template = template.replace('/etc/nginx/proxy.inc', str(GATEWAY / 'proxy.inc'))
        config = self.directory / 'nginx.conf'
        config.write_text(
            f'pid {self.directory}/nginx.pid;\n'
            f'error_log {self.directory}/error.log notice;\n'
            'worker_processes 1;\nevents { worker_connections 64; }\nhttp {\n'
            'access_log off;\n'
            f'client_body_temp_path {self.directory}/client-body;\n'
            f'proxy_temp_path {self.directory}/proxy;\n' + template + '\n}\n'
        )
        checked = subprocess.run([NGINX, '-t', '-p', str(self.directory) + '/', '-c', str(config)],
                                 capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.process = subprocess.Popen(
            [NGINX, '-p', str(self.directory) + '/', '-c', str(config), '-g', 'daemon off;'],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        )
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                self.fail('Nginx exited: ' + self.process.stderr.read().decode())
            try:
                status, _, _ = self.request('/healthz')
                if status == 200:
                    return
            except (ConnectionError, TimeoutError, OSError):
                pass
            time.sleep(0.025)
        self.fail('Nginx did not start within five seconds')

    def stop_gateway(self):
        if self.process is not None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=5)
            if self.process.stderr:
                self.process.stderr.close()
            self.process = None

    def request(self, path='/', headers=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.port, timeout=2)
        try:
            connection.request('GET', path, headers=headers or {})
            response = connection.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            connection.close()

    def login_cookie(self):
        status, headers, _ = self.request(headers={'Authorization': basic()})
        self.assertEqual(status, 200)
        return headers['Set-Cookie'].split(';', 1)[0]

    def test_unauthorized_and_incorrect_credentials_are_denied(self):
        for headers in ({}, {'Authorization': basic('wrong')},
                        {'Authorization': basic(username='wrong')},
                        {'Authorization': 'Bearer native-app-token'},
                        {'X-Template-Key': 'wrong'}):
            with self.subTest(headers=headers):
                status, response_headers, _ = self.request(headers=headers)
                self.assertEqual(status, 401)
                self.assertNotIn('Set-Cookie', response_headers)

    def test_healthz_never_mints_an_owner_cookie(self):
        for headers in ({}, {'Authorization': basic()}, {'X-Template-Key': PASSWORD},
                        {'Cookie': '__Host-template-owner=' + self.token}):
            with self.subTest(headers=headers):
                status, response_headers, body = self.request('/healthz', headers)
                self.assertEqual(status, 200)
                self.assertEqual(body, b'gateway ready')
                self.assertNotIn('Set-Cookie', response_headers)

    def test_basic_login_sets_cookie_and_consumes_owner_authorization(self):
        status, headers, body = self.request(headers={'Authorization': basic()})
        self.assertEqual(status, 200)
        cookie = headers['Set-Cookie']
        self.assertTrue(cookie.startswith('__Host-template-owner=' + self.token + ';'))
        for attribute in ('Path=/', 'Secure', 'HttpOnly', 'SameSite=Strict', 'Max-Age=43200'):
            self.assertIn(attribute, cookie.split('; '))
        self.assertNotIn('Domain=', cookie)
        self.assertNotIn('Authorization', json.loads(body)['headers'])

    def test_browser_session_preserves_native_bearer_authorization(self):
        cookie = self.login_cookie()
        status, _, body = self.request('/native-api', {
            'Cookie': cookie, 'Authorization': 'Bearer native-app-token',
        })
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['headers']['Authorization'], 'Bearer native-app-token')

    def test_cookie_boundaries_and_forged_values(self):
        valid = self.login_cookie()
        for cookie in ('__Host-template-owner=forged', valid + 'suffix',
                       'prefix' + valid, 'other=' + self.token, '__Host-template-owner='):
            with self.subTest(cookie=cookie):
                status, headers, _ = self.request(headers={'Cookie': cookie})
                self.assertEqual(status, 401)
                self.assertNotIn('Set-Cookie', headers)
        status, _, _ = self.request(headers={'Cookie': 'unrelated=x; ' + valid + '; another=y'})
        self.assertEqual(status, 200)

    def test_password_rotation_revokes_previous_cookie(self):
        old_cookie = self.login_cookie()
        old_token = self.token
        self.stop_gateway()
        self.start_gateway(ROTATED_PASSWORD)
        self.assertNotEqual(old_token, self.token)
        status, headers, _ = self.request(headers={'Cookie': old_cookie})
        self.assertEqual(status, 401)
        self.assertNotIn('Set-Cookie', headers)
        status, _, _ = self.request(headers={'Authorization': basic(ROTATED_PASSWORD)})
        self.assertEqual(status, 200)

    def test_api_key_preserves_native_bearer_and_is_removed_upstream(self):
        status, _, body = self.request('/native-api', {
            'X-Template-Key': PASSWORD, 'Authorization': 'Bearer native-app-token',
        })
        self.assertEqual(status, 200)
        headers = json.loads(body)['headers']
        self.assertEqual(headers['Authorization'], 'Bearer native-app-token')
        self.assertNotIn('X-Template-Key', headers)

    def test_upstream_auth_failure_does_not_mint_cookie(self):
        status, headers, _ = self.request('/upstream-401', {'Authorization': basic()})
        self.assertEqual(status, 401)
        self.assertNotIn('Set-Cookie', headers)

    def test_setup_scope_is_rejected_before_startup(self):
        result = self.production_startup(PASSWORD, OWNER_SCOPE='setup')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('OWNER_SCOPE=all', result.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
