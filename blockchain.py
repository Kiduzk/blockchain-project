class Blockchain:
    
    def get_last_blockchain_value(self, blockchain):
        if len(blockchain) < 1:
            return None
        return blockchain[-1]

    def print_blockchain_elements(self, blockchain):
        for block in blockchain:
            print("Outputting Block")
            print(block)
 