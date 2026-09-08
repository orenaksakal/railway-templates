FROM ghcr.io/toeverything/affine:0.27.4@sha256:b649f5ce2384ffdf13c23bccf81d759e15973d59d0b0058af65d895a84373099
COPY --chmod=755 templates/affine/start.sh /app/railway-start.sh
COPY shared/wait-for-dependencies.mjs /app/wait-for-dependencies.mjs
ENTRYPOINT ["/app/railway-start.sh"]
