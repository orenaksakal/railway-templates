FROM mysql:8.4.5@sha256:679e7e924f38a3cbb62a3d7df32924b83f7321a602d3f9f967c01b3df18495d6
ADD --chmod=644 https://raw.githubusercontent.com/coze-dev/coze-studio/fefb05ff27be1da939612fbf9faf5db62583b8ae/docker/volumes/mysql/schema.sql /docker-entrypoint-initdb.d/01-schema.sql
ADD --chmod=644 https://raw.githubusercontent.com/coze-dev/coze-studio/fefb05ff27be1da939612fbf9faf5db62583b8ae/docker/atlas/opencoze_latest_schema.hcl /operator/opencoze_latest_schema.hcl
