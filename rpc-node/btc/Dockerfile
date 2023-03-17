FROM ubuntu:20.04

ARG VERSION=22.0

RUN apt-get update \
  && apt-get install -y net-tools curl \
  && curl -o /tmp/bitcoin.tar.gz https://bitcoincore.org/bin/bitcoin-core-${VERSION}/bitcoin-${VERSION}-x86_64-linux-gnu.tar.gz \
  && tar -zxvf /tmp/bitcoin.tar.gz -C /opt \
  && mv /opt/bitcoin-* /opt/bitcoin \
  && ln -s /opt/bitcoin/bin/* /usr/local/bin \
  && rm -f /tmp/bitcoin.tar.gz

WORKDIR /btc

EXPOSE 8332

ENTRYPOINT ["sh", "-c", "bitcoind -datadir=/btc -rpcbind=0.0.0.0 -rpcallowip=0.0.0.0/0 -txindex -rpcworkqueue=1000 -rpcuser=$RPC_USER -rpcpassword=$RPC_PWD"]
