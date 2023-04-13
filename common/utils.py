import math
import web3
import sha3
from web3 import Account
from eth_account.messages import encode_defunct
from rpc import Rpc

COIN_DECIMALS = math.pow(10, 18) # 主币精度
STABLE_COIN_DECIMALS = math.pow(10, 6) # 稳定币精度

def keccak256_hash(text: str):
    """hash 函数名
    return : methodid
    """
    k = sha3.keccak_256()
    k.update(text.encode('utf-8'))
    return '0x'+ k.hexdigest()[:8]

def sign_msg(msg: str, account: Account):
    """签名消息"""
    sign = account.sign_message(encode_defunct(text=msg))
    return sign.signature.hex()

class Confirm:
    """二次确认"""

    @staticmethod
    def tx(tx: str, rpc: Rpc):
        """确认tx"""
        res = rpc.get_transaction(tx)
        print(res)
        if res['result']:
            if res['result']['blockNumber'] != '0x0' or res['result']['blockNumber'] != None:
                return True
        return False

    @staticmethod
    def balance(address: str, rpc: Rpc, threshold_value=None):
        """确认主币余额
        param address: 查询地址
        param rpc: Rpc类
        param threshold_value: 余额阈值
        """
        res = rpc.get_balance(address)
        if res['result'] == '0x0':
            return False, 0
        balance = float(int(res['result'], 16) / COIN_DECIMALS)
        if not threshold_value:
            return True, balance
        if balance < threshold_value:
            return False, balance
        return True, balance
        

class Erc20Utils:
    """ERC20标准方法
    allowance: 查询授权
    approve: 批准额度
    decimals: 查询精度
    balance_of: 查询代币额度
    transfer: 代币转账
    """
    @staticmethod
    def allowance(token, my_address: str, to_address: str, rpc: Rpc):
        """查询我的代币授权某地址额度
        token: 代币
        my_address: 我的钱包地址
        to_address: 授权地址
        rpc: PRC类
        """
        addr_1 = my_address[2:].rjust(64,'0')
        addr_2 = to_address[2:].rjust(64,'0')
        data = '0xdd62ed3e' + addr_1 + addr_2
        res = rpc.call(token, data)
        return res

    @staticmethod
    def approve(token, account: Account, spender_address: str, rpc: Rpc, value=None, gaslimit=None):
        """授权
        param token: 代币
        param account: 自己的钱包
        param spender_address: 批准的钱包地址
        param rpc: Rpc类
        param value: 批准的额度
        """
        method = '0x095ea7b3'
        addr_0 = spender_address[2:].rjust(64,'0')
        uint_1 = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
        if value:
            value = int(value, 16) if not isinstance(value, int) else value
            uint_1 = hex(value)[2:].rjust(64, '0')
        data = method + addr_0 + uint_1
        to = web3.Web3.toChecksumAddress(token)
        if not gaslimit:
            res = rpc.get_gas_limit(account.address, to, data)
            gaslimit = res['result']
        res = rpc.transfer(account, to, 0, gaslimit, data=data)
        return res

    @staticmethod
    def decimals(token: str, rpc: Rpc):
        """获取代币精度
        param token: 代币地址
        param rpc: Rpc类
        """
        method = '0x313ce567'
        data = method
        res = rpc.call(token, data)
        return res

    @staticmethod
    def balance_of(token: str, address: str, rpc: Rpc):
        """查询代币下的某地址余额
        param token: 代币地址
        param address: 查询地址
        param rpc: Rpc类
        """
        data = '0x70a08231' + address[2:].rjust(64, '0')
        res = rpc.call(token, data)
        return res

    @staticmethod
    def transfer(token, account: Account, recipient_address: str, rpc: Rpc, value=None, gaslimit=None):
        """代币转账
        param token: 代币地址
        param account: 发送账号
        param recipient_address: 接收人地址
        """
        method = '0xa9059cbb'
        addr_0 = recipient_address[2:].rjust(64, '0') # 转移地址
        if not value:
            res = Erc20Utils.balance_of(token, account.address, rpc)
            value = res['result']
        value = hex(value) if isinstance(value, int) else value
        uint_1 = value[2:].rjust(64, '0') # amount 数量
        data = method + addr_0 + uint_1
        data = data.lower()
        to = web3.Web3.toChecksumAddress(token)
        res = rpc.get_gas_limit(account.address, to, data)
        gaslimit = int(res['result'], 16)
        res = rpc.transfer(account, to, 0, gaslimit, data=data)
        return res