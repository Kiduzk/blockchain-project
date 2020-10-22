import pickle

class FileHandler:
    def read_file(self, file_name):
        try:
            with open(file_name, "rb") as f:
                read = pickle.load(f)
            return read
        except FileNotFoundError:
            return False

    def write_to_file(self, file_name, data):
        with open(file_name, "wb") as f:
            pickle.dump(data, f)
        return True  

    def load_blockchain(self, gen_block):
        if not self.read_file("blockchain"):
            self.write_to_file("blockchain", [gen_block])
            return [gen_block]
        else:
            return self.read_file("blockchain")

    def load_participants(self, owner):
        if not self.read_file("participants"):
            self.write_to_file("participants", {owner})
            return {owner}
        else:
            return self.read_file("participants")

    def load_transactions(self):
        if not self.read_file("transactions"):
            self.write_to_file("transactions", [])
            return []
        else:
            return self.read_file("transactions")
