from collections import OrderedDict 
from utility import *
import json, pprint

class Blockchain:

    def __init__(self, owner):
        # constants
        self.MINIG_REWARD = 10
        self.number_of_zeros = 2
        self.gen_block = {"nonce": 0, "previous_hash": "", "index": 0, "transactions": []}
        self.blockchain = load_blockchain(self.gen_block)
        self.outstanding_transactions = load_transactions()
        self.owner = owner
        self.participants = load_participants(owner)

    def add_transaction(self, recepient, amount=1.0):
        sender = self.owner
        transaction = OrderedDict([("sender", sender), ("recepient", recepient), ("amount", amount)])
    
        if self.verify_transaction(transaction):
            self.outstanding_transactions.append(transaction)
            self.participants.add(sender)
            self.participants.add(recepient)
            write_to_file("participants", self.participants)
            return True
    
        return False
    
    def get_proof_of_work(self):
        proof_of_work = 0
        while not validate_proof_of_work(hash_block(get_last_blockchain_value(self.blockchain)), self.outstanding_transactions, proof_of_work, self.number_of_zeros):
            proof_of_work += 1

        return proof_of_work

    def mine_block(self):
        proof_of_work = self.get_proof_of_work()
        last_block = get_last_blockchain_value(self.blockchain)

        mining_reward_transaction = OrderedDict([("sender", None), ("recepient", self.owner), ("amount", self.MINIG_REWARD)])
        self.outstanding_transactions.append(mining_reward_transaction)

        new_block = {
            "previous_hash": hash_block(last_block),
            "index": int(last_block["index"]) + 1,
            "transactions": self.outstanding_transactions,
            "nonce": proof_of_work
        }
        self.outstanding_transactions = []
        self.blockchain.append(new_block)
        write_to_file("blockchain", self.blockchain)
    
    def verify_transaction(self, transaction):
        sender_balance = self.get_balance(transaction["sender"])
        return sender_balance >= transaction["amount"]
    
    def verify_blockchain(self):
        for (index, block) in enumerate(self.blockchain):
            if index == 0:
                continue
            if block["previous_hash"] != hash_block(self.blockchain[index - 1]):
                return False
            if not validate_proof_of_work(block["previous_hash"], block["transactions"][:-1], block["nonce"], self.number_of_zeros):
                return False 
        return True

    def get_balance(self, participant):
        amount_sent = 0.0
        amount_received = 0.0
    
        for block in self.blockchain:
            for transaction in block["transactions"]:
                if transaction["sender"] == participant:
                    amount_sent += transaction["amount"]
                elif transaction["recepient"] == participant:
                    amount_received += transaction["amount"]
    
        for transaction in self.outstanding_transactions:
            if transaction["sender"] == participant:
                amount_sent += transaction["amount"]
    
        return float(amount_received - amount_sent)
    
    def print_participant_balance(self):
        for participant in self.participants:
            print(participant, self.get_balance(participant))
  
    def run(self):
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
                if self.add_transaction(recepient, amount=amount):
                    print("Transaction successful!")
                else:
                    print("Invalid transaction. Insufficient funds")
            elif user_choice == "2":
                self.mine_block()

                if not self.verify_blockchain():
                    print("Invalid blockchain!")
                    break
            elif user_choice == "3":
                print_blockchain_elements(self.blockchain)
            elif user_choice == "4":
                self.print_participant_balance()
            elif user_choice == "q":
                write_to_file("transactions", self.outstanding_transactions)
                break
        
        pprint.pprint(self.blockchain)

blockchian = Blockchain("Kaleb")
blockchian.run()