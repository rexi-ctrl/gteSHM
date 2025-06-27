from web3 import Web3

def approve_if_needed(web3, account, token_address, spender, amount, gas_price_gwei=0.1):
    abi = [
        {
            "constant": True,
            "inputs": [
                {"name": "_owner", "type": "address"},
                {"name": "_spender", "type": "address"}
            ],
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
    amount_wei = int(amount * (10 ** 18))  # konversi manual

    if allowance >= amount_wei:
        print(f"✅ Token {token_address[:6]}... sudah di-approve.")
        return True

    try:
        tx = contract.functions.approve(spender, int(1_000_000 * 10**18)).build_transaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 100000,
            'gasPrice': Web3.to_wei(gas_price_gwei, 'gwei')
        })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"📝 Approving token {token_address[:6]}... tx: {tx_hash.hex()}")
        web3.eth.wait_for_transaction_receipt(tx_hash)
        return True
    except Exception as e:
        print(f"❌ Gagal approve token {token_address[:6]}: {e}")
        return False
