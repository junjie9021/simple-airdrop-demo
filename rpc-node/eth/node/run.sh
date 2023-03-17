#!/bin/bash

# 如果需要升级版本，修改这里的版本号后，执行一下run.sh脚本即可。
VERSION=1.10.23

docker build --build-arg VERSION=$VERSION -t eth:$VERSION .
docker stop eth
docker rm eth
docker run --init -d --restart=always --name eth -p 8545:8545 -p 8551:8551 -v /data/eth:/eth eth:$VERSION