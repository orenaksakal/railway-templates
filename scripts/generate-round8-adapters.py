"""Generate small adapters for empty volumes and explicit starter configuration."""
import json
from catalog_round8 import ROOT

LOCK = json.loads((ROOT / 'images.round8.lock.json').read_text())
SOURCES = json.loads((ROOT / 'sources.round8.lock.json').read_text())


def write(slug, name, content):
    path = ROOT / 'templates' / slug / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + '\n')


def generate():
    source = SOURCES['grimoire']
    write('grimoire', 'Dockerfile', f'''
FROM {LOCK['oven/bun:1.4.2']} AS builder
WORKDIR /app
ADD --checksum=sha256:{source['archiveSha256']} {source['archiveUrl']} /tmp/source.tar.gz
RUN tar -xzf /tmp/source.tar.gz --strip-components=1 -C /app && rm /tmp/source.tar.gz
RUN bun install --frozen-lockfile && cd daemon && bun install --frozen-lockfile
RUN bun run build
FROM {LOCK['oven/bun:1.4.2-slim']}
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/daemon ./daemon
COPY --from=builder /app/package.json ./package.json
ENV HOST=0.0.0.0 PORT=3210 DATA_DIR=/data HOME=/data XDG_CONFIG_HOME=/data/config NODE_ENV=production LITTLEIMP_IN_CONTAINER=1
EXPOSE 3210
CMD ["bun", "run", "daemon:start"]
''')
    write('linkace', 'Dockerfile', f'''
FROM {LOCK['linkace/linkace:v2.6.1']}
USER root
RUN apk add --no-cache su-exec
COPY --chmod=755 templates/linkace/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
''')
    write('linkace', 'start.sh', '''#!/bin/sh
set -eu
mkdir -p /data
if [ ! -d /data/storage ]; then
  mkdir -p /data/storage
  cp -a /app/storage/. /data/storage/
  chown -R www-data:www-data /data/storage
fi
if [ ! -L /app/storage ]; then
  mv /app/storage /app/storage.image
  ln -s /data/storage /app/storage
fi
if [ ! -f /data/database.sqlite ]; then
  touch /data/database.sqlite
fi
chown www-data:www-data /data /data/database.sqlite
exec su-exec www-data /usr/bin/supervisord -c /etc/supervisor.d/supervisord.ini
''')
    write('fava', 'Dockerfile', f'''
FROM {LOCK['python:3.13-slim-bookworm']}
RUN pip install --no-cache-dir fava==1.30.16
COPY templates/fava/starter.beancount /opt/starter.beancount
COPY --chmod=755 templates/fava/start.sh /start.sh
ENV FAVA_HOST=0.0.0.0 FAVA_PORT=5000
EXPOSE 5000
ENTRYPOINT ["/start.sh"]
''')
    write('fava', 'start.sh', '''#!/bin/sh
set -eu
mkdir -p /data
if [ ! -e /data/main.beancount ]; then
  cp /opt/starter.beancount /data/main.beancount
fi
exec fava --host 0.0.0.0 --port 5000 /data/main.beancount
''')
    write('fava', 'starter.beancount', '''option "title" "My ledger"
option "operating_currency" "USD"
2026-01-01 open Assets:Checking USD
2026-01-01 open Equity:Opening-Balances USD
2026-01-01 * "Example opening balance"
  Assets:Checking             100.00 USD
  Equity:Opening-Balances     -100.00 USD
''')
    write('mockserver', 'Dockerfile', f'''
FROM {LOCK['busybox:1.37.0-uclibc']} AS bootstrap
FROM {LOCK['mockserver/mockserver:8.0.0']}
USER root
COPY --from=bootstrap /bin/busybox /bootstrap
COPY templates/mockserver/start.sh /start.sh
ENTRYPOINT ["/bootstrap", "sh", "/start.sh"]
''')
    write('mockserver', 'start.sh', '''#!/bin/sh
set -eu
/bootstrap mkdir -p /config
if [ ! -e /config/expectations.json ]; then
  printf '[]\\n' > /config/expectations.json
fi
exec /usr/lib/jvm/temurin25-trimmed/bin/java -Dfile.encoding=UTF-8 -XX:MaxRAMPercentage=75.0 -XX:SharedArchiveFile=/mockserver.jsa -cp '/mockserver-netty-jar-with-dependencies.jar:/libs/*' -Dmockserver.propertyFile=/config/mockserver.properties org.mockserver.cli.Main
''')
    write('sqlpage', 'Dockerfile', f'''
FROM {LOCK['lovasoa/sqlpage:v0.46.3']}
USER root
COPY templates/sqlpage/index.sql /opt/starter/index.sql
COPY --chmod=755 templates/sqlpage/start.sh /start.sh
ENTRYPOINT ["/start.sh"]
''')
    write('sqlpage', 'start.sh', '''#!/bin/sh
set -eu
mkdir -p /data/www /data/config
if [ ! -e /data/www/index.sql ]; then
  cp /opt/starter/index.sql /data/www/index.sql
fi
exec /usr/local/bin/sqlpage
''')
    write('sqlpage', 'index.sql', '''select 'shell' as component, 'My SQL application' as title;
select 'text' as component;
select 'Edit /data/www/index.sql to build your application. The SQLite database is stored at /data/app.db.' as contents;
select 'table' as component;
select sqlite_version() as sqlite_version, datetime('now') as server_utc;
''')
    write('maintainerr', 'Dockerfile', f'''
FROM {LOCK['ghcr.io/maintainerr/maintainerr:3.29.0']}
USER root
RUN apk add --no-cache su-exec
COPY --chmod=755 templates/maintainerr/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
''')
    write('maintainerr', 'start.sh', '''#!/bin/sh
set -eu
mkdir -p /opt/data/logs
chown node:node /opt/data /opt/data/logs
exec su-exec node /opt/app/start.sh
''')
    write('olivetin', 'Dockerfile', f'''
FROM {LOCK['jamesread/olivetin:3000.20.0']}
USER root
COPY templates/olivetin/config.yaml /opt/railway-config.yaml
COPY templates/olivetin/config.yaml /config/config.yaml
COPY --chmod=755 templates/olivetin/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
''')
    write('olivetin', 'start.sh', '''#!/bin/sh
set -eu
mkdir -p /config
if [ ! -e /config/config.yaml ]; then
  cp /opt/railway-config.yaml /config/config.yaml
fi
chown olivetin:olivetin /config /config/config.yaml
exec su -s /bin/sh olivetin -c 'exec /usr/bin/OliveTin'
''')
    write('olivetin', 'config.yaml', '''listenAddressSingleHTTPFrontend: 0.0.0.0:1337
logLevel: INFO
actions:
  - title: Show UTC time
    shell: date -u
    icon: clock
  - title: Show configuration volume usage
    shell: df -h /config
    icon: disk
''')
    write('go-feature-flag', 'Dockerfile', f'''
FROM {LOCK['thomaspoignant/go-feature-flag:v1.55.3']}
COPY templates/go-feature-flag/goff-proxy.yaml /goff/goff-proxy.yaml
COPY templates/go-feature-flag/flags.yaml /goff/flags.yaml
WORKDIR /goff
CMD ["/go-feature-flag", "--config", "/goff/goff-proxy.yaml"]
''')
    write('go-feature-flag', 'goff-proxy.yaml', '''server:
  mode: http
  port: 1031
pollingInterval: 60000
retriever:
  kind: file
  path: /goff/flags.yaml
startWithRetrieverError: false
loglevel: info
enableSwagger: false
''')
    write('go-feature-flag', 'flags.yaml', '''welcome-banner:
  variations:
    enabled: true
    disabled: false
  defaultRule:
    variation: enabled
''')
    write('flagd', 'Dockerfile', f'''
FROM {LOCK['ghcr.io/open-feature/flagd:v0.16.3']}
COPY templates/flagd/flags.json /etc/flagd/flags.json
CMD ["start", "--port", "8013", "--uri", "file:/etc/flagd/flags.json"]
''')
    write('flagd', 'flags.json', json.dumps({
        '$schema': 'https://flagd.dev/schema/v0/flags.json',
        'flags': {'welcome-banner': {'state': 'ENABLED', 'variants': {'on': True, 'off': False}, 'defaultVariant': 'on'}},
    }, indent=2))


if __name__ == '__main__':
    generate()
