'''

blockchain.py
Implementation of Blockchain and its methods

Author: Rajat Gupta
Email: rajat15101@iiitnr.edu.in
Time & Date: 17:32 hrs, Sat, 3trd March 2018

'''

import warnings

from pyp2p import *
#from transaction import *
from .block import Block
from datetime import datetime
from hashlib import sha256

class Blockchain(object):
    '''

    Chain of blocks will be blockchain.
    The object of this class stores individual block object of Block class. The longer the chain more authenticity.
    
    '''

    def __init__(self):
        '''
        Initialize our blockchain
        '''

        self.blocks = [self.initialize_genesis()]
        self.number_of_blocks = len(self.blocks)




    def return_last_block(self):
        '''
        Returns last block or latest block in our chain
        '''

        return self.blocks[self.number_of_blocks-1]



    def return_genesis_block(self):
        pass



    def initialize_genesis(self):
        '''
        First time block is added of our blockchain is initialized with genesis block
        '''
        block_ = Block(str(datetime.now()), sha256(str(datetime.now()).encode()))
        genesis_transcations = ['A', 'B', 'C', 'D', 'E']
        for i in range(5):
            if(block_.add_transactions(genesis_transcations[i])==101):
                print("Added transcation")
        return
        




    def lenght_of_chain(self):
        '''
        Returns chane lenght
        '''

        return self.number_of_blocks



    def add_block(self, block):
        self.blocks.append(block)
        self.number_of_blocks +=1
        return



    def print_block_chain(self):
        pass 