FROM stoplight/prism:5.15.10@sha256:586d1f0f94f8d0eaf20b26b8b41f985f2a2d494bea297bd3988c3de3eb87094e
COPY templates/round10/prism/openapi.json /opt/template/openapi.json
COPY --chmod=755 templates/round10/prism/start.sh /opt/template/start.sh
ENTRYPOINT ["/opt/template/start.sh"]
