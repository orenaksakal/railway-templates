FROM thomaspoignant/go-feature-flag:v1.55.3@sha256:89a82b1f0f667f66db60e7ed3aa74d644b61d859a4fad8f8b81a846f29c32054
COPY templates/go-feature-flag/goff-proxy.yaml /goff/goff-proxy.yaml
COPY templates/go-feature-flag/flags.yaml /goff/flags.yaml
WORKDIR /goff
CMD ["/go-feature-flag", "--config", "/goff/goff-proxy.yaml"]
