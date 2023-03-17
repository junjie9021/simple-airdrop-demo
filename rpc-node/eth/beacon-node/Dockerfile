FROM ubuntu:20.04

ARG VERSION=3.1.0

RUN apt-get update \
    && apt-get install -y net-tools wget  \
    && wget https://github.com/prysmaticlabs/prysm/releases/download/v${VERSION}/beacon-chain-v${VERSION}-linux-amd64 -P /usr/local/bin \
    && mv /usr/local/bin/beacon-chain-v${VERSION}-linux-amd64 /usr/local/bin/beacon-chain \
    && chmod +x /usr/local/bin/beacon-chain

WORKDIR /data

EXPOSE 8080 4000 3500

ENTRYPOINT ["sh", "-c", "beacon-chain --datadir=/data --rpc-host=0.0.0.0 --monitoring-host=0.0.0.0 --execution-endpoint=$ETH --jwt-secret=/data/jwt.hex --grpc-gateway-host=0.0.0.0"]