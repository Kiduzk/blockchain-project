import json
import file_storage as fs
from wallet import Wallet
from verification import Verification
from transactions import Transaction
from blockchain import Blockchain
from block import Block
from utility import hash_block, validate_proof_of_work
from flask import Flask, request

class Node:
    def __init__(self, owner):
        self.fileh = fs.FileHandler()
        self.MINING_REWARD = 10
        self.number_of_zeros = 2
        self.gen_block = Block(" ", 0, [], 0)
        self.wallet = Wallet()
        self.blockchain = Blockchain(self.fileh.load_blockchain_list(self.gen_block), self.fileh.load_transactions(), self.wallet.get_public_key())
        

    def mine_block(self):
        proof_of_work = self.get_proof_of_work()
        last_block = self.blockchain.get_last_blockchain_value()

        mining_reward_transaction = [Transaction(None, self.wallet.get_public_key(), self.MINING_REWARD), None]
        self.blockchain.add_transaction(mining_reward_transaction)

        for item in self.blockchain.get_transactions():
            transaction, sign = item
            if not Verification().verify_transaction(transaction, self.blockchain, sign):
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
        self.blockchain.add_transaction([transaction, signature])

    def get_transaction_details(self):
        recepient = input("Please enter recepient: ")
        amount = float(input("Enter transaction amount: "))
        return recepient, amount
    
    def get_proof_of_work(self):
        proof_of_work = 0
        while not validate_proof_of_work(hash_block(self.blockchain.get_last_blockchain_value()), self.blockchain.get_transactions(), proof_of_work, self.number_of_zeros):
            proof_of_work += 1

        return proof_of_work
    
    def run2(self):
        app = Flask(__name__)

        # Block
        @app.route("/mine_block", methods=["GET"])
        def _mine_block():
            if not self.mine_block():
                return json.dumps("There was invalid transaction in the blockchain")

            if not Verification().verify_blockchain(self.blockchain.get_blocks(), self.number_of_zeros):
                return json.dumps("Blockchain is not valid")
            
            return json.dumps("Block mined succesfully")    
        
        @app.route("/get_blocks", methods=["GET"])
        def _get_blockchain_elements():
            return json.dumps(self.blockchain.get_readable_blocks())

        # Transactions
        @app.route("/add_transaction", methods=["POST"])                 
        def _add_transaction():
            data = request.get_json()
            recepient, amount = data["recepient"], data["amount"]
            self.add_transaction(recepient, amount)
            return json.dumps("Transaction succesfully added!")
        
        @app.route("/get_transactions", methods=["GET"])
        def _get_transactions():
            return json.dumps(self.blockchain.get_readable_transactions())

        # Wallet
        @app.route("/my_address", methods=["GET"])
        def _get_public_key():
            return json.dumps(str(self.wallet.get_public_key()))
        
        @app.route("/my_balance", methods=["GET"])
        def _get_balance():
            return json.dumps(self.wallet.get_my_balance(self.blockchain))
        
        app.run()
        self.fileh.write_to_file("transactions", self.blockchain.get_transactions())

blockchian = Node("Kidus")
blockchian.run2()