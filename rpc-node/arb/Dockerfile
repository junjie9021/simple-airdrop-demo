ARG VERSION=2.0.5-208d9d5

FROM offchainlabs/nitro-node:v${VERSION} as builder

FROM ubuntu:20.04

COPY --from=builder /usr/local/bin/nitro /usr/local/bin/nitro

RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y net-tools curl libsnappy-dev wget build-essential cmake gcc sqlite3 \
  && chmod +x /usr/local/bin/* \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /root/.arbitrum

ADD Entrypoint.sh /Entrypoint
RUN chmod +x /Entrypoint

EXPOSE 8547

ENTRYPOINT ["/Entrypoint"]