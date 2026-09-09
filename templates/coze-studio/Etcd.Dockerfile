FROM bitnamilegacy/etcd:3.5@sha256:1b9977cf4cce7546873e0ee50e684c38a38a4e7a27d22086fbd2b8a1b44a69d0
USER root
COPY --chmod=755 templates/coze-studio/etcd-start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
