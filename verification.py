from utility import hash_block, validate_proof_of_work

class Verification:

    def get_balance(self, participant, blockchain, outstanding_transactions):
        amount_sent = 0.0
        amount_received = 0.0

        for block in blockchain:
            for transaction in block.transactions:
                if transaction.sender == participant:
                    amount_sent += transaction.amount
                elif transaction.recepient == participant:
                    amount_received += transaction.amount

        for transaction in outstanding_transactions:
            if transaction.sender == participant:
                amount_sent += transaction.amount

        return float(amount_received - amount_sent)

    def verify_transaction(self, transaction, blockchain, outstanding_transactions):
        sender_balance = self.get_balance(transaction.sender, blockchain, outstanding_transactions)
        return sender_balance >= transaction.amount
    
    def verify_blockchain(self, blockchain, number_of_zeros):
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash!= hash_block(blockchain[index - 1]):
                return False
            if not validate_proof_of_work(block.previous_hash, block.transactions[:-1], block.nonce, number_of_zeros):
                return False 
        return True
