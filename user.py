import json
import file_storage as fs
from verification import Verification
from transactions import Transaction
from blockchain import Blockchain
from block import Block
from utility import *

from collections import OrderedDict

class User:
    def __init__(self, owner):
        self.fileh = fs.FileHandler()
        self.MINING_REWARD = 10
        self.number_of_zeros = 2
        self.gen_block = Block(" ", 0, [], 0)
        self.blockchain = self.fileh.load_blockchain(self.gen_block)
        self.outstanding_transactions = self.fileh.load_transactions()
        self.owner = owner
        self.participants = self.fileh.load_participants(owner)
    
    def mine_block(self):
        proof_of_work = self.get_proof_of_work()
        last_block = Blockchain().get_last_blockchain_value(self.blockchain)

        mining_reward_transaction = Transaction(None, self.owner, self.MINING_REWARD)
        self.outstanding_transactions.append(mining_reward_transaction)

        new_block = Block(
            hash_block(last_block),
            int(last_block.index) + 1,
            self.outstanding_transactions,
            proof_of_work
        )

        self.outstanding_transactions = []
        self.blockchain.append(new_block)
        self.fileh.write_to_file("blockchain", self.blockchain)
    
   
    def print_participant_balance(self):
        for participant in self.participants:
            print(participant, Verification().get_balance(participant, self.blockchain, self.outstanding_transactions))
    
    def get_user_choice(self):
        return input("Your choice: ")
 
    def add_transaction(self, recepient, amount=1.0):
        sender = self.owner
        transaction = Transaction(sender, recepient, amount)

        if Verification().verify_transaction(transaction, self.blockchain, self.outstanding_transactions):
            self.outstanding_transactions.append(transaction)
            self.participants.add(sender)
            self.participants.add(recepient)
            self.fileh.write_to_file("participants", self.participants)
            return True
        return False

    def get_transaction_details(self):
        recepient = input("Please enter recepient: ")
        amount = float(input("Enter transaction amount: "))
        return recepient, amount
    
    def get_proof_of_work(self):
        proof_of_work = 0
        while not validate_proof_of_work(hash_block(Blockchain().get_last_blockchain_value(self.blockchain)), self.outstanding_transactions, proof_of_work, self.number_of_zeros):
            proof_of_work += 1

        return proof_of_work

    def run(self):
        while True:
            print("Hello, please choose: ")
            print("1: Add a new transaction")
            print("2: Mine a new block")
            print("3: Output the blockchain blocks")
            print("4: Output the participant balance")
            print("q: Quit")
            user_choice = self.get_user_choice()
        
            if user_choice == "1":
                tx_details = self.get_transaction_details()
                recepient, amount = tx_details
                if self.add_transaction(recepient, amount=amount):
                    print("Transaction successful!")
                else:
                    print("Invalid transaction. Insufficient funds")
            elif user_choice == "2":
                self.mine_block()

                if not Verification().verify_blockchain(self.blockchain, self.number_of_zeros):
                    print("Invalid blockchain!")
                    break
            elif user_choice == "3":
                Blockchain().print_blockchain_elements(self.blockchain)
            elif user_choice == "4":
                self.print_participant_balance()
            elif user_choice == "q":
                self.fileh.write_to_file("transactions", self.outstanding_transactions)
                break
        
        print(self.blockchain)

blockchian = User("Kidus")
blockchian.run()