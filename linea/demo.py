import web3
import math
import time
import requests

headers = {
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }

class Rpc:
    """
    eth rpc方法
    """
    def __init__(self, api='https://rpc.ankr.com/eth_goerli', chainid=5, proxies=None, timeout=30):
        self.api = api
        self.chainid = chainid
        self.proxies = proxies
        self.timeout = timeout

    def get_current_block(self):
        """获取最新区块"""
        data = {"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}
        res = requests.post(self.api, json=data, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def get_block_detail(self, number):
        """获取区块hash"""
        if isinstance(number, int):
            number = hex(number)
        data = {"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":[number,True],"id":1}
        res = requests.post(self.api, json=data, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def get_transaction(self, txhash):
        """获取的交易详情"""
        data = {"jsonrpc":"2.0","method":"eth_getTransactionByHash","params":[txhash],"id":1}
        res = requests.post(self.api, json=data, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def get_gas_price(self):
        """获取gasprice"""
        data = {"jsonrpc":"2.0","method":"eth_gasPrice","params":[],"id":1}
        res = requests.post(self.api, json=data, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def get_max_gas_price(self):
        """(base*2 + Priority) * gasLimit"""
        res = self.get_fee_history()
        base = int(res['result']['baseFeePerGas'][-1], 16)
        res = self.get_max_PriorityFeePerGas()
        priority = int(res['result'], 16)
        return base * 2 + priority

    def get_fee_history(self):
        """获取历史gasfee"""
        data = {"jsonrpc":"2.0","method":"eth_feeHistory","params":["0x1", "latest", []],"id":1}
        res = requests.post(self.api, json=data, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def get_max_PriorityFeePerGas(self):
        """获取Priority"""
        data = {"jsonrpc":"2.0","method":"eth_maxPriorityFeePerGas","params":[],"id":1}
        res = requests.post(self.api, json=data, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def get_gas_limit(self, from_, to, data):
        """call计算gaslimit"""
        data = {"jsonrpc":"2.0","method":"eth_estimateGas","params":[{"from": from_, "to": to, "data": data}],"id":1}
        res = requests.post(self.api, json=data, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def get_transaction_count_by_address(self, address):
        data = {"jsonrpc":"2.0","method":"eth_getTransactionCount","params":[address,'latest'],"id":1}
        res = requests.post(self.api, json=data, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def call(self, to, data):
        data = {"jsonrpc":"2.0","method":"eth_call","params":[{"to": to, "data": data}, "latest"],"id":1}
        res = requests.post(self.api, json=data, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def send_raw_transaction(self, hex):
        """广播交易"""
        data = {"jsonrpc":"2.0","method":"eth_sendRawTransaction","params":[hex],"id":1}
        res = requests.post(self.api, json=data, headers=headers,  proxies=self.proxies, timeout=self.timeout)
        return res.json()

    def get_balance(self, address):
        """获取余额"""
        data = {"jsonrpc":"2.0","method":"eth_getBalance","params":[address, 'latest'],"id":1}
        res = requests.post(self.api, json=data, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return res.json()#(int(res.json()['result'], 16)) / math.pow(10,18)

    def transfer(self, account, to, amount, gaslimit, **kw):
        amount = int(amount, 16) if isinstance(amount, str) else int(amount)
        gaslimit = int(gaslimit, 16) if not isinstance(gaslimit, int) else gaslimit
        gasprice = int(self.get_gas_price()['result'], 16)
        nonce = int(self.get_transaction_count_by_address(account.address)['result'], 16)
        tx = {'from': account.address, 'value': amount,'to': to, 'gas': gaslimit, 'gasPrice': gasprice, 'nonce': nonce, 'chainId': self.chainid}
        if kw:
            tx.update(**kw)
        signed = account.signTransaction(tx)
        return self.send_raw_transaction(signed.rawTransaction.hex())
    
    def transfer_eip1559(self, account, to, amount, gaslimit=21000, priority_fee=None, max_gas_fee=None, **kw):
        """eip 1559发送tx, 更节省gas"""
        amount = int(amount, 16) if isinstance(amount, str) else int(amount)
        gaslimit = int(gaslimit, 16) if not isinstance(gaslimit, int) else gaslimit
        if not priority_fee:
            priority_fee = self.get_max_PriorityFeePerGas()['result']
        priority_fee = int(priority_fee, 16) if not isinstance(priority_fee, int) else priority_fee
        if not max_gas_fee:
            basefee = int(self.get_fee_history()['result']['baseFeePerGas'][-1], 16)
            max_gas_fee = 2 * basefee + priority_fee
        max_gas_fee = int(max_gas_fee, 16) if not isinstance(max_gas_fee, int) else max_gas_fee
        nonce = int(self.get_transaction_count_by_address(account.address)['result'], 16)
        tx = {'from': account.address, 'value': amount,'to': to, 'gas': gaslimit, 'maxPriorityFeePerGas': priority_fee, 'maxFeePerGas': max_gas_fee, 'nonce': nonce, 'chainId': self.chainid}
        if kw:
            tx.update(**kw)
        signed = account.signTransaction(tx)
        return self.send_raw_transaction(signed.rawTransaction.hex())

if __name__ == '__main__':
    privkey = 'xxxxxx' # 这里替换成自己的私钥
    account = web3.Account.from_key(privkey)
    COIN_DECIMALS = math.pow(10, 18) # 主币精度
    rpc = Rpc()
    value = 0.01 # 要存款的数量
    method = '0xdeace8f5' # 存款方法hash值
    uint_0 = '000000000000000000000000000000000000000000000000000000000000e704' # chainid
    addr_1 = account.address[2:].rjust(64, '0') # recipient
    amount = int(value * COIN_DECIMALS)
    uint_2 = hex(amount)[2:].rjust(64, '0') # amount
    uint_3 = '0000000000000000000000000000000000000000000000000000000000000000' # amountOutMin
    time_4 = hex(int(time.time() + 7 * 86400))[2:].rjust(64, '0') # deadline
    addr_5 = '00000000000000000000000081682250d4566b2986a2b33e23e7c52d401b7ab7' # relayer
    uint_6 = '0000000000000000000000000000000000000000000000000000000000000000' # relayerFee
    data = method + uint_0 + addr_1 +uint_2 + uint_3 + time_4 + addr_5 + uint_6
    amount += (0.01 * COIN_DECIMALS)
    data = data.lower()
    gaslimit = 130000
    to = '0xe85b69930fc6d59da385c7cc9e8ff03f8f0469ba' # linea存款的合约地址
    to = web3.Web3.toChecksumAddress(to)
    res = rpc.transfer_eip1559(account, to, amount, gaslimit, data=data)
    print(res)