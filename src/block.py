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
       

    '''
    def __init__(self, time_stamp, prev_hash):
        
        self.time_stamp = time_stamp
        self.transactions = []
        self.prev_hash = prev_hash
        self.hashblock = None

    def get_hashblock(self):

        return sha256(str(self.prev_hash).encode() + str(self.time_stamp).encode() + str(self.transactions).encode())
  

    def add_transactions(self, transaction):
        if len(self.transactions) < 5:
            self.transactions.append(transaction)
            return 101
        if len(self.transactions) == 5:
            self.hashblock = self.get_hashblock()
        else:
            return 100




            
            

       
