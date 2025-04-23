from web3 import Web3
import random
import json
import time

# Connect to Ganache
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

assert web3.isConnected(), "Failed to connect to Ganache"
accounts = web3.eth.accounts

tx_log = []

def send_tx(from_acct, to_acct, value_eth, label):
    tx = {
        'from': from_acct,
        'to': to_acct,
        'value': web3.toWei(value_eth, 'ether'),
        'gas': 21000,
        'gasPrice': web3.toWei('50', 'gwei')
    }
    tx_hash = web3.eth.send_transaction(tx)
    tx_log.append({
        'type': label,
        'from': from_acct,
        'to': to_acct,
        'value': value_eth,
        'tx_hash': tx_hash.hex()
    })

# ✅ Authentic transactions
for _ in range(20):
    from_acct = random.choice(accounts[:5])
    to_acct = random.choice(accounts[5:])
    value = round(random.uniform(0.1, 1.0), 4)
    send_tx(from_acct, to_acct, value, 'authentic')
    time.sleep(0.1)

# 🚨 Rug Pull: send from multiple users to a fake project, then drain
rug_addr = accounts[6]
for i in range(3):
    send_tx(accounts[i], rug_addr, 5, 'rug_pull')
send_tx(rug_addr, accounts[9], 15, 'rug_pull')

# 🎣 Phishing Scam: user sends ETH to a scam address
scam_addr = '0x000000000000000000000000000000000000dead'
send_tx(accounts[2], scam_addr, 3, 'phishing')

# 🔁 Double Transaction
for _ in range(2):
    send_tx(accounts[1], accounts[4], 1, 'double_spend')
    time.sleep(0.1)

# 🪂 Airdrop Farming: multiple small transactions to one address
airdrop_target = accounts[8]
for i in range(5):
    send_tx(accounts[i], airdrop_target, 0.01, 'airdrop_farming')

# 🔄 Wash Trading: repetitive send/receive
for _ in range(3):
    send_tx(accounts[3], accounts[7], 2, 'wash_trade')
    send_tx(accounts[7], accounts[3], 2, 'wash_trade')

# 💾 Save the data
with open('mock_blockchain_transactions.json', 'w') as f:
    json.dump(tx_log, f, indent=2)

print("✔️ Generated mock blockchain data and saved to 'mock_blockchain_transactions.json'")
