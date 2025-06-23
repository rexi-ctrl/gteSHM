
def wrap_eth(web3, account, weth_address, amount_eth):
    abi = [
        {
            "constant": False,
            "inputs": [],
            "name": "deposit",
            "outputs": [],
            "payable": True,
            "stateMutability": "payable",
            "type": "function"
        }
    ]

    contract = web3.eth.contract(address=weth_address, abi=abi)

    try:
        tx = contract.functions.deposit().build_transaction({
            'from': account.address,
            'value': int(amount_eth * 10**18),
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 100000,
            'gasPrice': web3.eth.gas_price
        })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"💠 Wrapping {amount_eth:.4f} ETH to WETH... tx: {tx_hash.hex()}")
        web3.eth.wait_for_transaction_receipt(tx_hash)
        return True
    except Exception as e:
        print(f"❌ Gagal wrap ETH: {e}")
        return False
