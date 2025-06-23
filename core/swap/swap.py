def swap(web3, account, router, token_in, token_out, amount_in):
    try:
        deadline = web3.eth.get_block('latest')['timestamp'] + 1200
        tx = router.functions.swapExactTokensForTokens(
            int(amount_in),
            0,  # amountOutMin = 0 for testnet
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
        print(f"✅ Swap berhasil: {web3.toHex(tx_hash)}")
        return tx_hash
    except Exception as e:
        print(f"❌ Swap gagal: {e}")
        return None
