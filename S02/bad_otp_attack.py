import sys
import os
import random

def bad_otp_attack(argv):
    fichenc = argv[1]
    palavras = [p.lower() for p in argv[2:]]
    
    if not(fichenc.endswith('.enc')):
        print('Erro')
        return
    
    with open(fichenc, 'rb') as f:
        mensenc = f.read()
    
    # usei 30 porque como no enunciado temos a sucessao de comandos para criar o encriptado e lá usa o 30 é isso que vou usar
    tam = 30
    
    for i in range(65536):
        random.seed(i)
        # gerar a chave com  base no tam que lhe demos antes senão n dá
        chave_completa = random.randbytes(tam)
        chave_candidata = chave_completa[:len(mensenc)]
        dec = []
        
        for j in range(len(mensenc)):
            bytes_chave = chave_candidata[j]
            bytes_mensage = mensenc[j]
            k = bytes_chave ^ bytes_mensage
            dec.append(k)
        
        try:    
            dec_bytes = bytes(dec)
            dec_txt = dec_bytes.decode('utf-8').lower()
            
            for p in palavras:
                if p in dec_txt:
                    print(dec_txt)
                    return
        except:
            pass
    
    print("Nenhuma mensagem encontrada")

if __name__ == "__main__":
    bad_otp_attack(sys.argv)
