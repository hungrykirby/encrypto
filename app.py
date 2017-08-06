import base64
from Crypto import Random
from Crypto.Cipher import AES

import string, random

class AESCipher(object):
    def __init__(self, key, block_size=32):
        self.bs = block_size
        if len(key) >= len(str(block_size)):
            self.key = key[:block_size]
        else:
            self.key = self._pad(key)

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

def writeEncrypted(inputtext, filename, key):
    cipher = AESCipher(key)
    encryptedtxt = cipher.encrypt(inputtext)
    f = open(filename, 'w')
    f.write(str(encryptedtxt).split("\'")[1])
    f.close()

def openDecypt(filename, key):
    cipher = AESCipher(key)
    f = open(filename)
    data = f.read()
    f.close()
    print(cipher.decrypt(data.encode('utf-8')))


if __name__ == '__main__':
    key = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(50)])
    print(key)
    writeEncrypted("hogehuga", "hogehuga.txt", key)
    openDecypt("hogehuga.txt", key)
