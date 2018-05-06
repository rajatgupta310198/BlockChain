from src.blockchain import Blockchain
from src.transaction import Transaction
from src.block import Block
import sys, pickle, os, threading, signal
from datetime import datetime
import socket
from src.mine import *
from src.wallet import *

# 100 ask miner if he has blockchain
# 102 miner respond yes to 100
# 101 miner responds no to 101

data_dir = '/blk'

public_list_of_peers = [
    ["172.16.122.241", 10009, "active"]
]
connections = []
connection_miners = []
list_of_transactions = []
chains =[]

def handle_multiple_chains():
    while True:
        if len(chains) > 0:
            time.sleep(1)
            print(len(chains))
            chains_time_Stamps = {

            }
            time_stapms = []
            print('Priting each chain >')
            for i,chain in enumerate(chains):
                time_stapms.append(chain.return_last_block().get_time_of_creation())
                chains_time_Stamps[chain.return_last_block().get_time_of_creation()] = chain
            time_stapms.sort()
            print('Selected chain:', chains_time_Stamps[time_stapms[0]].print_block_chain())
            chain = chains_time_Stamps[time_stapms[0]]
            print(chain.print_block_chain())
            save(chain)
            chains.clear()
            broadcast_new_blockchain(connection_miners, chain)

    
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

    


def save(chain):
    with open('blkchain.pkl', 'wb') as fp:
        pickle.dump(chain, fp)
        fp.close()
    


def broadcast_peers(public_list_of_peers):
    for connection in connections:
        connection.send('upp'.encode())
        connection.send(pickle.dumps(public_list_of_peers))
    sys.exit(0)

def broadcast_new_blockchain(connection_miners, chain):
    for c_miner in connection_miners:
        c_miner.send(pickle.dumps(chain))


def handle_wallet(c, a):
    global list_of_transactions
    print('Receving transaction...')
    data = c.recv(102400)
    
    list_of_transactions.append(pickle.loads(data))
    if len(list_of_transactions) >2:
        send_to_miners()
        list_of_transactions = []
    connections.remove(c)
    print(list_of_transactions)
    c.close()
    sys.exit()
        

def send_to_miners():
    print('called')
    for miner in connection_miners:
        miner.send(pickle.dumps(list_of_transactions))


def handle_and_distribute(c, a, chain):
    print('Handle')
    isWallet = False
    while True:
        data = c.recv(10240)
        try:

            if data.decode() == 'miner':
                connection_miners.append(c)
                c.send('100'.encode())
            elif data.decode() == '102':
                '''
                Do nothing
                '''
            elif data.decode() == '101':
                file_to_transfer = pickle.dumps(chain)
                c.send(file_to_transfer)
                

            elif data.decode() =='wallet':
                file_to_send = pickle.dumps(public_list_of_peers)
                c.send(file_to_send)
                isWallet = True
                #print('Receving transaction...')
                handle_wallet(c, a)
                break


            
            if not data and isWallet == False:
                connections.remove(c)
                c.close()
                for i, connection in enumerate(public_list_of_peers):
                    if connection[0] == a[0] and connection[1] == a[1]:
                        public_list_of_peers.pop(i)
                        broadcast_peers(public_list_of_peers)
        
        except OSError:

            sys.exit()
        
        except:
            try:
                obj = pickle.loads(data)
                if type(obj).__name__ == 'Blockchain':
                    # received new chain
                    print('Neighbor chain appended')
                    chains.append(obj)
                    
            except:
                print('Cannot read')
                

def checkif_blockchain_exist():
    if 'blkm' in os.listdir():
        return True
    else:
        return False

def read_from_local():
    with open('blkchain.pkl', 'rb') as fp:
        chain = pickle.load(fp)
        fp.close()
    
    return chain

if __name__ =="__main__":
    print(sys.argv)
    main()
    if sys.argv[1] =='init':
        '''
        Initialize blockchain
        Setup network
        Look for peers
        '''
        
        multipleChainsThread = threading.Thread(target=handle_multiple_chains)
        multipleChainsThread.daemon = True
        multipleChainsThread.start()
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.bind(('0.0.0.0', 10009))
        sock.listen(1)
        while True:
            try:
                print('Listening for peers')
                c, a = sock.accept()
                connections.append(c)
                chain = read_from_local()
                public_list_of_peers.append([a[0], a[1], "Active"])
                print("Got a peer ", a[0] + ':' + str(a[1]))
                #print(chain.print_block_chain())
                cThread = threading.Thread(target=handle_and_distribute, args=(c, a, chain))
                cThread.daemon = False
                cThread.start()
                print('Neighbor chains :', chains)
                #print('Thread terminated', cThread.name)
                #print(public_list_of_peers)
            except KeyboardInterrupt:
                sys.exit(0)



    if sys.argv[1] == 'mine':
        '''
        start miner
        download blockchain
        take transactions from file
        mine a block
        '''
        miner = Mine(name=socket.gethostname())

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.connect((public_list_of_peers[0][0], public_list_of_peers[0][1]))
        sock.send("miner".encode())
        peersr = False
        while True:
            
            data_ = sock.recv(512000)
            try:
                 
                if peersr!=True:
                    if data_.decode() == 'upp':
                            peersr = True
                            print('Next we will receive peers')
                            
                    else:
                        if data_.decode() == '100':
                            if miner.check_block_exist():
                                print('Exist')
                                sock.send('102'.encode())
                                
                            else:
                                print('Not exist')
                                sock.send('101'.encode())
    
                else:
                    print('Receiving peers  updated')
                    public_list_of_peers = pickle.loads(data_)
                    print(public_list_of_peers)
                    peersr = False

            except: 
                obj = pickle.loads(data_)
                print(type(obj).__name__)
                if type(obj).__name__ == 'Blockchain':
                    chain = obj
                    miner.savechain(chain)
                    miner.printchain()
                if type(obj) == list:
                    blk = Block(time.time(), miner.getchain().return_last_block().get_hash())
                    blk.add_transactions(obj)
                    blk.hashblock = blk.get_hashblock()
                    print('Mining block')
                    chain = miner.getchain()
                    proof = miner.proof_of_work(blk.get_hash())
                    blk.proof_of_work = proof
                    blk.miner = socket.gethostname()
                    print(proof)
                    chain.add_block(blk)
                    print(chain.print_block_chain())
                    print(type(chain).__name__)
                    sock.send(pickle.dumps(chain))

                #chain.print_block_chain()

                
    if sys.argv[1] == 'wallet':
        connectToNetwork(connections)

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


