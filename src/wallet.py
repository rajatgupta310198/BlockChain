#client/peers for voting
import socket, os, sys
from .block import Block
from hashlib import sha256
from .transaction import Transaction
import time, pickle


public_list_of_peers = [
    ["172.16.102.38", 10009, "active"]
]
class User:
    def __init__(self, name, age, publickey, privatekey, candidate=False):
        self.name = name 
        self.age = age
        self.candidate = candidate
        self.publickey = publickey
        self.privatekey = privatekey



def register(sock, ca):
    global public_list_of_peers
    name = input("Enter Name")
    age = input("Enter age")
    if int(age)>17:
        user = User(name, age, sha256(name.encode() + str(age).encode()).hexdigest(), sha256(name.encode() + str(age).encode()).hexdigest(), candidate=False)
        choice = int(input("Enter choice :"))
        

        new_Transaction = Transaction(ca[choice][0], user.publickey, name=ca[choice][1])
        print(user.publickey)
        new_Transaction.timestamp = time.ctime()
        print(ca[choice])
        new_Transaction.digital_signature = sha256(ca[choice][0].encode() + user.privatekey.encode()).hexdigest()
        print(new_Transaction,'Digital Signature : ', new_Transaction.digital_signature)
        return new_Transaction

    else:
        sock.close()
        return False

        
def connectToNetwork(connections):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.connect(('172.16.102.38', 10009))
    sock.send('wallet'.encode()) 
    
    
    data = sock.recv(10240)
    chain = pickle.loads(data)
    print(type(chain).__name__)
    print('\nCandidates -\n')
    blk = chain.return_genesis_block()
    t = blk.get_transactions()
    ca = {

    }
    for i,tt in enumerate(t):
        ca[i] = [tt.get_add(), tt.get_candidate()]
        
        print('Name :', tt.get_candidate(), 'Address : ', tt.get_add(), 'Option :', i)
    trans = register(sock, ca)
    print(trans)
    sock.send(pickle.dumps(trans))
    sock.close()

    


#connectToNetwork()
    
        

#register()