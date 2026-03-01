import struct, os ,sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def pbenc_chacha20(argv):
    tipo=argv[1]
    counter = 0
    if tipo=='enc':
        fich=argv[2]
        key=argv[3].encode().zfill(32)
        with open(fich,'rb') as f:
            mens=f.read()
            
        nonce = os.urandom(8)
        # with open('nonce','wb') as f: f.write(nonce)
        full_nonce = struct.pack("<Q", counter) + nonce
        algorithm = algorithms.ChaCha20(key, full_nonce)
        cipher = Cipher(algorithm, mode=None)
        encryptor = cipher.encryptor()
        ct = encryptor.update(mens) + encryptor.finalize()
        print(nonce)
        with open(fich+".enc",'wb') as fenc:
            fenc.write(nonce+ ct)
            # fenc.write(b'\n')
            # fenc.write(ct)
    elif tipo=='dec':
        fich=argv[2]
        key=argv[3].encode().zfill(32)
        with open(fich,'rb') as f:
            menscrip=f.read()
        nonce = menscrip[:8]     
        menscrip = menscrip[8:]      
        full_nonce = struct.pack("<Q", counter) + nonce
        algorithm = algorithms.ChaCha20(key, full_nonce)
        cipher = Cipher(algorithm, mode=None)
        decryptor = cipher.decryptor()
        dec = decryptor.update(menscrip) + decryptor.finalize()
        with open(fich+".dec",'wb') as fenc:
            fenc.write(dec)
    else:
        print('Erro')
    

if __name__ == "__main__":
    pbenc_chacha20(sys.argv)
