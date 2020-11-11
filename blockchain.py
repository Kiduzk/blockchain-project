from block import Block

class Blockchain:
    def __init__(self, blocks, transactions, id):
        self._blockchain = blocks
        self._transactions = transactions
        self._node_id = id
    
    def get_blocks(self):
        return self._blockchain
    
    def get_readable_blocks(self):
        blocks = self.get_blocks()
        changed_blocks = []
        for i in blocks:
            clone_block = Block(i.previous_hash, i.index, self.get_readable_transactions(i.transactions), i.nonce)    
            changed_blocks.append(vars(clone_block))
        
        return changed_blocks

    def get_transactions(self):
        return self._transactions
    
    def get_readable_transactions(self, optional_transactoin_pool=None):
        if not optional_transactoin_pool:
            transactions = self.get_transactions_only()
        else:
            transactions = optional_transactoin_pool

        changed_transactions = []
        for i in transactions:
            changed_transactions.append(str(i))
        
        return changed_transactions

    def get_transactions_only(self):
        ret = []
        for i in self._transactions:
            ret.append(i[0])

        return ret

    def get_node_id(self):
        return self._node_id
    
    def add_transaction(self, transaction):
        self._transactions.append(transaction)
        
    def empty_transactions(self):
        self._transactions = []
    
    def add_block(self, block):
        self._blockchain.append(block)

    def get_last_blockchain_value(self):
        if len(self.get_blocks()) < 1:
            return None
        return self.get_blocks()[-1]

    def print_blockchain_elements(self):
        for block in self.get_blocks():
            print("Outputting Block")
            print(block)