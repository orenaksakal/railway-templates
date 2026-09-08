import http from 'node:http';
import { timingSafeEqual } from 'node:crypto';

export function createGateway({ apiKey, upstream }) {
  if (!apiKey || apiKey.length < 32) throw new Error('API_KEY must contain at least 32 characters');
  const target = new URL(upstream);
  if (target.protocol !== 'http:' || target.username || target.password) throw new Error('UPSTREAM_URL must be a private HTTP origin');
  const expected = Buffer.from(`Bearer ${apiKey}`);
  return http.createServer((req, res) => {
    // Health is only a reachability probe; no upstream response bodies are exposed.
    if (req.method === 'GET' && req.url === '/healthz') {
      const probe = http.get(new URL('/', target), { timeout: 3000 }, response => {
        response.resume();
        res.writeHead(response.statusCode < 500 ? 200 : 503);
        res.end(response.statusCode < 500 ? 'ready' : 'unavailable');
      });
      probe.once('timeout', () => probe.destroy());
      probe.once('error', () => { if (!res.headersSent) res.writeHead(503); res.end('unavailable'); });
      return;
    }
    const given = Buffer.from(req.headers.authorization || '');
    if (given.length !== expected.length || !timingSafeEqual(given, expected)) {
      res.writeHead(401, { 'content-type': 'application/json', 'www-authenticate': 'Bearer' });
      res.end(JSON.stringify({ success: false, error: 'Unauthorized' }));
      return;
    }
    // Restrict forwarding to the API surface. Upstream admin/debug routes stay private.
    let path;
    try { path = decodeURIComponent((req.url || '').split('?')[0]); } catch { path = ''; }
    if (!/^\/v[12]\//.test(path) || path.includes('\\') || path.split('/').some(part => part === '.' || part === '..') || path.includes('%')) {
      res.writeHead(404); res.end('Not found'); return;
    }
    const headers = { ...req.headers, host: target.host };
    delete headers.authorization;
    delete headers['proxy-authorization'];
    delete headers['x-forwarded-for'];
    const proxy = http.request({ hostname: target.hostname, port: target.port || 80,
      method: req.method, path: req.url, headers, timeout: 180_000 }, response => {
      res.writeHead(response.statusCode, response.headers);
      response.pipe(res);
    });
    proxy.on('timeout', () => proxy.destroy(new Error('upstream timeout')));
    proxy.on('error', () => {
      if (!res.headersSent) res.writeHead(502, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ success: false, error: 'Upstream unavailable' }));
    });
    req.on('aborted', () => proxy.destroy());
    res.on('close', () => { if (!res.writableFinished) proxy.destroy(); });
    req.pipe(proxy);
  });
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const server = createGateway({ apiKey: process.env.API_KEY, upstream: process.env.UPSTREAM_URL });
  server.listen(Number(process.env.PORT || 8080), '::');
  process.on('SIGTERM', () => {
    server.close(() => process.exit(0));
    setTimeout(() => process.exit(0), 10_000).unref();
  });
}
