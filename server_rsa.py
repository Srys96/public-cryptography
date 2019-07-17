import socket
from Crypto.PublicKey import RSA
from Crypto import Random
import time

#Generate private and public keys
random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()

#Declartion
server = socket.socket()
host = socket.gethostbyname(socket.getfqdn())
port = 7777

if host == "127.0.1.1":
    import commands
    host = commands.getoutput("hostname -I")
print "host = " + host

#Prevent socket.error: [Errno 98] Address already in use
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((host, port))

server.listen(5)

c, addr = server.accept()

while True:
    
    message = "Hi, who is this?"
    client_string = c.recv(1024)
    #print (client_string)
    strip_client = client_string.strip().decode()
    clientpubkey = RSA.importKey(strip_client)
    cpk = clientpubkey.encrypt(message, 32)
    #print(cpk)
    c.send(str(cpk))
    publickeys = public_key.exportKey().decode()
    #print(public_key)
    #print ("")
    #print(publickeys)
    c.send(str(publickeys))
    msg = c.recv(1024)
    decrypt = private_key.decrypt(eval(msg))
    time.sleep(3)
    print("Encrypted message:", msg)
    print("Decrypted message:", decrypt)
    break
