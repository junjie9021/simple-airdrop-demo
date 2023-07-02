import hmac
import json
import base64
import requests
import datetime

class OkxAccount:
    """okx 账户类操作
    https://www.okx.com/docs-v5/zh/#rest-api-funding-get-currencies
    """
    headers = {'Content-Type':'application/json'}

    def __init__(self, ak, sk, passphrase, api='https://www.okx.com'):
        self.ak = ak
        self.sk = sk
        self.passphrase = passphrase
        self.api = api

    def _request(self, method, request_path, body=None):
        timestamp = datetime.datetime.utcnow().isoformat("T", "milliseconds") + 'Z'
        self.headers['OK-ACCESS-KEY'] = self.ak
        self.headers['OK-ACCESS-TIMESTAMP'] = timestamp
        self.headers['OK-ACCESS-PASSPHRASE'] = self.passphrase
        signature = self.signature(timestamp, method.upper(), request_path, body)
        self.headers['OK-ACCESS-SIGN'] = signature
        api = self.api + request_path
        if method.upper() == 'GET':
            res = requests.get(api, headers=self.headers)
        if method.upper() == 'POST':
            res = requests.post(api, headers=self.headers, json=body)
        return res.json()

    def signature(self, timestamp, method, request_path, body):
        body = '' if not body else json.dumps(body)
        message = str(timestamp) + str.upper(method) + request_path + body
        mac = hmac.new(bytes(self.sk, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)

    def get_balance(self):
        """获取账户资金余额"""
        method = 'GET'
        request_path = '/api/v5/asset/balances'
        return self._request(method, request_path)
    
    def withdrawal(self, amt, toAddr, chain, dest="4", ccy='ETH'):
        """提币, 默认ETH; 参考 https://www.okx.com/docs-v5/zh/#rest-api-funding-withdrawal
        amt: 数量
        toAddr: 接收地址
        fee: 手续费
        chain: 网络
        """
        method = 'POST'
        request_path = '/api/v5/asset/withdrawal'
        fee, chain = self.get_fee(ccy, chain)
        body = {'amt': str(amt), 'toAddr': toAddr, 'chain': chain, 'fee': fee, 'dest': str(dest), 'ccy': ccy}
        return self._request(method, request_path, body)

    def get_currency(self):
        """获取所有资产"""
        method = 'GET'
        request_path = '/api/v5/asset/currencies'
        return self._request(method, request_path)

    def get_fee(self, ccy='ETH', chain='zksync era'):
        """获取网络提现手续费
        ccy: 代币
        chain: 网络
        """
        res = self.get_currency()
        fee = 0
        chain = None
        for i in res['data']:
            if i['ccy'].upper() == ccy.upper():
                if chain.upper() in i['chain'].upper():
                    fee = i['minFee']
                    chain = i['chain']
        return fee, chain

if __name__ == '__main__':
    ak = '' # api key
    sk = '' # secret key
    passphrase = '' # 密码
    account = OkxAccount(ak, sk, passphrase)
    value = 0.01 # 提现eth数量
    to = '' # 接收地址
    res = account.withdrawal(value, to, 'zksync era')
    print(res)