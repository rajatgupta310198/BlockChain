from src.blockchain import Blockchain
from src.transaction import Transaction
from src.block import Block
import sys, pickle, os, threading
from datetime import datetime
import socket
from src.mine import Mine
from src.wallet import *
# 100 ask miner if he has blockchain
# 102 miner respond yes to 100
# 101 miner responds no to 101



public_list_of_peers = [
    ("0.0.0.0", 10009, "active")
]

def main():
    path = os.getcwd()
    try:
        print('trying to read')
        os.chdir(path + '/blk')
        with open('blkchain.pkl', 'rb') as fp:
            chain = pickle.load(fp)
            fp.close()
    
    except:
        print('Creating genesis')
        chain = Blockchain()
        os.mkdir('blk')
        os.chdir(path + '/blk')
        with open('blkchain.pkl', 'wb') as fp:
            pickle.dump(chain, fp)
            fp.close()

    return chain


def save(chain):
    with open('blkchain.pkl', 'wb') as fp:
        pickle.dump(chain, fp)
        fp.close()


def handle_and_distribute(c, a, chain):
    print('Handle')
    while True:
        data = c.recv(1024)
        if data.decode() == 'miner':
            c.send('100'.encode())
        if data.decode() == '102':
            '''
            Do nothing
            '''
        if data.decode() == '101':
            file_to_transfer = pickle.dumps(chain)
            c.send(file_to_transfer)
        
        if not data:
            print(a[0], 'N')
            c.close()
        if data.decode() =='wallet':
            file_to_send = pickle.dumps(public_list_of_peers)
            c.send(file_to_send)
        #    for i,connections  in enumerate(public_list_of_peers):
        #         if connections[0] == a[0]
        #             public_list_of_peers[i][2] =="offline"
        #             c.close()
        #             break
        #     print(public_list_of_peers)
            
            #then distribute public list of peers to others




#print(sys.argv)

def checkif_blockchain_exist():
    if 'blkm' in os.listdir():
        return True
    else:
        return False


if __name__ =="__main__":
    print(sys.argv)
    if sys.argv[1] =='init':
        '''
        Initialize blockchain
        Setup network
        Look for peers
        '''
        chain = main()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.bind(('0.0.0.0', 10009))
        sock.listen(1)
        while True:
            c, a = sock.accept()
            public_list_of_peers.append((a[0], a[1], "Active"))
            print("Got a peer ", a[0] + ':' + str(a[1]))
            cThread = threading.Thread(target=handle_and_distribute, args=(c, a, chain))
            cThread.daemon = True
            cThread.start()
            print(public_list_of_peers)


    if sys.argv[1] == 'mine':
        '''
        start miner
        download blockchain
        take transactions from file
        mine a block
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.connect((public_list_of_peers[0][0], public_list_of_peers[0][1]))
        sock.send("miner".encode())
        while True:
            data_ = sock.recv(1024)
            try:
                if data_.decode() == '100':
                    if checkif_blockchain_exist():
                        print('Exist')
                        sock.send('102'.encode())
                    else:
                        print('Not exist')
                        sock.send('101'.encode())

            
                print(data_.decode())
            except:
                chain = pickle.loads(data_)
                chain.print_block_chain()

    if sys.argv[1] == 'wallet':
        connectToNetwork()
            

                





# chain = Blockchain()
# def miner():
#     '''
#     Not correct way or technique to do mining iplementationm
#     Just for test purpose. 

#     Miners verify transactions, create block, and add to their blockchain
#     '''
#     l = []
#     for i in range(1,11):

#         trans = Transaction('Alice', 'Bob', i)
#         l.append(trans)
#         if i%5==0:

#             blk = Block(str(datetime.now()), chain.return_last_block().get_hash())
#             blk.add_transactions(l)
#             chain.add_block(blk)
#             l = []


# miner()
# chain.print_block_chain()


