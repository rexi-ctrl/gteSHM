
from web3 import Web3

def approve_if_needed(web3, account, token_address, spender, amount):
    abi = [
        {
            "constant": True,
            "inputs": [
                {"name": "_owner", "type": "address"},
                {"name": "_spender", "type": "address"}
            ],
            "name": "allowance",
            "outputs": [{"name": "remaining", "type": "uint256"}],
            "name": "allowance",
            "outputs": [{"name": "remaining", "type": "uint256"}],
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [
                {"name": "_spender", "type": "address"},
                {"name": "_value", "type": "uint256"}
            ],
            "name": "approve",
            "outputs": [{"name": "success", "type": "bool"}],
            "type": "function"
        }
    ]

    contract = web3.eth.contract(address=token_address, abi=abi)
    allowance = contract.functions.allowance(account.address, spender).call()

    if allowance >= int(amount):
        print(f"✅ Token {token_address[:6]}... sudah di-approve.")
        return True

    try:
        tx = contract.functions.approve(spender, Web3.toWei(1_000_000, 'ether')).build_transaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 100000,
            'gasPrice': web3.toWei('1', 'gwei')
        })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"📝 Approving token {token_address[:6]}... tx: {web3.toHex(tx_hash)}")
        web3.eth.wait_for_transaction_receipt(tx_hash)
        return True
    except Exception as e:
        print(f"❌ Gagal approve token {token_address[:6]}: {e}")
        return False
