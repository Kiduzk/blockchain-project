import pickle
from hashlib import sha256

def validate_proof_of_work(prev_hash, outstanding_transactions, proof_of_work, number_of_zeros):
    return sha256((str(prev_hash) + str(outstanding_transactions) + str(proof_of_work)).encode()).hexdigest().startswith("0" * number_of_zeros)
 
def hash_block(block):
    return sha256(pickle.dumps(block)).hexdigest()