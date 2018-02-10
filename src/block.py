'''

block.py
Implementation of Class Block and its methods

Author: Rajat Gupta
Time & Date: 22:10 hrs, Sat, 10th Feb 2018
Email: rajat15101@iiitnr.edu.in

'''

from datetime import datetime
from hashlib import sha256
import warnings


class Block(object):
    '''

    Block class
    Contains all attributes and methods for Block
    data: This field is intended to be json/dictionary field containing custom data according to application
    In our case it will contain-
        -Voted to
        -Vote time
        (for voting application)

    '''
    def __init__(self, time_stamp, data, prev_hash):
        
        self.time_stamp = time_stamp
        self.data = data 
        self.prev_hash = prev_hash
        self.hash = self.hash_block()
        self.public_key = self.hash_block() # the key visible to all
        self.user_key = self.hash_block()   # key only visible to authenticated user who created block of transaction


    def hash_block(self):
        '''
        Hash current block
        perform SHA256 Hash of block
        '''
        hashed = sha256(str(self.time_stamp) + str(self.data) + str(self.prev_hash))

        return hashed

    def get_data_of_block(self, user_key):

        if user_key == self.user_key:
            '''
            Creater of this block
            '''

            return self.data
        else:
            return warnings.raise_invalid_user_key()
