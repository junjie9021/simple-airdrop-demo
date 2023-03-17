import requests

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

class Rpc:
    """
    eth rpc方法
    """
    def __init__(self, rpc='https://rpc.ankr.com/eth_goerli', chainid=5, proxies=None):
        self.rpc = rpc
        self.chainid = chainid
        self.proxies = proxies

    def get_current_block(self):
        """获取最新区块"""
        data = {"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}
        res = requests.post(self.rpc, json=data, headers=headers, proxies=self.proxies)
        return res.json()

    def get_block_detail(self, number):
        """获取区块hash"""
        if isinstance(number, int):
            number = hex(number)
        data = {"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":[number,True],"id":1}
        res = requests.post(self.rpc, json=data, headers=headers, proxies=self.proxies)
        return res.json()

    def call(self, to, data):
        data = {"jsonrpc":"2.0","method":"eth_call","params":[{"to": to, "data": data}, "latest"],"id":1}
        res = requests.post(self.rpc, json=data, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def get_transaction(self, txhash):
        """获取的交易详情"""
        data = {"jsonrpc":"2.0","method":"eth_getTransactionByHash","params":[txhash],"id":1}
        res = requests.post(self.rpc, json=data, headers=headers)
        return res.json()

    def get_gas_price(self):
        """获取gas"""
        data = {"jsonrpc":"2.0","method":"eth_gasPrice","params":[],"id":1}
        res = requests.post(self.rpc, json=data, headers=headers, proxies=self.proxies)
        return res.json()

    def get_transaction_count_by_address(self, address):
        data = {"jsonrpc":"2.0","method":"eth_getTransactionCount","params":[address,'latest'],"id":1}
        res = requests.post(self.rpc, json=data, headers=headers, proxies=self.proxies)
        return res.json()

    def send_raw_transaction(self, hex):
        """广播交易"""
        data = {"jsonrpc":"2.0","method":"eth_sendRawTransaction","params":[hex],"id":1}
        res = requests.post(self.rpc, json=data, headers=headers,  proxies=self.proxies)
        return res.json()

    def get_balance(self, address):
        """获取余额"""
        data = {"jsonrpc":"2.0","method":"eth_getBalance","params":[address, 'latest'],"id":1}
        res = requests.post(self.rpc, json=data, headers=headers, proxies=self.proxies)
        return res.json()#(int(res.json()['result'], 16)) / math.pow(10,18)

    def get_code(self, address, block="latest"):
        block = hex(block) if isinstance(block, int) else block
        data = {"jsonrpc":"2.0","method":"eth_getCode","params":[address, block],"id":1}
        res = requests.post(self.rpc, json=data, headers=headers, proxies=self.proxies)
        return res.json()

    def transfer(self, account, to, amount, gaslimit, **kw):
        """离线交易
        prvikey: 私钥
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