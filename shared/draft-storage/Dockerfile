FROM minio/mc:RELEASE.2025-04-16T18-13-26Z@sha256:aead63c77f9db9107f1696fb08ecb0faeda23729cde94b0f663edf4fe09728e3 AS client
FROM minio/minio:RELEASE.2025-04-22T22-12-26Z@sha256:a1ea29fa28355559ef137d71fc570e508a214ec84ff8083e39bc5428980b015e
COPY --from=client /usr/bin/mc /usr/bin/mc
COPY --chmod=755 shared/draft-storage/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
