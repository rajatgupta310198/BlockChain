'''

mine.py

This file contains implementation of mining class


Author: Rajat Gupta
Email: rajat15101@iiitnr.edu.in
Time & Date: 23:27 hrs, Sat, 3rd March 2018


'''

from hashlib import sha256
import os, pickle
from .blockchain import Blockchain
from .block import Block

class Mine(object):
    '''
    Mine class contains basic miner methods
    Miner object/node will discover transactions and select bunch of transcations. 
    After selecting bunch of transactions it will verify it and create block.
    Then it will add to it's own blockchaing and distribute it to network.
    2nd part of project
    '''

    def __init__(self, name):
        self.transctions = []
        self.name = name
        self.filename = 'blockchain_' + str(self.name) + '.pkl'
        if self.check_block_exist():
            with open(self.filename, 'rb') as fp:
                self.chain = pickle.load(fp)
        
    def proof_of_work(self, current_hash):
        
        proof = 0
        while True:
            newhash = sha256(current_hash.encode() + str(proof).encode()).hexdigest()
            if newhash[:2] == "00":
                #DISTRIBUTE PROOF and add to chain and update it's chain
                return proof
            proof +=1

    def check_block_exist(self):
        print(os.getcwd())
        if self.filename in os.listdir():
            return True
        else:
            return False

    def savechain(self, chain):
        with open(self.filename, 'wb') as fp:
            pickle.dump(chain, fp)
            fp.close()
            self.chain = chain
    
    def getchain(self):
        return self.chain
    
    def printchain(self):
        with open(self.filename, 'rb') as fp:
            chain = pickle.load(fp)

            fp.close()
        print('Miners blockchain :')
        chain.print_block_chain()



        
       





