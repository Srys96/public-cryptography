import socket
from Crypto.PublicKey import RSA
from Crypto import Random
import time

random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()

client = socket.socket()
host = "172.20.10.6"
port = 7777

client.connect((host, port))

publickeys = public_key.exportKey().decode()
#print(public_key)
#print ("")
#print(publickeys)
client.send(str(publickeys))

msg = client.recv(1024)
decrypt = private_key.decrypt(eval(msg))
time.sleep(3)
print('Encrypted message:', msg)
print('Decrypted message:', decrypt)

message = "Hi, this is 001476253"
server_string = client.recv(1024)
#print (server_string)
strip_server = server_string.strip().decode()
serverpubkey = RSA.importKey(strip_server)
spk = serverpubkey.encrypt(message, 32)
#print(spk)
client.send(str(spk))

