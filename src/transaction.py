"""

Transaction Class

List of Transaction objects will be added to one Block.

Author: Rajat Gupta
Email: rajat15101@iiitnr.edu.in
Time & Date: 11:28 hrs, Sat, 3rd March 2018


"""
from datetime import datetime

class Transaction(object):
    ''''

    Transcation class will encompases single transaction in network by two client
    Client in our network are not miners/verfiers

    '''
    def __init__(self, to_, from_, qty=1):
        self.to_ = to_
        self.from_ = from_
        self.qty = qty
        self.timestamp = str(datetime.now())


    def __str__(self):

        return  str(self.from_) + ' ' + str(self.to_) + ' ' + str(self.qty) + ' '+ str(self.timestamp)


