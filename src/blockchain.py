'''

blockchain.py
Implementation of Blockchain and its methods

Author: Rajat Gupta
Email: rajat15101@iiitnr.edu.in
Time & Date: 17:32 hrs, Sat, 3trd March 2018

'''

import warnings

#from pyp2p import *
from .transaction import *
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
        '''
        Return genesis block object
        '''
        return self.blocks[0]


    #@staticmethod
    def initialize_genesis(self):
        '''
        First time block is added of our blockchain is initialized with genesis block
        '''
        block_ = Block(str(datetime.now()), sha256(str(datetime.now()).encode()).hexdigest())
        genesis_transcations = ['A', 'B', 'C', 'D', 'E'] # Original trancations will be different
        block_.add_transactions(genesis_transcations)
        block_.hashblock = block_.get_hashblock()
        return block_
        

    def is_voted(self, trans):
        print('called')
        
        for i,block in enumerate(self.blocks):
            if i!=0:
                trans_ = block.get_transactions()
                for t in trans_:
                    print(t)
                    if t.get_who() == trans.get_who():
                        return True
        return False



    def lenght_of_chain(self):
        '''
        Returns chane lenght
        '''

        return self.number_of_blocks



    def add_block(self, block):
        '''

        This fucntion will be called when miner successfully verfies a block.

        '''

        self.blocks.append(block)
        self.number_of_blocks +=1
        #save chain after this locally and then distribute block
        return



    def print_block_chain(self):
        print('Blochain printing\n')
        for i in range(self.number_of_blocks):
            print('Block Number:', i)
            print(self.blocks[i].get_hash())
            print('Miner of this block :', self.blocks[i].get_miner())
            l = self.blocks[i].get_transactions()
            print('Transactions :\n')
            print('To,Digital Signature\n')
            for t in l:
                print(t)
        