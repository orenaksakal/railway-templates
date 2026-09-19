FROM python:3.13-slim-bookworm@sha256:3e4eb6a8c8d89e10d322b1eac2b0aefefb13e7d818ddd2a0c3a3196aa01a57a2
RUN pip install --no-cache-dir fava==1.30.16
COPY templates/fava/starter.beancount /opt/starter.beancount
COPY --chmod=755 templates/fava/start.sh /start.sh
ENV FAVA_HOST=0.0.0.0 FAVA_PORT=5000
EXPOSE 5000
ENTRYPOINT ["/start.sh"]
