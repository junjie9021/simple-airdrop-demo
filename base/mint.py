"""
pip3 install web3
"""

import web3
import math
import requests

headers = {
    'content-type': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }

class Rpc:
    """
    eth rpc方法
    """
    def __init__(self, rpc='https://rpc.ankr.com/eth_goerli', chainid=5, proxies=None, timeout=30):
        self.rpc = rpc
        self.chainid = chainid
        self.proxies = proxies
        self.timeout = timeout

    def get_transaction(self, txhash):
        """获取的交易详情"""
        data = {"jsonrpc":"2.0","method":"eth_getTransactionByHash","params":[txhash],"id":1}
        res = requests.post(self.rpc, json=data, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def get_gas_price(self):
        """获取gas"""
        data = {"jsonrpc":"2.0","method":"eth_gasPrice","params":[],"id":1}
        res = requests.post(self.rpc, json=data, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def get_balance(self, address):
        """获取余额"""
        data = {"jsonrpc":"2.0","method":"eth_getBalance","params":[address, 'latest'],"id":1}
        res = requests.post(self.rpc, json=data, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def get_transaction_count_by_address(self, address):
        """获取地址nonce"""
        data = {"jsonrpc":"2.0","method":"eth_getTransactionCount","params":[address,'latest'],"id":1}
        res = requests.post(self.rpc, json=data, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def send_raw_transaction(self, hex):
        """广播交易"""
        data = {"jsonrpc":"2.0","method":"eth_sendRawTransaction","params":[hex],"id":1}
        res = requests.post(self.rpc, json=data, headers=headers,  proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def transfer(self, account, to, amount, gaslimit, **kw):
        """离线交易
        account
        to: 收款地址
        gaslimit: 由当前区块的gaslimit获取
        gasprice: get_gas_price获取
        nonce: 交易总数 get_transaction_count_by_address获取
        chainId: 链id
        """
        amount = int(amount, 16) if isinstance(amount, str) else int(amount)
        gaslimit = int(gaslimit, 16) if not isinstance(gaslimit, int) else gaslimit
        gasprice = int(self.get_gas_price()['result'], 16)
        nonce = int(self.get_transaction_count_by_address(account.address)['result'], 16)
        tx = {'from': account.address, 'value': amount,'to': to, 'gas': gaslimit, 'gasPrice': gasprice, 'nonce': nonce, 'chainId': self.chainid}
        if kw:
            tx.update(**kw)
        signed = account.signTransaction(tx)
        return self.send_raw_transaction(signed.rawTransaction.hex())
    
if __name__ == '__main__':
    privkey = 'xxxxxxxxx' # 这里替换成自己的私钥
    account = web3.Account.from_key(privkey)
    rpc = Rpc(rpc='https://rpc.ankr.com/eth', chainid=1)
    amount = 0.000777 # 要存款的数量
    gaslimit = 116900 # gaslimit
    mint_nft_token = '0xd4307e0acd12cf46fd6cf93bc264f5d5d1598792' # base存款的合约地址
    method = '0xefef39a1' # mint nft 方法hash值
    uint_1 = '0000000000000000000000000000000000000000000000000000000000000001'
    data = method + uint_1 # 拼接数据
    amount = hex(int(amount * math.pow(10, 18))) # 处理amount值
    res = rpc.transfer(account, to=mint_nft_token, amount=amount, gaslimit=gaslimit, data=data) # 发送交易
    print(res)