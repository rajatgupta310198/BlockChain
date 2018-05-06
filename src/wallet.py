#client/peers for voting
import socket, os, sys
from .block import Block
from hashlib import sha256
from .transaction import Transaction
import time, pickle


public_list_of_peers = [
    ["172.16.122.241", 10009, "active"]
]
class User:
    def __init__(self, name, age, publickey, privatekey, candidate=False):
        self.name = name 
        self.age = age
        self.candidate = candidate
        self.publickey = publickey
        self.privatekey = privatekey



def register(sock):
    global public_list_of_peers
    name = input("Enter Name")
    age = input("Enter age")
    if int(age)>17:
        user = User(name, age, sha256(name.encode() + str(age).encode()).hexdigest(), sha256(name.encode() + str(age).encode()).hexdigest(), candidate=False)
        to = input("Enter digital signature of candidate you wanna vote :")
        

        new_Transaction = Transaction(to, user.publickey)
        print(user.publickey)
        new_Transaction.timestamp = time.ctime()
        new_Transaction.digital_signature = sha256(to.encode() + user.privatekey.encode()).hexdigest()
        print(new_Transaction,'Digital Signature : ', new_Transaction.digital_signature)
        return new_Transaction

    else:
        sock.close()
        return False

        
def connectToNetwork(connections):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.connect(('172.16.122.241', 10009))
    sock.send('wallet'.encode()) 
    trans = register(sock)
    print(trans)
    if trans:
        data = sock.recv(1024)
        public_list_of_peers = pickle.loads(data)
        print(public_list_of_peers)
        sock.send(pickle.dumps(trans))
        sock.close()

    


#connectToNetwork()
    
        

#register()
