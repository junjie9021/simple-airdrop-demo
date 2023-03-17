import uuid
import json
import base64
import urllib3
import requests
from typing import List
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'content-type': 'application/json',
    }

SUI_COIN_TYPE = "0x2::coin::Coin<0x2::sui::SUI>"


class Rpc:
    def __init__(self, api='https://fullnode.testnet.sui.io/', proxies=None):
        self.api = api
        self.proxies = proxies

    def get_objects(self, address):
        """获取地址拥有的objs
        """
        data = {"method": "sui_getObjectsOwnedByAddress","jsonrpc": "2.0","params": [address],"id": str(uuid.uuid1())}
        res = requests.post(self.api, data=json.dumps(data), headers=headers, proxies=self.proxies)
        return res.json()
        
    def get_object(self, obj_id):
        """返回指定对象的对象信息;
        """
        data = {"method": "sui_getObject","jsonrpc": "2.0","params": [obj_id],"id": str(uuid.uuid1())}
        res = requests.post(self.api, data=json.dumps(data), headers=headers, proxies=self.proxies)
        return res.json()

    def get_transaction(self, tx):
        """获取交易详情
        """
        data = {"method": "sui_getTransaction","jsonrpc": "2.0","params": [tx],"id": str(uuid.uuid1())}
        res = requests.post(self.api, data=json.dumps(data), headers=headers, proxies=self.proxies)
        return res.json()

    def transfer_sui(self, from_, object_id, to, amount, gas=1000,):
        """创建一个未签名的交易以将 SUI 硬币对象发送到 Sui 地址。 SUI 对象也用作气体对象。
        """
        data = {"method": "sui_transferSui","jsonrpc": "2.0","params": [from_, object_id, gas, to, int(amount)],"id": str(uuid.uuid1())}
        res = requests.post(self.api, data=json.dumps(data), headers=headers, proxies=self.proxies)
        return res.json()

    def pay_sui(self, from_, objs, to, amount, gas=300):
        """创建一个未签名的交易以将 SUI 硬币对象发送到 Sui 地址。 SUI 对象也用作气体对象。
        """
        data = {"method": "sui_paySui","jsonrpc": "2.0","params": [from_, objs, [to], amount, gas],"id": str(uuid.uuid1())}
        res = requests.post(self.api, data=json.dumps(data), headers=headers, proxies=self.proxies)
        return res.json()

    def pay_all_sui(self, from_, objs, to, gas=1000):
        """创建一个未签名的交易以将 SUI 硬币对象发送到 Sui 地址。 SUI 对象也用作气体对象。
        """
        data = {"method": "sui_payAllSui","jsonrpc": "2.0","params": [from_, objs, to, gas],"id": str(uuid.uuid1())}
        res = requests.post(self.api, data=json.dumps(data), headers=headers, proxies=self.proxies)
        return res.json()

    def transfer(self, from_, to, amount):
        objs = self.get_objects(from_)
        amount = int(amount)
        sui_objs = [i['objectId'] for i in objs['result'] if i['type'] == SUI_COIN_TYPE]
        balance = 0
        pay_objs = []
        for i in sui_objs:
            obj = self.get_object(i)
            if int(obj['result']['details']['data']['fields']['balance']) > amount:
                res = self.pay_sui(from_, [i], to, [amount])
                return res
            balance += int(obj['result']['details']['data']['fields']['balance'])
            pay_objs.append(i)
            if balance >= amount:
                res = self.pay_sui(from_, pay_objs, to, [amount])
                return res

    def merge_coin(self, address, primary_obj_id, merge_obj_id, gas=1000, gas_object_id=None):
        """合并硬币;
        """
        gas_object_id = primary_obj_id
        data = {"method": "sui_mergeCoins","jsonrpc": "2.0","params": [address, primary_obj_id, merge_obj_id, gas_object_id, gas],"id": str(uuid.uuid1())}
        res = requests.post(self.api, data=json.dumps(data), headers=headers, proxies=self.proxies)
        return res.json()

    def execute_transaction(self, tx_bytes, signature_bytes, pub_key, request_type="WaitForLocalExecution"):
        """广播交易
        """
        flag = {
            "ed25519": 0x00,
            "secp256k1": 0x01,
        }
        sign_b64 = base64.b64encode(signature_bytes).decode()
        serialized_sig = [flag["ed25519"]] + \
                         list(base64.b64decode(sign_b64)) + \
                         list(base64.b64decode(pub_key))
        signature = base64.b64encode(bytes(serialized_sig)).decode()
        data = {"method": "sui_executeTransactionSerializedSig","jsonrpc": "2.0","params": [tx_bytes, signature, request_type],"id": str(uuid.uuid1())}
        res = requests.post(self.api, data=json.dumps(data), headers=headers, proxies=self.proxies)
        return res.json()

    def transfer_object(self, from_, object_id, to, gas=1000, gas_object_id=None):
        """创建一个未签名的交易以将 SUI 硬币对象发送到 Sui 地址。 SUI 对象也用作气体对象。
        """
        data = {"method": "sui_transferObject","jsonrpc": "2.0","params": [from_, object_id, gas_object_id, gas, to],"id": str(uuid.uuid1())}
        res = requests.post(self.api, data=json.dumps(data), headers=headers)
        return res.json()

    def move_call(self, address, package_object_id, module, function, arguments, gas_budget=10000, type_arguments=[], gas=None):
        """合约交互"""
        data = {"method": "sui_moveCall","jsonrpc": "2.0","params": [address, package_object_id, module, function, type_arguments, arguments, gas, gas_budget],"id": str(uuid.uuid1())}
        res = requests.post(self.api, data=json.dumps(data), headers=headers, proxies=self.proxies)
        return res.json()

    def sendtx(self, tx, account):
        """广播交易"""
        # 1.对tx进行base64编码
        tx_b64 = base64.b64decode(tx)
        # 2. 签名 [0, 0, 0] + tx; 参考 https://github.com/MystenLabs/sui/pull/6445
        data = bytes([0, 0, 0] + list(map(int, tx_b64)))
        signature_bytes = account.sign_data(data)
        pub_key = account.get_public_key_as_b64_string()
        res = self.execute_transaction(tx, signature_bytes, pub_key)
        return res
