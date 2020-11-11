class Block:
    def __init__(self, previous_hash, index, transactions, nonce):
        self.previous_hash = previous_hash
        self.index = index
        self.transactions = transactions
        self.nonce = nonce

    def __repr__(self):
        return f"Previous hash: {self.previous_hash}; Index: {self.index}; Transactions: {self.transactions}; Nonce: {self.nonce}"

  
