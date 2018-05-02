'''

block.py
Implementation of Class Block and its methods

Author: Rajat Gupta
Email: rajat15101@iiitnr.edu.in
Time & Date: 22:10 hrs, Sat, 10th Feb 2018

'''

from datetime import datetime
from hashlib import sha256
import warnings


class Block(object):
    '''

    Block class
    Contains all attributes and methods for Block
    data: This field is intended to be list field containing custom data according to application
    A block is created by miner, in our implementation it is created directly via blockchain class for only genesis block.
    Genesis block is created when first time system is live.

    '''
    def __init__(self, time_stamp, prev_hash):
        
        self.time_stamp = time_stamp
        self.transactions = None
        self.block_number = None  # calculate when adding to block chain
        self.prev_hash = prev_hash
        self.hashblock = None
        self.proof_of_work = None # added after verification

    def get_hashblock(self):

        return sha256(str(self.prev_hash).encode() + str(self.time_stamp).encode() + str(self.transactions).encode()).hexdigest()
  

    def add_transactions(self, transaction):
        
        self.transactions = transaction
            #print("Added transcation", len(self.transactions))
            
        
            #print('5th transaction added and ready to be added in blockchain')
        self.hashblock = self.get_hashblock()
        #call proof of work algorithm 
        return 101
       

    def get_hash(self):
        return self.hashblock

    def get_transactions(self):

        return self.transactions




            
            

       
