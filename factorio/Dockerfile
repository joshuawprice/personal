FROM debian:13-slim AS builder

WORKDIR /build

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y curl ca-certificates xz-utils \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LO https://factorio.com/get-download/stable/headless/linux64 \
    && xz -d < linux64 | tar -x


FROM debian:13-slim

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system nonroot \
    && mkdir /data \
    && chown nonroot: /data

COPY --from=builder --chown=nonroot:nonroot /build/factorio /opt/factorio
COPY entrypoint.sh /entrypoint.sh

VOLUME /data
EXPOSE 34197/udp

USER nonroot

ENTRYPOINT ["/entrypoint.sh"]
