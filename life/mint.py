import web3
import requests
from rpc import Rpc
from eth_account.messages import encode_defunct

class lifeDapp:
    def __init__(self, account, rpc, aff_addr):
        self.account = account
        self.rpc = rpc
        self.aff_addr = aff_addr # 邀请地址
        self.__contract_addr = '0x37ac6a9b55dcec42145a2147c2fcccb4c737c7e4'

    def _sign_message(self):
        """钱包签名消息"""
        msg = 'address=%s,chain_id=56' % self.account.address
        res = self.account.sign_message(encode_defunct(text=msg))
        return res.signature.hex()
    
    def _login(self):
        """登录, 获取access_token"""
        headers = {'Host': 'api-v2.lifeform.cc',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        url = 'https://api-v2.lifeform.cc/api/v1/wallet_login'
        data = {
            "address": self.account.address,
            "chain_id": 56,
            "sign": self._sign_message(),
        }
        res = requests.post(url, json=data, headers=headers)
        return res.json()
    
    def _sign_mint(self, access_token):
        """签名"""
        headers = {'Host': 'pandora.lifeform.cc', 
                   'Connection': 'keep-alive',
                   'Content-Type': 'application/json',
                   'Authorization': access_token,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
        url = 'https://pandora.lifeform.cc/lifeform_bsc_prod/api/avatarCartoon/easyMintAvatar'
        data = {'gender': 'female', 'address': self.account.address, 'affAddress': self.aff_addr}
        res = requests.post(url, json=data, headers=headers)
        return res.json()

    def _mint(self, signCode, wlSignature, dataSignature, gaslimit=249822):
        """Function: mintAvatar721((address,uint256,address,uint256,address,uint256,uint256,uint256,bytes32,bytes), bytes)"""
        method = '0x5e194c37'
        addr_0 = '0000000000000000000000000000000000000000000000000000000000000040'
        uint_1 = '0000000000000000000000000000000000000000000000000000000000000200'
        addr_2 = '0000000000000000000000000c522b99695e6555c5ce853f3d8d76cb027f6ea0'
        uint_3 = '0000000000000000000000000000000000000000000000000000000000040001'
        addr_4 = '000000000000000000000000e9e7cea3dedca5984780bafc599bd69add087d56'
        uint_5 = '0000000000000000000000000000000000000000000000000000000000000000'
        addr_6 = '000000000000000000000000e9e7cea3dedca5984780bafc599bd69add087d56'
        uint_7 = '0000000000000000000000000000000000000000000000000000000000000000'
        uint_8 = '0000000000000000000000000000000000000000000000000000000000000001'
        uint_9 = '0000000000000000000000000000000000000000000000000000000000000001'
        sign_code_10 = signCode[2:]
        uint_11 = '0000000000000000000000000000000000000000000000000000000000000140'
        uint_12 = '0000000000000000000000000000000000000000000000000000000000000041'
        wl_unit13 = wlSignature[2:] + '00000000000000000000000000000000000000000000000000000000000000'
        uint_14 = '0000000000000000000000000000000000000000000000000000000000000041'
        data_sign_15 = dataSignature[2:] + '00000000000000000000000000000000000000000000000000000000000000'
        data = method + addr_0 + uint_1 + addr_2 + uint_3 + addr_4 + uint_5 + addr_6 + uint_7 + uint_8 + uint_9 + sign_code_10 + uint_11 + uint_12 + wl_unit13 + uint_14 + data_sign_15
        res = self.rpc.transfer(self.account, self.__contract_addr, 0, gaslimit, data=data)
        return res

    def mint(self):
        access_token = self._login()['data']['access_token']
        sign = self._sign_mint(access_token)
        signCode = sign['result']['condition']['signCode']
        wlSignature = sign['result']['condition']['wlSignature']
        dataSignature = sign['result']['dataSignature']['signature']
        res = self._mint(signCode, wlSignature, dataSignature)
        return res

if __name__ == '__main__':
    privkey = 'xxxxxxx' # 你的私钥
    aff_addr = '' # 邀请地址
    account = web3.Account.from_key(privkey)
    rpc = Rpc('https://bsc-dataseed.binance.org', chainid=56)
    life = lifeDapp(account, rpc, aff_addr)
    res = life.mint()
    print(res)
    