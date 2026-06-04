import struct, os ,sys
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 

def cfish_chacha20_poly(argv):
    tipo=argv[1]
    #data = b"a secret message"
    aad = b"authenticated but unencrypted data"
    if tipo=='setup':
        output=argv[2]
        key = ChaCha20Poly1305.generate_key()
        with open(output,'wb') as o:
            o.write(key)
    elif tipo=='enc':
        fich=argv[2]
        key=argv[3]
        with open(fich,'rb') as f:
            mens=f.read()
        with open(key,'rb') as f:
            chave=f.read()
        nonce = os.urandom(12) # Supostamente tem de ser 12 ao usar o Poly1305 ?????
        
        cipher = ChaCha20Poly1305(chave)

        ct = cipher.encrypt(nonce,mens, aad)
        
        with open(fich+".enc",'wb') as fenc:
            fenc.write(nonce)
            fenc.write(ct)
    elif tipo=='dec':
        fich=argv[2]
        key=argv[3]
        with open(fich,'rb') as f:
            menscrip=f.read()
        with open(key,'rb') as f:
            chave=f.read()
            
        nonce = menscrip[:12]
        ct = menscrip[12:]

        cipher = ChaCha20Poly1305(chave)

        dec = cipher.decrypt(nonce, ct, aad)

        with open(fich+".dec",'wb') as fenc:
            fenc.write(dec)
    else:
        print('Erro')

if __name__ == "__main__":
    cfish_chacha20_poly(sys.argv)
