# ETH节点Docker部署

> 配置要求 至少8C 32G 2T

## 启动
0.配置 JWT 身份验证
```
# 把生成的密钥保存到执行层节点和共识层节点挂在目录
openssl rand -hex 32 | tr -d "\n" > "jwt.hex"
```

1.部署执行层节点
```bash
cd node
./run.sh
```

2.部署共识层节点
```
cd beacon-node
./run.sh
```

**获取高度**
```bash
# 本地
curl -X POST --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' -H "Content-Type: application/json" http://localhost:8545
```

## 其他文档
- [执行层部署文档](https://github.com/ethereum/go-ethereum)
- [共识层部署文档](https://docs.prylabs.network/docs/prepare-for-merge)
- [区块链浏览器](https://etherscan.io/)
