import struct, os ,sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def cfish_chacha20(argv):
    tipo=argv[1]
    counter = 0
    if tipo=='setup':
        output=argv[2]
        key = os.urandom(32)
        with open(output,'wb') as o:
            o.write(key)
    elif tipo=='enc':
        fich=argv[2]
        key=argv[3]
        with open(fich,'rb') as f:
            mens=f.read()
        with open(key,'rb') as f:
            chave=f.read()
            
        nonce = os.urandom(8)
        # with open('nonce','wb') as f:
        #     f.write(nonce)
        full_nonce = struct.pack("<Q", counter) + nonce
        algorithm = algorithms.ChaCha20(chave, full_nonce)
        cipher = Cipher(algorithm, mode=None)
        encryptor = cipher.encryptor()
        ct = encryptor.update(mens) + encryptor.finalize()
        
        with open(fich+".enc",'wb') as fenc:
            fenc.write(ct)
            fenc.write(b'\n')
            fenc.write(nonce)
    elif tipo=='dec':
        fich=argv[2]
        key=argv[3]
        with open(fich,'rb') as f:
            menscrip=f.read()
        with open(key,'rb') as f:
            chave=f.read()
            
        menscrip, nonce = menscrip.split(b'\n')
        # with open('nonce','rb') as f:
        #     nonce = f.read()    
        full_nonce = struct.pack("<Q", counter) + nonce
        algorithm = algorithms.ChaCha20(chave, full_nonce)
        cipher = Cipher(algorithm, mode=None)
        decryptor = cipher.decryptor()
        dec = decryptor.update(menscrip) + decryptor.finalize()
        with open(fich+".dec",'wb') as fenc:
            fenc.write(dec)
    else:
        print('Erro')
    

if __name__ == "__main__":
    cfish_chacha20(sys.argv)
