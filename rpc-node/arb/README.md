# BTC 节点Docker部署

> 配置要求 4C 16G 500G

注意：节点最好跟eth节点同一台，arb是eth的L2

## 启动
**启动命令**
```bash
./run.sh
```

**获取高度**
```bash
# 本地
curl -X POST --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' -H "Content-Type: application/json" http://localhost:8547
# 公共
curl -X POST --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' -H "Content-Type: application/json" https://arb1.arbitrum.io/rpc
```
## 其他文档
- [部署文档](https://developer.offchainlabs.com/node-running/running-a-node)
- [区块链浏览器](https://arbiscan.io/)
