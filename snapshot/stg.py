import time
import web3
import requests
from eth_account.messages import encode_structured_data

headers = {
    'origin': 'https://snapshot.org',
    'content-type': 'application/json',
    'referer': 'https://snapshot.org/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

def hexstr_to_bytes32(text: str):
    return bytes.fromhex(text[2:])

def get_message(address, proposal):
    message = {
    "domain": {
      "name": "snapshot",
      "version": "0.1.4",
    },
    "types": {
      "EIP712Domain": [
		  	{"name": "name", "type": "string"},
		  	{"name": "version", "type": "string"},
		  ],
      "Vote": [
        {
          "name": "from",
          "type": "address"
        },
        {
          "name": "space",
          "type": "string"
        },
        {
          "name": "timestamp",
          "type": "uint64"
        },
        {
          "name": "proposal",
          "type": "bytes32"
        },
        {
          "name": "choice",
          "type": "uint32"
        },
        {
          "name": "reason",
          "type": "string"
        },
        {
          "name": "app",
          "type": "string"
        },
        {
          "name": "metadata",
          "type": "string"
        }
      ]
    },
    "message": {
      "space": "stgdao.eth",
      "proposal": hexstr_to_bytes32(proposal),
      "choice": 1,
      "app": "snapshot",
      "reason": "",
      "metadata": "{}",
      "from": address,
      "timestamp": int(time.time())
    },
    "primaryType": "Vote",
    }
    return message

def vote(account, proposal='0x108a9e597560c4f249cd8be23acd409059fcd17bb2290d69a550ac2232676e7d'):
    """投票 
    account: 账户
    proposal: 提案tx
    """
    message = get_message(account.address, proposal)
    encoded_msg = encode_structured_data(primitive=message)
    signed_msg = account.sign_message(encoded_msg)
    message['message']['proposal'] = proposal
    del message['primaryType']
    del message['types']['EIP712Domain']
    data = {'address': account.address, 'sig': signed_msg.signature.hex(), 'data': message}
    api = 'https://seq.snapshot.org/'
    res = requests.post(api, headers=headers, json=data)
    return res.json()

if __name__ == '__main__':
    pk = '' # 私钥
    proposal = '0x108a9e597560c4f249cd8be23acd409059fcd17bb2290d69a550ac2232676e7d' # 提案tx
    account = web3.Account.from_key()
    res = vote(account, proposal)
    print(res)