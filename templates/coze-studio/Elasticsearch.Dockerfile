FROM bitnamilegacy/elasticsearch:8.18.0@sha256:4a7d14222c876a87c1ddd38e1128d8e42df80071b09ec54db5c32586c9cf5a38
USER root
ADD --chmod=644 https://raw.githubusercontent.com/coze-dev/coze-studio/fefb05ff27be1da939612fbf9faf5db62583b8ae/docker/volumes/elasticsearch/es_index_schema/coze_resource.index-template.json /operator/es_index_schema/coze_resource.index-template.json
ADD --chmod=644 https://raw.githubusercontent.com/coze-dev/coze-studio/fefb05ff27be1da939612fbf9faf5db62583b8ae/docker/volumes/elasticsearch/es_index_schema/project_draft.index-template.json /operator/es_index_schema/project_draft.index-template.json
ADD --chmod=644 https://raw.githubusercontent.com/coze-dev/coze-studio/fefb05ff27be1da939612fbf9faf5db62583b8ae/docker/volumes/elasticsearch/analysis-smartcn.zip /tmp/analysis-smartcn.zip
ADD --chmod=644 https://raw.githubusercontent.com/coze-dev/coze-studio/fefb05ff27be1da939612fbf9faf5db62583b8ae/docker/volumes/elasticsearch/setup_es.sh /operator/setup_es.sh
RUN /opt/bitnami/elasticsearch/bin/elasticsearch-plugin install --batch file:///tmp/analysis-smartcn.zip && rm /tmp/analysis-smartcn.zip
COPY templates/coze-studio/elasticsearch.yml /opt/bitnami/elasticsearch/config/elasticsearch.yml
COPY --chmod=755 templates/coze-studio/es-start.sh /start.sh
ENTRYPOINT ["/start.sh"]
