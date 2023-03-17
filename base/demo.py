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
    privkey = 'xxxxxxx' # 这里替换成自己的私钥
    account = web3.Account.from_key(privkey)
    rpc = Rpc()
    value = 0.01 # 要存款的数量
    gaslimit = 100000 # gaslimit
    base_token = '0xe93c8cd0d409341205a592f8c4ac1a5fe5585cfa' # base存款的合约地址
    method = '0xe9e05c42' # 存款方法hash值
    addr_0 = account.address[2:].rjust(64,'0') # 地址格式处理
    amount = int(value * math.pow(10, 18)) # eth的主币精度是18位
    value = hex(amount) # value hex格式处理
    unit_1 = value[2:].rjust(64,'0')
    unit_2 = hex(int(gaslimit))[2:].rjust(64,'0')
    bool_3 = '0000000000000000000000000000000000000000000000000000000000000000'
    unit_4 = '00000000000000000000000000000000000000000000000000000000000000a0'
    unit_5 = '0000000000000000000000000000000000000000000000000000000000000000'
    data = method + addr_0 + unit_1 + unit_2 + bool_3 + unit_4 + unit_5 # 拼接数据
    res = rpc.transfer(account, to=base_token, amount=amount, gaslimit=gaslimit, data=data) # 发送交易
    print(res)