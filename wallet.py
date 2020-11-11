import rsa
from file_storage import FileHandler
from utility import encode_object
from hashlib import sha256, sha512

class Wallet:
    def __init__(self):
        fileh = FileHandler()
        if fileh.read_file("wallet"):
            self._public, self._private = fileh.read_file("wallet")
        else:
            self._public, self._private = rsa.newkeys(1024)
            fileh.write_to_file("wallet", (self._public, self._private))

    def get_public_key(self):
        return self._public
    
    def sign_transaction(self, transaction):
        transaction = encode_object(transaction)
        hashed = int.from_bytes(sha256(transaction).digest(), byteorder="big")
        sign = pow(hashed, self._private.d, self._public.n)
        return sign
    