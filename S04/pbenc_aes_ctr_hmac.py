import os
import sys
from cryptography.hazmat.primitives.ciphers.modes import CTR
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac


def pbenc_aes_ctr_hmac_hmac(argv):
    tipo = argv[1]
    fich = argv[2]
    passfrase = " ".join(argv[3:]) 
    passfrase = passfrase.encode().zfill(32)
    if tipo == 'enc':
        with open(fich, 'rb') as f:
            ficheiro = f.read()
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(passfrase), modes.CTR(iv))
        encryptor = cipher.encryptor()
        
        ct = encryptor.update(ficheiro) + encryptor.finalize()
        h = hmac.HMAC(passfrase, hashes.SHA256())
        h.update(ct)
        signature = h.finalize()
        print(f"Actual MAC length: {len(signature)}")
        with open(fich+".enc", 'wb') as f:
            ficheiro = f.write(iv)
            ficheiro = f.write(signature)
            ficheiro = f.write(ct)
            

    elif tipo == 'dec':
        with open(fich,'rb') as f:
            textocif = f.read()
        iv,mac,enc = textocif[:16],textocif[16:48],textocif[48:]
        cipher = Cipher(algorithms.AES(passfrase), modes.CTR(iv))
        decryptor = cipher.decryptor()
        ct = decryptor.update(enc) + decryptor.finalize()
        h = hmac.HMAC(passfrase, hashes.SHA256())
        h.update(enc)
        try:
            h.verify(mac)
        except Exception:
            print("HMAC inválido! Ficheiro adulterado.")
            return

        
        with open(fich+".enc"+".dec", 'wb') as f:
            ficheiro = f.write(iv)
            ficheiro = f.write(signature)
            ficheiro = f.write(ct)

    else:
        print("erro")


if __name__ == "__main__":
    pbenc_aes_ctr_hmac_hmac(sys.argv)
