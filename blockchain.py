import hashlib, json    #Used for encoding into JSON format, then hashing blocks with SHA-256.
from time import time   #Used for creating block timestamps.

class Blockchain:
    """A Blockchain class to create a Blockchain object. Used for storing blocks of data."""

    def __init__(self):
        """Instantiate an empty Blockchain object with empty chain and current_transactions lists."""
        self.chain = []                                                 #Set block list to empty.
        self.current_transactions = []                                  #Set transaction list to empty.

        self.new_block(previous_hash=1, proof=100)                      #Set origin block.

    def new_block(self, proof, previous_hash = None):
        """Creates a new block to append to the Blockchain object's chain.
        
        Arguments:
            proof <int> - Result of the proof of work algorithm defined in Blockchain class.
            previous_hash <str> - The SHA-256 hash of the preceding block in Blockchain object.

        Returns:
            block <dict> - the new block to be appended to the Blockchain object.
        """

        block = {
            "index" : len(self.chain) + 1,                              #New block will be appended to chain.
            "timestamp" : time(),                                       #Set time of creation for new block.
            "transactions" : self.current_transactions,                 #Extant transactions in Blockchain object.
            "proof" : proof,                                            #Proof of Work passed in via argument.
            "previous_hash" : previous_hash,                            #The SHA-256 hash of the preceding block.
        }

        self.current_transactions = []                                  #Reset transaction list to empty.
        self.chain.append(block)                                        #Append the block to the Blockchain object's chain list.

        return block                                                    #Return the created block.

    def new_transaction(self, sender, recipient, amount):
        """Adds a new transaction to the register.
      
        Arguments:
            sender <str> - address of the sender.
            recipient <str> - address of the recipient.
            amount <num> - the amount of the transaction.

        Returns:
            <int> - the index of the new transaction in the Blockchain object.
        """
        self.current_transactions.append({                              #Append transaction to Blockchain object:
            "sender" : sender,                                          #Add sender to dict.
            "recipient" : recipient,                                    #Add recipient to dict.
            "amount" : amount,                                          #Add value/amount to dict.
        })

        return self.last_block["index"] + 1                             #Return the index of the new block (old index + 1)


    def proof_of_work(self, last_proof):
        """Proof of work algorithm.
        
        Constantly checks if last_proof and proof combination is valid.
        Proof is incremented by 1 and checked each iteration.

        Arguments:
            last_proof <int> - the previous block's proof.
        
        Returns:
            proof <int> - the new proof once discovered.
        """
        proof = 0                                                   #Set initial proof to 0.

        while self.is_valid_proof(last_proof, proof) is False:      #Pass to is_valid_proof to check against last_proof.
            proof += 1                                              #Increment proof by 1, check again until combined proof hash is valid.
        
        return proof                                                #Return validated proof.


    @staticmethod
    def hash(block):
        """Hashes the given block with SHA-256.
        
        Arguments:
            block <dict> - The block to be hashed.

        Returns:
            <str> - The block hashed with SHA-256.
        """

        block_as_json_str = json.dumps(block, sort_keys = True).encode() #Encode block in JSON for consistent hashing.
            
        return hashlib.sha256(block_as_json_str).hexdigest()             #Return the SHA-256 encoded block.


    @staticmethod
    def is_valid_proof(last_proof, proof):
        """Determine if the proof is valid by checking against last proof.

        Method combines the values of last_proof and proof, encodes, and hashes them
        to determine if their first 4 characters are 0s. If so, the proof is valid.
        
        Arguments:
            last_proof <int> - the previous block's proof.
            proof <int> - the proposed proof.

        Returns:
            <bool> - True if hashed combination has 4 leading 0s. False otherwise.
        """

        encoded = f"{proof}{last_proof}".encode()                       #Encode combined proof.
        hashed =  hashlib.sha256(encoded).hexdigest()                   #Hash with SHA-256.
        return hashed[:4] == "0000"                                     #Return True/False if first 4 are 0s.


    @property
    def last_block(self):
        """Returns the last block in the Blockchain object."""
        return self.chain[-1]