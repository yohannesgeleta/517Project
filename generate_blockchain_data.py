from web3 import Web3
import random
import json
import time

# Connect to Ganache (GUI assumed running on port 7545)
ganache_url = "HTTP://127.0.0.1:7545" # Replece this when you are running Ganache GUI
web3 = Web3(Web3.HTTPProvider(ganache_url))
assert web3.is_connected(), "Failed to connect to Ganache"

accounts = web3.eth.accounts
tx_log = []

def send_tx(from_acct, to_acct, value_eth, label):
    try:
        tx = {
            'from': from_acct,
            'to': to_acct,
            'value': web3.to_wei(value_eth, 'ether'),
            'gas': 21000,
            'gasPrice': web3.to_wei('50', 'gwei')
        }

        tx_hash = web3.eth.send_transaction(tx)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        block = web3.eth.get_block(receipt.blockNumber)

        tx_log.append({
            'type': label,
            'from': from_acct,
            'to': to_acct,
            'value': value_eth,
            'tx_hash': tx_hash.hex(),
            'block_number': receipt.blockNumber,
            'timestamp': block.timestamp,
            'gas_used': receipt.gasUsed,
            'gas_price': tx['gasPrice']
        })
    except Exception as e:
        print(f"Failed transaction: {e}")

# --- CONFIGURATION ---
TOTAL_TXS = 1000
PHISHING_TXS = 20
RUG_PULL_TXS = 50
AIRDROP_TXS = 100
WASH_TRADES = 80
DOUBLE_SPENDS = 30
AUTHENTIC_TXS = TOTAL_TXS - (PHISHING_TXS + RUG_PULL_TXS + AIRDROP_TXS + 2 * WASH_TRADES + 2 * DOUBLE_SPENDS)

#  Authentic Transactions
for _ in range(AUTHENTIC_TXS):
    send_tx(random.choice(accounts[:5]), random.choice(accounts[5:]), round(random.uniform(0.01, 1.5), 4), 'authentic')

#  Phishing Scams
scam_addr = web3.to_checksum_address('0x000000000000000000000000000000000000dead')
for _ in range(PHISHING_TXS):
    send_tx(random.choice(accounts), scam_addr, round(random.uniform(1, 3), 4), 'phishing')

#  Rug Pulls (investment phase)
rug_addr = accounts[6]
for _ in range(RUG_PULL_TXS - 1):
    send_tx(random.choice(accounts[:5]), rug_addr, round(random.uniform(3, 7), 4), 'rug_pull')
# drain
send_tx(rug_addr, random.choice(accounts), round(random.uniform(10, 30), 4), 'rug_pull')

#  Airdrop Farming
target = accounts[8]
for _ in range(AIRDROP_TXS):
    send_tx(random.choice(accounts), target, round(random.uniform(0.001, 0.02), 5), 'airdrop_farming')

#  Wash Trading
for _ in range(WASH_TRADES):
    a, b = random.sample(accounts, 2)
    amt = round(random.uniform(1, 2), 4)
    send_tx(a, b, amt, 'wash_trade')
    send_tx(b, a, amt, 'wash_trade')

#  Double Spends
for _ in range(DOUBLE_SPENDS):
    a, b = random.sample(accounts, 2)
    amt = round(random.uniform(0.5, 2), 4)
    send_tx(a, b, amt, 'double_spend')
    send_tx(a, b, amt, 'double_spend')

# Save JSON
with open('mock_blockchain_transactions_large.json', 'w') as f:
    json.dump(tx_log, f, indent=2)

print(f"Done! {len(tx_log)} transactions saved to 'mock_blockchain_transactions_large.json'")
