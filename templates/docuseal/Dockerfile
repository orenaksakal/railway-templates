FROM docuseal/docuseal:3.2.4@sha256:a8f063f916e39fe326af62111f875200c171ea1f5c6902f3b39f634b9549a3ef
ENV BUNDLE_GEMFILE=/app/Gemfile
COPY templates/docuseal/bootstrap.rb /opt/railway/bootstrap.rb
COPY --chmod=755 templates/docuseal/start.sh /opt/railway/start.sh
ENTRYPOINT ["/opt/railway/start.sh"]
