FROM bludit/docker:3.20.0@sha256:907e1ac53ecb6d4a43f71031532375f7d00ab3927df78353c71a4fdc3b317a6a
RUN mkdir -p /seed && for directory in bl-content bl-themes bl-plugins; do cp -a "/usr/share/nginx/html/$directory" "/seed/$directory"; rm -rf "/usr/share/nginx/html/$directory"; ln -s "/data/$directory" "/usr/share/nginx/html/$directory"; done
RUN sed -i "s/'DEBUG_MODE', TRUE/'DEBUG_MODE', FALSE/g" /usr/share/nginx/html/bl-kernel/boot/init.php

COPY shared/round9-bootstrap/seed.sh /seed.sh
COPY --chmod=755 templates/round9/bludit/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
