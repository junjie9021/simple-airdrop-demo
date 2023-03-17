"""
pip install bip_utils
"""

import nacl
import base64
import hashlib
import requests
import bip_utils
from rpc import Rpc

headers = {
    'content-type': 'application/json',
    }

class Account:
    def __init__(self,  mnemonic: str, derivation_path="m/44'/784'/0'/0'/0'"):
        self.mnemonic = mnemonic
        self.derivation_path = derivation_path
        self.bip39_seed = bip_utils.Bip39SeedGenerator(self.mnemonic).Generate()  # or = bip39.phrase_to_seed(mnemonic)
        self.bip32_ctx = bip_utils.Bip32Slip10Ed25519.FromSeed(self.bip39_seed)
        self.bip32_der_ctx = self.bip32_ctx.DerivePath(derivation_path)
        self.private_key: bytes = self.bip32_der_ctx.PrivateKey().Raw().ToBytes()
        self.public_key: bytes = self.bip32_der_ctx.PublicKey().RawCompressed().ToBytes()
        self.full_private_key = self.private_key[:32] + self.public_key[1:]
        self.address = self.get_address()

    @staticmethod
    def generate():
        return Account(mnemonic=bip_utils.Bip39MnemonicGenerator().FromWordsNumber(bip_utils.Bip39WordsNum.WORDS_NUM_12).ToStr())

    def get_address(self) -> str:
        return "0x" + hashlib.sha3_256(self.bip32_der_ctx.PublicKey().RawCompressed().ToBytes()).digest().hex()[:40]

    def sign_data(self, data: bytes) -> bytes:
        return nacl.signing.SigningKey(self.private_key).sign(data)[:64]  # Todo: support secp256k1 key and signature

    def get_public_key_as_b64_string(self) -> str:
        return base64.b64encode(self.public_key[1:]).decode()
    
if __name__ == '__main__':
    rpc = Rpc('https://fullnode.devnet.sui.io')
    account = Account.generate() # 生成一个地址
    account = Account('pilot fish popular tuna energy zoo initial vivid gym win gain author')
    print(account.mnemonic, account.address) # 打印私钥和地址
    faucet_url = 'https://faucet.devnet.sui.io/gas'
    data = {"FixedAmountRequest":{"recipient": account.address}}
    res = requests.post(faucet_url, json=data,  headers=headers, verify=False) # 领水
    print(res.json()) # 打印输出
    # mint nft
    args = ["Example NFT", "An NFT created by Sui Wallet", "ipfs://QmZPWWy5Si54R3d26toaqRiqvCH7HkGdXkxwUgCm2oKKM2?filename=img-sq-01.png"] # mint nft的参数
    res = rpc.move_call(account.address, '0x2', 'devnet_nft', 'mint', args, gas_budget=2000) # 与合约交互获取返回的txBytes
    tx = res['result']['txBytes']
    res = rpc.sendtx(tx, account) # 广播交易
    print(res) # 打印交易hash
    