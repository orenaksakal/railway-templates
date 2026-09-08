FROM mongo:5.0.32@sha256:5e3e87afd24d75e722884d777c5713d254f7e88ba65381b5d6484f75a21b73e3
COPY --chmod=755 templates/fastgpt/mongo-start.sh /start.sh
ENTRYPOINT ["/start.sh"]
