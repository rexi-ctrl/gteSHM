
from web3 import Web3

def approve_token(web3, account, token_address, spender, amount):
    abi = [{
        "constant": False,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }]
    contract = web3.eth.contract(address=token_address, abi=abi)
    try:
        tx = contract.functions.approve(spender, int(amount)).build_transaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 60000,
            'gasPrice': Web3.to_wei(1, 'gwei')
        })
        signed_tx = web3.eth.account.sign_transaction(tx, account.key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"✅ Approve berhasil: {web3.to_hex(tx_hash)}")
        return tx_hash
    except Exception as e:
        print(f"❌ Gagal approve: {e}")
        return None

def swap(web3, account, router, token_in, token_out, amount_in):
    try:
        deadline = web3.eth.get_block('latest')['timestamp'] + 1200
        tx = router.functions.swapExactTokensForTokens(
            int(amount_in),
            0,
            [token_in, token_out],
            account.address,
            deadline
        ).build_transaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 200000,
            'gasPrice': Web3.to_wei(1, 'gwei')
        })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"✅ Swap berhasil: {web3.to_hex(tx_hash)}")
        return tx_hash
    except Exception as e:
        print(f"❌ Swap gagal: {e}")
        return None
