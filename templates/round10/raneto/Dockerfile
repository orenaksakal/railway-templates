FROM raneto/raneto:0.18.1@sha256:75dc64b8c94f0ecba614a4ab08e449761ddbb1cda5613a2f57aaaf5d12caf50c
USER root
RUN mv /opt/raneto/config/config.js /opt/raneto/config/upstream-config.js
COPY templates/round10/raneto/config.js /opt/raneto/config/config.js
COPY templates/round10/raneto/start.mjs /usr/local/bin/railway-raneto.mjs
ENTRYPOINT ["node", "/usr/local/bin/railway-raneto.mjs"]
