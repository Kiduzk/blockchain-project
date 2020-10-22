class Transaction:
    def __init__(self, sender, recepient, amount):
        self.sender = sender
        self.recepient = recepient
        self.amount = amount

    def __repr__(self):
        return f"Sender: {self.sender}, recepient: {self.recepient}, amount: {self.amount}"   

