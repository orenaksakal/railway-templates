FROM mongo:8.0.17@sha256:9814652e33f0cf8b9fddea8b46dfc9d8e19b130dcfdd7b510ca58bb0d40c8b71
COPY --chmod=755 templates/appwrite/mongo-start.sh /railway-mongo-start.sh
ENTRYPOINT ["/railway-mongo-start.sh"]
