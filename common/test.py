import math
import web3
from rpc import Rpc
from utils import Confirm, Erc20Utils

def test_balance_of(token, address, rpc):
    """测试获取地址代币余额"""
    res = Erc20Utils.decimals(token, rpc) # 获取代币精度
    decimals = int(res['result'], 16)
    res = Erc20Utils.balance_of(token, address, rpc) # 获取代币余额
    balance = int(res['result'], 16)
    return balance / math.pow(10, decimals)

def test_allowance(token, my_address, to_address, rpc):
    """测试获取地址代币余额批准to_address额度"""
    res = Erc20Utils.decimals(token, rpc) # 获取代币精度
    decimals = int(res['result'], 16)
    res = Erc20Utils.allowance(token, my_address, to_address, rpc) # 获取代币余额
    value = int(res['result'], 16)
    return value / math.pow(10, decimals)


if __name__ == '__main__':
    # 以下示例为 Arb 链操作
    proxies = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
    rpc = Rpc(proxies=proxies)
    token = '0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9' # usdt 代币合约地址
    address = '0xf89d7b9c864f589bbf53a82105107622b35eaa40' # 要查询的地址
    # print('检查地址 0xf89d7b9c864f589bbf53a82105107622b35eaa40 的代币USDT余额')
    # res = test_balance_of(token, address, rpc)
    # print(res)

    # print('检查地址 0xf89d7b9c864f589bbf53a82105107622b35eaa40 的代币USDT对 uniswap permit2 授权')
    # to_address = '0x000000000022D473030F116dDEE9F6B43aC78BA3' # Uniswap Protocol: Permit2
    # res = test_allowance(token, my_address, to_address, rpc)
    # print(res)

    # print('授权地址 xxxxx 的代币USDT对 uniswap permit2 的授权')
    # pk = 'xxxxx' # 私钥
    # account = web3.Account.from_key(pk)
    # res = Erc20Utils.approve(token, account, to_address, rpc)
    # print(res)

    # print('地址 xxxxx USDT代币转账给 to_address')
    # account = web3.Account.from_key(pk)
    # res = Erc20Utils.transfer(token, account, to_address, rpc)
    # print(res)

    # print('确认地址 0xf89d7b9c864f589bbf53a82105107622b35eaa40 主币余额')
    # res = Confirm.balance(address, rpc)
    # status, balance = res[0], res[1]
    # print(status, balance)

    # print('确认tx 0xdc5fafc861a562ef1ce4346f03a37f1070d9cd67029aa89f5e98b6ec039d26df 状态')
    # tx = '0xdc5fafc861a562ef1ce4346f03a37f1070d9cd67029aa89f5e98b6ec039d26df'
    # res = Confirm.tx(tx, rpc)
    # print(res)