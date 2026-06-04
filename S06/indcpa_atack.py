import struct, os 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from indcpa import Cipher_, INDCPA_Adv, IND_CPA
import random

class BadChaCha20(Cipher_):
    def keygen(self):
        return os.urandom(32)

    def enc(self, key: bytes, text: bytes):

        counter = 0
        nonce = b'\x00'*8 #porque o nonce tem de ser fixo  

        full_nonce = struct.pack("<Q", counter) + nonce

        algorithm = algorithms.ChaCha20(key, full_nonce)
        cipher = Cipher(algorithm, mode=None)

        encryptor = cipher.encryptor()

        ct = encryptor.update(text) + encryptor.finalize()

        return ct
    
    def dec(self, key: bytes, ciphertext: bytes):

        counter = 0
        nonce = b'\x00'*8 

        full_nonce = struct.pack("<Q", counter) + nonce

        algorithm = algorithms.ChaCha20(key, full_nonce)
        cipher = Cipher(algorithm, mode=None)

        decryptor = cipher.decryptor()

        return decryptor.update(ciphertext) + decryptor.finalize()
    

class Adversario_ChaCha20(INDCPA_Adv):

    def choose(self, oracle: callable):

        self.m0=b'taveira bay'
        self.m1=b'denis benis'


        msg_zeros = b'\x00' * len(self.m0)
        self.keystream = oracle(msg_zeros)

        return self.m0, self.m1


    def guess(self, oracle: callable, ciphertext: bytes):

        cifrado_m0 = bytes([a ^ b for a, b in zip(self.m0, self.keystream)])
        if ciphertext == cifrado_m0:
            return 0
        else:
            return 1

if __name__ == "__main__":

    C = BadChaCha20
    A = Adversario_ChaCha20

    count = 0
    total = 200

    for _ in range(total):
        if IND_CPA(C,A):
            count += 1

    print("Win rate:", count/total)
        