#!/bin/bash

start_node(){
    nitro --l1.url $L1_URL --l2.chain-id=42161 --http.api=net,web3,eth,debug --http.corsdomain=* --http.addr=0.0.0.0 --http.vhosts=* $@
}

if [ ! -d /root/.arbitrum/nitro ];then
    start_node --init.url="https://snapshot.arbitrum.io/mainnet/nitro.tar"
else
    start_node
fi