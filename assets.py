
account = web3.eth.account.from_key(private_key)

balance = web3.eth.get_balance(account.address)
print(f"Баланс адреса {account.address}: {balance} wei")
