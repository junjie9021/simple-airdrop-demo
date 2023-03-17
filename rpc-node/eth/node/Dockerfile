FROM golang:1.16.7-buster as builder

ARG VERSION=1.10.23

RUN git clone https://github.com/ethereum/go-ethereum.git \
    && cd go-ethereum \
    && git checkout tags/v${VERSION} \
    && make geth

FROM ubuntu:20.04

COPY --from=builder /go/go-ethereum/build/bin/* /usr/local/bin/

RUN apt-get update \
  && apt-get install -y net-tools curl \
  && chmod +x /usr/local/bin/* \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /eth

EXPOSE 8545 8551

ENTRYPOINT ["sh", "-c", "geth --datadir /eth --authrpc.addr 0.0.0.0 --authrpc.jwtsecret /eth/jwt.hex --http --http.addr 0.0.0.0 --http.api web3,eth,net,personal,admin --cache 8192 --gpo.blocks 20 --gpo.percentile 95 --gpo.maxprice 1000000000000 --txpool.accountqueue 1000 --txpool.globalqueue 20000 --txpool.accountslots 160 --txpool.globalslots 20000 --txpool.lifetime 6h0m0s --txpool.pricebump 1 --allow-insecure-unlock --http.vhosts=*"]
