'''

mine.py

This file contains implementation of mining class


Author: Rajat Gupta
Email: rajat15101@iiitnr.edu.in
Time & Date: 23:27 hrs, Sat, 3rd March 2018


'''

from hashlib import sha256

class Mine(object):
    '''
    Mine class contains basic miner methods
    Miner object/node will discover transactions and select bunch of transcations. 
    After selecting bunch of transactions it will verify it and create block.
    Then it will add to it's own blockchaing and distribute it to network.
    2nd part of project
    '''

    def __init__(self):
        self.transctions = []
        
    def proof_of_work(self, current_hash):

        proof = 0
        while True:
            newhash = sha256(current_hash.encode() + str(proof).encode()).hexdigest()
            if newhash[:2] == "00":
                #DISTRIBUTE PROOF and add to chain and update it's chain
                return proof
        
        
       





