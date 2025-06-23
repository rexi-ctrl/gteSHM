def print_header():
    print("=" * 50)
    print("🔥 GTE AUTO SWAP BOT - Powered by SAHME 🔥")
    print("=" * 50)


def show_balances(web3, account):
    from core.config import GTE_TOKENS
    print("🔍 Saldo per token:")
    for token in GTE_TOKENS:
        balance = get_token_balance(web3, account, token)
        print(f" - {token[:8]}...: {web3.fromWei(balance, 'ether'):.4f}")


def get_token_balance(web3, account, token_address):
    abi = [{
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    }]
    contract = web3.eth.contract(address=token_address, abi=abi)
    return contract.functions.balanceOf(account.address).call()
