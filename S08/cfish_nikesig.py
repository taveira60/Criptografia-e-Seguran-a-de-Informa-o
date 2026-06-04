import sys,os
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.asymmetric import rsa,dh
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives import serialization, hashes

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

def cfish_nikesig(argv):
    type=argv[1]
    
    if type== "setup":
        
        #rsa
        user=argv[2]
        private_key=rsa.generate_private_key(public_exponent=65537, key_size=2048)
        publicy_key=private_key.public_key()
        
        with open(user+".rsask",'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
            
        with open(user+".rsapk",'wb') as f:
            f.write(publicy_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        
        #dh
        params_file = "parametros_dh.pem"
        if os.path.exists(params_file):
            with open(params_file, 'rb') as f:
                parameters = serialization.load_pem_parameters(f.read())
        else:
            parameters = dh.generate_parameters(generator=2, key_size=2048)
            with open(params_file, 'wb') as f:
                f.write(parameters.parameter_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.ParameterFormat.PKCS3
                ))
    
        dh_privatekey=parameters.generate_private_key()
        dh_publickey=dh_privatekey.public_key()
        
        dh_pub_bytes = dh_publickey.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        signature = private_key.sign(
            dh_pub_bytes,
            padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
       )
        
        with open(user+".dhsk",'wb') as f:
            f.write(dh_privatekey.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
            
        with open(user+".dhpk",'wb') as f:
            f.write(mkpair(dh_pub_bytes,signature))
        
    
    elif type=="enc":
        user=argv[2]
        me = argv[3]
        fich = argv[4]
        
        ##User Keys
        with open(user+".rsapk",'rb') as f:   
            public_key_rsa = load_pem_public_key(f.read())
            
        with open(user+".dhpk",'rb') as f:
            public_key_dh_bytes,signature = unpair(f.read())
            
        public_key_dh = load_pem_public_key(public_key_dh_bytes)
        
        try:
            public_key_rsa.verify(
                signature,
                public_key_dh_bytes,
                padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
            )
        except Exception as e:
            print(f"ERROR: Decryption or Verification failed! Reason: {e}")
            
        with open(me+".dhsk",'rb') as f:
            private_key_dh = load_pem_private_key(f.read(),None)
            
        with open(me+".rsask",'rb') as f:   
            private_key_rsa = load_pem_private_key(f.read(),None)
            
        shared_key = private_key_dh.exchange(public_key_dh)
            
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

        signature = private_key_rsa.sign(
            mens,
            padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
       )
        payload = mkpair(mens,signature)
        ciphertext = chacha.encrypt(nonce, payload, None)

        with open(fich+'.enc',"wb") as f:
            f.write(mkpair(nonce,ciphertext))
        

    elif type=="dec":
        user = argv[3]
        me = argv[2]
        fich = argv[4]
        with open(me+".rsask",'rb') as f:
            private_key = load_pem_private_key(f.read(),None)
            
        with open(user + ".rsapk", 'rb') as f:
            public_key_rsa = load_pem_public_key(f.read())
            
        with open(fich,"rb") as f:
            nonce,payload_cif = unpair(f.read())
        
        with open(me+".dhsk",'rb') as f:
            private_key_dh = load_pem_private_key(f.read(),None)
            
        with open(user+".dhpk",'rb') as f:
            public_key_dh_bytes,_ = unpair(f.read())
            
        public_key_dh = load_pem_public_key(public_key_dh_bytes)
            
        shared_key = private_key_dh.exchange(public_key_dh)
            
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)
        
        chacha = ChaCha20Poly1305(derived_key)
        payload = chacha.decrypt(nonce,payload_cif,None)
        message, sig = unpair(payload)
        public_key_rsa.verify(
            sig,
            message,  
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        with open(fich+".dec",'wb') as f:
            f.write(message)


    else:
        print("")
        
if __name__ == "__main__":
    cfish_nikesig(sys.argv)
