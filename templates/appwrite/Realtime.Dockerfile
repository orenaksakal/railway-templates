FROM appwrite/appwrite:2.0.0@sha256:27ca3f70d06fb0f4751e93cba03c49f96562236986f9b688185ee1c0e1f7e9aa
USER root
RUN apk add --no-cache python3
COPY templates/appwrite/patch-redis-auth.py /opt/railway/patch-redis-auth.py
RUN python3 /opt/railway/patch-redis-auth.py && php -l /usr/src/code/app/init/registers.php
CMD ["realtime"]
