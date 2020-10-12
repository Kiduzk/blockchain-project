import pickle
import json
from hashlib import sha256

def read_file(file_name):
    try:
        with open(file_name, "rb") as f:
            read = pickle.load(f)
        return read
    except FileNotFoundError:
        return False

def write_to_file(file_name, data):
    with open(file_name, "wb") as f:
        pickle.dump(data, f)
    return True  

def load_blockchain(gen_block):
    if not read_file("blockchain"):
        write_to_file("blockchain", [gen_block])
        return [gen_block]
    else:
        return read_file("blockchain")

def load_participants(owner):
    if not read_file("participants"):
        write_to_file("participants", {owner})
        return {owner}
    else:
        return read_file("participants")

def load_transactions():
    if not read_file("transactions"):
        write_to_file("transactions", [])
        return []
    else:
        return read_file("transactions")

def validate_proof_of_work(prev_hash, outstanding_transactions, proof_of_work):
    return sha256((str(prev_hash) + str(outstanding_transactions) + str(proof_of_work)).encode()).hexdigest().startswith("0" * number_of_zeros)
 
def hash_block(block):
    return sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
 
def get_user_choice():
    return input("Your choice: ")
 
def get_last_blockchain_value(blockchain):
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def print_blockchain_elements(blockchain):
    for block in blockchain:
        print("Outputting Block")
        print(block)

def get_transaction_details():
    recepient = input("Please enter recepient: ")
    amount = float(input("Enter transaction amount: "))
    return recepient, amount

def print_participant_balance(participants):
    for participant in participants:
        print(participant, get_balance(participant))
  