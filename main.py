from src.blockchain import Blockchain
from src.transaction import Transaction
from src.block import Block
import sys
from datetime import datetime




chain = Blockchain()
def miner():
    '''
    Not correct way or technique to do mining iplementationm
    Just for test purpose. 

    Miners verify transactions, create block, and add to their blockchain
    '''
    l = []
    for i in range(1,11):

        trans = Transaction('Alice', 'Bob', i)
        l.append(trans)
        if i%5==0:

            blk = Block(str(datetime.now()), chain.return_last_block().get_hash())
            blk.add_transactions(l)
            chain.add_block(blk)
            l = []


miner()
chain.print_block_chain()
    

