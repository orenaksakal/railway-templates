FROM chrislusf/seaweedfs:4.37@sha256:f898c91e42d7da5f4bb13f1efd424ff03ba85b420312eb929708a384e8a8b03d
COPY --chmod=755 templates/agenta/storage.sh /start.sh
ENTRYPOINT ["/start.sh"]
