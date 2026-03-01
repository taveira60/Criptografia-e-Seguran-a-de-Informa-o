import sys
import os

def otp(argv):
    
    if argv[1]=='setup':
        if not(argv[2].isdigit()):
            print('Erro tem de ser um inteiro')
        if not(argv[3].endswith('.key')):
            print('Erro')
        else:
            bits=int(argv[2])
            ficheiro=argv[3]
            key=os.urandom(bits)
            file=open(ficheiro,'wb')
            file.write(key)
            file.close
    if argv[1]=='enc':
        if not(argv[2].endswith('.txt')):
            print('erro')
        if not(argv[3].endswith('.key')):
            print('erro')
        else:
            ficheiro=argv[2]
            chave=argv[3]
            with open(ficheiro, 'rb') as o_msg:
                mens = o_msg.read()
            with open(chave, 'rb') as o_cha:
                key = o_cha.read()
            if len(mens)>len(key):
                print("nao da tem de ter tamanho igual")
            mensenc=[]
            for i in range(len(mens)):
                bytes_chave=key[i]
                bytes_mens=mens[i]
                
                j= bytes_chave^bytes_mens
                mensenc.append(j)
                
            fileenc=open(ficheiro +'.enc','wb')
            fileenc.write(bytes(mensenc))
            fileenc.close
            
    if argv[1]=='dec':
        if not(argv[2].endswith('.enc')):
            print('erro')
        if not(argv[3].endswith('.key')):
            print('erro')
        else:
            ficheiro=argv[2]
            chave=argv[3]
            with open(ficheiro,'rb') as fic:
                mens=fic.read()
            with open(chave,'rb') as chav:
                key=chav.read()
            if len(mens)>len(key):
                print('nao tem o mesmo tamanho')
            mensfinal=[]
            for i in range(len(mens)):
                bytes_chave=key[i]
                bytes_mens=mens[i]
                
                j=bytes_chave^bytes_mens
                mensfinal.append(j)
            filefinal=open(ficheiro +'.dec','wb')
            filefinal.write(bytes(mensfinal))
            filefinal.close
            
            
if __name__ == "__main__":
    otp(sys.argv)