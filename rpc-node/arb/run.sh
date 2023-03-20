#!/bin/bash

# 如果需要升级版本，修改这里的版本号后，执行一下run.sh脚本即可。
VERSION="2.0.11-8e786ec"
L1_URL="http://172.17.0.1:8545"

docker build --build-arg VERSION=$VERSION -t arb:$VERSION .
docker stop arb
docker rm arb
docker run --init -d --restart=always --name arb -p 8547:8547 -e L1_URL=$L1_URL -v /data/arb:/root/.arbitrum arb:$VERSION