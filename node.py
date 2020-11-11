import json
import uuid
import file_storage as fs
from wallet import Wallet
from verification import Verification
from transactions import Transaction
from blockchain import Blockchain
from block import Block
from utility import hash_block, validate_proof_of_work


class Node:
    def __init__(self, owner):
        self.fileh = fs.FileHandler()
        self.MINING_REWARD = 10
        self.number_of_zeros = 2
        self.gen_block = Block(" ", 0, [], 0)
        self.blockchain = Blockchain(self.fileh.load_blockchain_list(self.gen_block), self.fileh.load_transactions(), self.fileh.load_id(uuid.uuid4()))
        self.wallet = Wallet()

    def mine_block(self):
        proof_of_work = self.get_proof_of_work()
        last_block = self.blockchain.get_last_blockchain_value()

        mining_reward_transaction = [Transaction(None, self.wallet.get_public_key(), self.MINING_REWARD), None]
        self.blockchain.add_transaction(mining_reward_transaction)

        for item in self.blockchain.get_transactions():
            transaction, sign = item
            if not Verification().verify_transaction(transaction, self.blockchain.get_blocks(), self.blockchain.get_transactions_only(), sign):
                return False

        new_block = Block(
            hash_block(last_block),
            int(last_block.index) + 1,
            self.blockchain.get_transactions(),
            proof_of_work
        )

        self.blockchain.empty_transactions()
        self.blockchain.add_block(new_block)
        self.fileh.write_to_file("blockchain", self.blockchain.get_blocks())

        return True
    
    def get_user_choice(self):
        return input("Your choice: ")
 
    def add_transaction(self, recepient, amount):
        sender = self.wallet.get_public_key()
        transaction = Transaction(sender, recepient, amount)
        signature = self.wallet.sign_transaction(transaction)
        self.blockchain.add_transaction([transaction, signature, self.wallet.get_public_key()])

    def get_transaction_details(self):
        recepient = input("Please enter recepient: ")
        amount = float(input("Enter transaction amount: "))
        return recepient, amount
    
    def get_proof_of_work(self):
        proof_of_work = 0
        while not validate_proof_of_work(hash_block(self.blockchain.get_last_blockchain_value()), self.blockchain.get_transactions(), proof_of_work, self.number_of_zeros):
            proof_of_work += 1

        return proof_of_work

    def run(self):
        while True:
            print("Hello, please choose: ")
            print("1: Add a new transaction")
            print("2: Mine a new block")
            print("3: Output the blockchain blocks")
            print("q: Quit")
            user_choice = self.get_user_choice()
        
            if user_choice == "1":
                tx_details = self.get_transaction_details()
                recepient, amount = tx_details
                self.add_transaction(recepient, amount)
                print("Transaction added")
            elif user_choice == "2":
                if not self.mine_block():
                    print("There was invalid transaction/s in blockchain")
                    break

                if not Verification().verify_blockchain(self.blockchain.get_blocks(), self.number_of_zeros):
                    print("Invalid blockchain!", self.blockchain.get_blocks())
                    break
                print("Block mined succesfully!")
            elif user_choice == "3":
                self.blockchain.print_blockchain_elements()
            elif user_choice == "q":
                self.fileh.write_to_file("transactions", self.blockchain.get_transactions())
                break

blockchian = Node("Kidus")
blockchian.run()