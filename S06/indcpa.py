from abc import ABC, abstractmethod
import struct, os ,sys  
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import random

class Cipher_(ABC):
    @abstractmethod
    def keygen(self) -> bytes:
        pass
  
    @abstractmethod
    def enc(self, key: bytes, text: bytes) -> bytes:
        pass

    @abstractmethod
    def dec(self, key: bytes, ciphertext: bytes) -> bytes:
        pass

class INDCPA_Adv(ABC):
    @abstractmethod
    def choose(self, oracle: callable) -> bytes:
        pass

    @abstractmethod
    def guess(self, oracle: callable, ciphertext: bytes) -> bool:
        pass

class CipherChaCha20(Cipher_):
    
    def keygen(self):
        key=os.urandom(32)
        return key
    
    def enc(self, key: bytes, text: bytes):
        counter = 0
        nonce = os.urandom(8)
        full_nonce = struct.pack("<Q", counter) + nonce
        algorithm = algorithms.ChaCha20(key, full_nonce)
        cipher = Cipher(algorithm, mode=None)
        encryptor = cipher.encryptor()
        ct = encryptor.update(text) + encryptor.finalize()
        return nonce + ct
    
    def dec(self, key: bytes, ciphertext: bytes):
        counter = 0
        nonce = ciphertext[:8]
        menscrip = ciphertext[8:]
        full_nonce = struct.pack("<Q", counter) + nonce
        algorithm = algorithms.ChaCha20(key, full_nonce)
        cipher = Cipher(algorithm, mode=None)
        decryptor = cipher.decryptor()
        dec = decryptor.update(menscrip) + decryptor.finalize()

        return dec

class IdentityCipher(Cipher_):
    def keygen(self):
        return b''
    
    def enc(self, key: bytes, text: bytes):
        return text
    
    def dec(self, key: bytes, ciphertext: bytes):
        return ciphertext
    
class Adversario_Identidade(ABC):
    def choose(self, oracle: callable) -> bytes:
        self.m0=b'miguel bay'
        self.m1=b'miguel mig'
        return self.m0 ,self.m1


    def guess(self, oracle: callable, ciphertext: bytes) -> bool:
        
        if ciphertext==self.m0:
            return 0
        else:
            return 1

class Adversario_ChaCha20(ABC):
    def choose(self, oracle: callable) -> bytes:
        self.m0=b'taveira bay'
        self.m1=b't veiramig '
        return self.m0 ,self.m1


    def guess(self, oracle: callable, ciphertext: bytes) -> bool:
        
        return random.choice([0,1])


def IND_CPA(C,A):
    cif = C()
    k = cif.keygen()
    enc_oracle = lambda ptxt: cif.enc(k,ptxt)
    adv = A()
    m0, m1 = adv.choose(enc_oracle)
    assert len(m0)==len(m1)
    b = random.choice([0,1])
    # print(b)
    if b==0:
        c = cif.enc(k,m0)
    else:
        c = cif.enc(k,m1)
    d = adv.guess(enc_oracle, c)
    # print(d,b==d)
    return b==d
    
if __name__ == "__main__":

    # Fazemos a "Animação" (simulação de 1000 jogos)
    jogos = 1000000
    vitorias = 0
    
    print("A testar a segurança do ChaCha20...")
    for i in range(jogos):
        acertou = IND_CPA(CipherChaCha20,Adversario_ChaCha20)
        if acertou:
            vitorias += 1
            
    print(f"O adversário acertou {vitorias} vezes em {jogos} jogos.")
    print(f"Taxa de sucesso: {(vitorias/jogos)*100}% (Deverá ser perto de 50%)")
    
    print("-"*70)
    
    jogos2 = 1000000
    vitorias2 = 0
    
    print("A testar a segurança do trivial...")
    for i in range(jogos2):
        acertou = IND_CPA(IdentityCipher,Adversario_Identidade)
        if acertou:
            vitorias2 += 1
            
    print(f"O adversário acertou {vitorias2} vezes em {jogos2} jogos.")
    print(f"Taxa de sucesso: {(vitorias2/jogos2)*100}% (Deverá ser 100%)")
    
    