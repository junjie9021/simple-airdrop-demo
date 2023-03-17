#!/bin/bash

# 如果需要升级版本，修改这里的版本号后，执行一下run.sh脚本即可。
VERSION=3.1.0

docker build --build-arg VERSION=$VERSION -t eth_beacon_node:$VERSION .
docker stop eth_beacon_node
docker rm eth_beacon_node
docker run --init -d --restart=always --name eth_beacon_node -e ETH="http://172.17.0.1:8551" -p 3500:3500 -p 4000:4000 -p 8080:8080 -v /data/eth/beacon_node:/data eth_beacon_node:$VERSION