import os
import sys
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives import hashes, hmac,padding
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

class InvalidTag(Exception):
    pass

def cbc_mac(key, plaintext):

    iv = os.urandom(16)

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    encryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
    ).encryptor()
    
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()


    return iv,ciphertext[:-16]

def cbc_mac_dec(iv,key, plaintext):

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    encryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
    ).encryptor()
    
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()


    return iv,ciphertext[:-16]

def cbc_mac_rnd(argv):
    tipo = argv[1]
    key = argv[2]
    key=key.encode().zfill(32)
    file = argv[3]
    if len(argv) == 5:
        tag = argv[4]
    iv = os.urandom(16)
    if tipo=="tag":
        with open(file,'rb') as f:
            ficheiro=f.read()
        tag = cbc_mac(key,ficheiro)
        print(tag)
        with open(file+'.tag','wb') as f:
            f.write(tag)
        
    elif tipo == "verify":
        with open(file,'rb') as f:
            ficheiro = f.read()
        with open(tag,'rb') as f:
            tag = f.read()
        iv = ficheiro[:16]
        tag_exp = cbc_mac_dec(iv,key,ficheiro)
        if tag == tag_exp :
            print("Tag Válida!")
        else:
            raise InvalidTag("Tag Inválida!")
    else :
        print("Erro")
    
        
        
        
if __name__ == "__main__":
    cbc_mac_rnd(sys.argv)