import random
from socket import *
import threading
import multiprocessing
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


MOD = int(1e9) + 7


def makeKey(n):
    ans = 1
    m = int(n)
    while m:
        if m&1:
            ans = (ans*n)%MOD
        n = (n*n)%MOD
        m >>= 1
    return ans


def pseudoRand(seed):
    temp = int(seed)
    ans = int(seed)
    x = (2<<31)-1
    while temp:
        if temp&1:
            ans = ((ans+1)^x)%x
        temp>>=1
    return ans


def decrypt(data, iv, s):
    k = (s.getsockname()[1])
    password = 'veryStrongPass'
    salt = b'\xc6\xea\x1e\xd8fQ\x8f\xbb\xfe1\xa3\x86\xe5\xefY^\xc0\x9e\xc1\xbd\r[\xfe\xe8 \x10/Z\xe14/g'
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    msg = unpad(cipher.decrypt(data), AES.block_size)
    return msg.decode()


# for single cleint

def client_start():
    s = socket()
    host = gethostname()
    port = 9992
    s.connect((host, port))
    no = str(random.randint(1, 4))
    s.send(no.encode())
    iv = s.recv(1024)
    data = s.recv(20000)
    if data != b'asahs':
        print(f'{decrypt(data, iv, s)} {s = }\n',end='')
    s.close()


pool = []
# creating multiple cleints
for _ in range(20):
    t1 = threading.Thread(target=client_start)
    t1.start()
    pool.append(t1)
