FROM ghcr.io/open-feature/flagd:v0.16.3@sha256:a11ae82ec6e40e89edae4327392a1e4ffc03e211f1b724879bb35b2e4f271bb3
COPY templates/flagd/flags.json /etc/flagd/flags.json
CMD ["start", "--port", "8013", "--uri", "file:/etc/flagd/flags.json"]
