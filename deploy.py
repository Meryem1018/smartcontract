import json
from solcx import compile_standard, install_solc
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./WSNcontract.sol", "r") as file:
    WSNcontract_file = file.read()
    # print(WSNcontract_file)

print("Installing...")
install_solc("0.8.17")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"WSNcontract.sol": {"content": WSNcontract_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.17",
)


with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["WSNcontract.sol"]["SecureMonitoring"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["WSNcontract.sol"]["SecureMonitoring"]["metadata"]
)["output"]["abi"]


# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337

sup_address = "0xFb8E7ef8453Ff07815f53D3697614bacf77dc76a"  # address of the supervisor
op_address = "0x3deea4dc72f6735374C26AAE49939F375e790F07"  # address of the operator







op_private_key = os.getenv("op_private_key")
sup_private_key = os.getenv("sup_private_key")

SecureMonitoring = w3.eth.contract(abi=abi, bytecode=bytecode)


# Get the latest transaction
nonce = w3.eth.getTransactionCount(op_address)
# Submit the transaction that deploys the contract
transaction = SecureMonitoring.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": op_address,
        "nonce": nonce,
    }
)

# print(transaction)

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=op_private_key)
print("Deploying Contract!")
# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


# Working with deployed Contracts
securemonitoring = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Deploy the WSN by operator

transaction_2 = securemonitoring.functions.WSN_deployment().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": op_address,
        "nonce": nonce + 1,
    }
)
signed_txn_2 = w3.eth.account.sign_transaction(
    transaction_2, private_key=op_private_key
)
txn_2_hash = w3.eth.send_raw_transaction(signed_txn_2.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(txn_2_hash)
print(f"WSN deployed in plug and play operation")


# Update the state of the estimation procedure by operator

transaction_3 = securemonitoring.functions.state_estimation().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": op_address,
        "nonce": nonce + 2,
    }
)
signed_txn_3 = w3.eth.account.sign_transaction(
    transaction_3, private_key=op_private_key
)
txn_3_hash = w3.eth.send_raw_transaction(signed_txn_3.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(txn_3_hash)
print(f"state of WSN recorded")


# Record the estimate by operator

transaction_4 = securemonitoring.functions.record_state_estimate(83).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": op_address,
        "nonce": nonce + 3,
    }
)
signed_txn_4 = w3.eth.account.sign_transaction(
    transaction_4, private_key=op_private_key
)
txn_4_hash = w3.eth.send_raw_transaction(signed_txn_4.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(txn_4_hash)
print(f"state estimate has been recorded")

# Check for anomalies in the estimate by the operator
transaction_5 = securemonitoring.functions.check_for_anomalies().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": op_address,
        "nonce": nonce + 4,
    }
)
signed_txn_5 = w3.eth.account.sign_transaction(
    transaction_5, private_key=op_private_key
)
txn_5_hash = w3.eth.send_raw_transaction(signed_txn_5.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(txn_5_hash)
print(f"Anomaly check completed")


# Deploy WSN fully by supervisor
transaction_6 = securemonitoring.functions.deploy_WSN_fully().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": sup_address,
        "nonce": nonce + 5,
    }
)
signed_txn_6 = w3.eth.account.sign_transaction(
    transaction_6, private_key=sup_private_key
)
txn_6_hash = w3.eth.send_raw_transaction(signed_txn_6.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(txn_6_hash)
print(f"WSN fully deployed")


# raise_alarm_supervisor
transaction_7 = securemonitoring.functions.raise_alarm().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": sup_address,
        "nonce": nonce + 6,
    }
)
signed_txn_7 = w3.eth.account.sign_transaction(
    transaction_7, private_key=sup_private_key
)
txn_7_hash = w3.eth.send_raw_transaction(signed_txn_7.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(txn_7_hash)
print(f"Alarm raised")


# confirm anomalies by supervisor
transaction_8 = securemonitoring.functions.confirm_anomalies().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": sup_address,
        "nonce": nonce + 7,
    }
)
signed_txn_8 = w3.eth.account.sign_transaction(
    transaction_8, private_key=sup_private_key
)
txn_8_hash = w3.eth.send_raw_transaction(signed_txn_8.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(txn_8_hash)
print(f"Anomalies Confirmed")

# Getter functions

# to view estimate
transaction_9 = securemonitoring.functions.view_estimate().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": op_address,
        "nonce": nonce + 8,
    }
)
signed_txn_9 = w3.eth.account.sign_transaction(
    transaction_9, private_key=op_private_key
)
txn_9_hash = w3.eth.send_raw_transaction(signed_txn_9.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(txn_9_hash)

# to view state of WSN
transaction_10 = securemonitoring.functions.view_state_of_WSN().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": op_address,
        "nonce": nonce + 9,
    }
)
signed_txn_10 = w3.eth.account.sign_transaction(
    transaction_10, private_key=op_private_key
)
txn_10_hash = w3.eth.send_raw_transaction(signed_txn_10.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(txn_10_hash)

# view state of estimate recording
transaction_11 = securemonitoring.functions.view_state_of_estimate().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": op_address,
        "nonce": nonce + 10,
    }
)
signed_txn_11 = w3.eth.account.sign_transaction(
    transaction_11, private_key=op_private_key
)
txn_11_hash = w3.eth.send_raw_transaction(signed_txn_11.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(txn_11_hash)

# view how many times estimate has been viewed by certain address

transaction_12 = securemonitoring.functions.view_times_visited(
    op_address
).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": sup_address,
        "nonce": nonce + 11,
    }
)
signed_txn_12 = w3.eth.account.sign_transaction(
    transaction_12, private_key=sup_private_key
)
txn_12_hash = w3.eth.send_raw_transaction(signed_txn_12.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(txn_12_hash)

# view if anomaly detected

transaction_13 = securemonitoring.functions.view_anomaly_detected().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": op_address,
        "nonce": nonce + 12,
    }
)
signed_txn_13 = w3.eth.account.sign_transaction(
    transaction_13, private_key=op_private_key
)
txn_13_hash = w3.eth.send_raw_transaction(signed_txn_13.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(txn_13_hash)

# view anomaly type
transaction_14 = securemonitoring.functions.view_anomaly_type().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": op_address,
        "nonce": nonce + 13,
    }
)
signed_txn_14 = w3.eth.account.sign_transaction(
    transaction_14, private_key=op_private_key
)
txn_14_hash = w3.eth.send_raw_transaction(signed_txn_14.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(txn_14_hash)

###################The End#######################
