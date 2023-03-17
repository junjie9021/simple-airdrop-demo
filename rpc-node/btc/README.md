# BTC 节点Docker部署

> 配置要求 4C 8G 1T 

**环境变量说明**
- `RPC_USER` RPC用户名
- `RPC_PWD` RPC密码

## 构建&部署
```
./run.sh
```

**获取高度**
```bash
# 本地
curl -X POST -u test:test -H 'content-type: text/plain;' -d '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockchaininfo", "params": [] }' http://localhost:8332/
```

## 其他文档
- [区块链浏览器](https://explorer.blackhatco.in/)
- [节点部署](https://forum.blackhatco.in/viewtopic.php?t=2)
