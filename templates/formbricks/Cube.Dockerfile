FROM cubejs/cube:v1.6.6@sha256:746a381c5deb1f33500c84bed357ebe68aa08acc5030939f9e9efd35796d368c
COPY templates/formbricks/cube/cube.js /cube/conf/cube.js
COPY templates/formbricks/cube/FeedbackRecords.js /cube/conf/model/FeedbackRecords.js
