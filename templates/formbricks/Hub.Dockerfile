FROM ghcr.io/formbricks/hub:0.8.7@sha256:027537bc6f3025aa3603a73fc741989fcf52105129e11959eec4e80ce65c037c
COPY --chmod=755 templates/formbricks/hub-start.sh /app/railway-start.sh
ENTRYPOINT ["/app/railway-start.sh"]
