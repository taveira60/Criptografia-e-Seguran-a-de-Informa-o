import sys
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

def mkpair(x, y):
   """ produz uma byte-string contendo o tuplo '(x,y)' ('x' e 'y' são byte-strings) """
   len_x = len(x)
   len_x_bytes = len_x.to_bytes(2, 'little')
   return len_x_bytes + x + y

def unpair(xy):
   """ extrai componentes de um par codificado com 'mkpair' """
   len_x = int.from_bytes(xy[:2], 'little')
   x = xy[2:len_x+2]
   y = xy[len_x+2:]
   return x, y

def cfish_nike(argv):
    op_type=argv[1]
    user=argv[2]
    if(len(argv)>3):
        fich=argv[3]
    
    if op_type=="setup":   
        
        if not os.path.exists("params.pem"):
            parameters = dh.generate_parameters(generator=2, key_size=2048)
            with open("params.pem", "wb") as f:
                f.write(parameters.parameter_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.ParameterFormat.PKCS3
                ))
        else:
            with open("params.pem", "rb") as f:
                parameters = serialization.load_pem_parameters(f.read())
        
        peer_private_key = parameters.generate_private_key()
        
        private_key = peer_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_key_aux = peer_private_key.public_key()
        
        public_key = public_key_aux.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        

        with open(user+".pk","wb") as f:
            f.write(public_key)
        
        with open(user+".sk","wb") as f:
            f.write(private_key)
            
    elif op_type== "enc":
        
        with open(user+".sk",'rb')as f:
            private_key = load_pem_private_key(f.read(),password = None)

        with open("bob"+".pk",'rb')as f:
            public_key= load_pem_public_key(f.read())     
       
        shared_key = private_key.exchange(public_key)
        
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)
        
        with open(fich,"rb") as f:
            mens=f.read()
            
        chacha = ChaCha20Poly1305(derived_key)
        nonce = os.urandom(12) 
        
        ciphertext = chacha.encrypt(nonce, mens, None)

        with open(fich + ".enc", "wb") as f:
            f.write(mkpair(nonce, ciphertext))
    
    elif op_type=="dec":
        with open(user+".pk",'rb')as f:
            public_key = load_pem_public_key(f.read())    
        
        with open("bob"+".sk",'rb')as f:
            private_key= load_pem_private_key(f.read(),password=None)
        
        with open(fich,'rb') as f:
            nonce,ciphered = unpair(f.read())
        
        shared_key = private_key.exchange(public_key)
        
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)
        
        chacha = ChaCha20Poly1305(derived_key)
        cleartext = chacha.decrypt(nonce, ciphered, None)

        with open(fich + ".dec", "wb") as f:
            f.write(cleartext)
    
    else:
        print("op_type non accepted")


# Só comes brolhos - nosso menino john 
if __name__ == "__main__":
    cfish_nike(sys.argv)
