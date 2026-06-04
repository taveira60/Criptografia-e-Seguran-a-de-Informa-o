import os
import sys
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives import hashes, hmac,padding
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
class InvalidTag(Exception):
    pass


def calc_cbc(key, plaintext):

    iv = b'\x00' * 16

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    encryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
    ).encryptor()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return ciphertext[-16:]

def cbc_mac(argv):
    tipo = argv[1]
    key = argv[2]
    key=key.encode().zfill(32)
    file = argv[3]
    if len(argv) == 5:
        tag = argv[4]
    if tipo=="tag":
        with open(file,'rb') as f:
            ficheiro=f.read()
        tag = calc_cbc(key,ficheiro)
        with open(file+'.tag','wb') as f:
            f.write(tag)
        
    elif tipo == "verify":
        with open(file,'rb') as f:
            ficheiro = f.read()
        with open(file+'.tag','rb') as f:
            tag = f.read()
        tag_exp = calc_cbc(key,ficheiro)
        if tag == tag_exp :
            print("Tag Válida!")
        else:
            raise InvalidTag("Tag Inválida!")
    else :
        print("Erro")
    
        
        
        
if __name__ == "__main__":
    cbc_mac(sys.argv)