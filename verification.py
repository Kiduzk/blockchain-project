from utility import encode_object, validate_proof_of_work, hash_block
from hashlib import sha256

class Verification:

    def get_balance(self, participant, blockchain, outstanding_transactions):
        amount_sent = 0.0
        amount_received = 0.0

        for block in blockchain:
            for transaction in block.transactions:
                if transaction[0].sender == participant:
                    amount_sent += transaction[0].amount
                elif transaction[0].recepient == participant:
                    amount_received += transaction[0].amount

        return float(amount_received - amount_sent)

    def verify_transaction(self, transaction, blockchain, outstanding_transactions, signature):
        public_key = transaction.sender
        if transaction.sender:
            sender_balance = self.get_balance(transaction.sender, blockchain, outstanding_transactions)
            if not sender_balance >= transaction.amount:
                return False
            
            transaction = encode_object(transaction)
            hashed = int.from_bytes(sha256(transaction).digest(), byteorder="big")

            verifiaction = pow(signature, public_key.e, public_key.n)
            return verifiaction == hashed
        else:
            return True
        
    
    def verify_blockchain(self, blockchain, number_of_zeros):
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not validate_proof_of_work(block.previous_hash, block.transactions[:-1], block.nonce, number_of_zeros):
                return False 
        return True
    