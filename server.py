import random
import socket
import time
from socket import *
import threading
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

d = {}

def send_to_group(con, addr):
    global d
    n = con.recv(1024).decode()
    print('Connected', addr, n)
    if n in d:
        d[n].append(con)
    else:
        d[n] = [con]


def multiCast(msg:str, target):
    global d
    print('Multicasting started')
    for conn in d[target]:
        salt = b'\xc6\xea\x1e\xd8fQ\x8f\xbb\xfe1\xa3\x86\xe5\xefY^\xc0\x9e\xc1\xbd\r[\xfe\xe8 \x10/Z\xe14/g'
        password = 'veryStrongPass'
        key = PBKDF2(password, salt, dkLen=32)
        cipher = AES.new(key, AES.MODE_CBC)
        enc = cipher.encrypt(pad(msg.encode(), AES.block_size))
        print(enc)
        iv = cipher.iv
        conn.send(iv)
        conn.send(enc)
    for i in d:
        if i!=target:
            for conn in d[i]:
                conn.send(b'sjhsd')
                conn.send(b'asahs')


def broardCast(msg:str):
    global d
    print('Bradcasting started')
    for target in d:
        for conn in d[target]:
            salt = b'\xc6\xea\x1e\xd8fQ\x8f\xbb\xfe1\xa3\x86\xe5\xefY^\xc0\x9e\xc1\xbd\r[\xfe\xe8 \x10/Z\xe14/g'
            password = 'veryStrongPass'
            key = PBKDF2(password, salt, dkLen=32)
            cipher = AES.new(key, AES.MODE_CBC)
            enc = cipher.encrypt(pad(msg.encode(), AES.block_size))
            print(enc)
            iv = cipher.iv
            conn.send(iv)
            conn.send(enc)


def close_all():
    global d
    for i in d:
        for conn in d[i]:
            conn.close()


flag = True
def setupServer():
    global flag
    s = socket()
    host = gethostname()
    port = 9992
    s.bind((host, port))
    s.listen()
    for _ in range(20):
        conn, addr = s.accept()
        send_to_group(conn, addr)
    flag = False


t1 = threading.Thread(target=setupServer, args=[])
t1.start()


# for synchronization
while flag:
    print('Waiting For Connections')
    time.sleep(1)


s = random.randint(1, 4)
multiCast(f'Multicast send to {str(s)}', str(s))
# broardCast(f'BoradCast send')
close_all()
