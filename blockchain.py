from collections import OrderedDict 
from utility import *
import json

MINIG_REWARD = 10
number_of_zeros = 2
gen_block = {"nonce": 0, "previous_hash": "", "index": 0, "transactions": []}
blockchain = load_blockchain(gen_block)
outstanding_transactions = load_transactions()
owner = "Kaleb"
participants = load_participants(owner)

def add_transaction(recepient, sender=owner, amount=1.0):
    transaction = OrderedDict([("sender", sender), ("recepient", recepient), ("amount", amount)])
 
    if verify_transaction(transaction):
        outstanding_transactions.append(transaction)
        participants.add(sender)
        participants.add(recepient)
        write_to_file("participants", participants)
        return True
 
    return False
 
def get_proof_of_work():
    proof_of_work = 0
    while not validate_proof_of_work(hash_block(get_last_blockchain_value(blockchain)), outstanding_transactions, proof_of_work):
        proof_of_work += 1

    return proof_of_work

def mine_block():
    global outstanding_transactions

    proof_of_work = get_proof_of_work()
    last_block = get_last_blockchain_value(blockchain)

    mining_reward_transaction = OrderedDict([("sender", None), ("recepient", owner), ("amount", MINIG_REWARD)])
    outstanding_transactions.append(mining_reward_transaction)

    new_block = {
        "previous_hash": hash_block(last_block),
        "index": int(last_block["index"]) + 1,
        "transactions": outstanding_transactions,
        "nonce": proof_of_work
    }
    outstanding_transactions = []
    blockchain.append(new_block)
    write_to_file("blockchain", blockchain)
 
def verify_transaction(transaction):
    sender_balance = get_balance(transaction["sender"])
    return sender_balance >= transaction["amount"]
 
def verify_blockchain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block["previous_hash"] != hash_block(blockchain[index - 1]):
            return False
        if not validate_proof_of_work(block["previous_hash"], block["transactions"][:-1], block["nonce"]):
            return False 
    return True

def get_balance(participant):
    amount_sent = 0.0
    amount_received = 0.0
 
    for block in blockchain:
        for transaction in block["transactions"]:
            if transaction["sender"] == participant:
                amount_sent += transaction["amount"]
            elif transaction["recepient"] == participant:
                amount_received += transaction["amount"]
 
    for transaction in outstanding_transactions:
        if transaction["sender"] == participant:
            amount_sent += transaction["amount"]
 
    return float(amount_received - amount_sent)

while True:
    print("Hello, please choose: ")
    print("1: Add a new transaction")
    print("2: Mine a new block")
    print("3: Output the blockchain blocks")
    print("4: Output the participant balance")
    print("q: Quit")
    user_choice = get_user_choice()
 
    if user_choice == "1":
        tx_details = get_transaction_details()
        recepient, amount = tx_details
        if add_transaction(recepient, amount=amount):
            print("Transaction successful!")
        else:
            print("Invalid transaction. Insufficient funds")
    elif user_choice == "2":
        mine_block()

        if not verify_blockchain():
            print("Invalid blockchain!")
            break
    elif user_choice == "3":
        print_blockchain_elements(blockchain)
    elif user_choice == "4":
        print_participant_balance(participants)
    elif user_choice == "q":
        write_to_file("transactions", outstanding_transactions)
        break
 
print(blockchain)
