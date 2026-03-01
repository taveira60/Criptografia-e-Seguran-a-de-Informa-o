import sys
import re
# defs auxiliares...
def conta_linhas(file):
    linhas = len(file.readlines())
    file.seek(0)
    return linhas
        
def conta_pal(file):
    data = file.read()
    x = data.split()
    file.seek(0)
    return len(x)
        
def contra_charateres(texto):
    contador = 0
    print(texto)
    for linha in texto:
        for chr in  linha:
            if chr not in (" ","\n"):
                contador+=1
   
    return contador

def main(inp):
    """ função que executa a funcionalidade pretendida... """
    print("Argumentos da linha de comando: ", inp)
    text = open(inp[1])
    a=conta_linhas(text)
    b=conta_pal(text)
    c=contra_charateres(text)
    
    print(f"{a}    {b}   {c}")

# Se for chamada como script...
if __name__ == "__main__":
    main(sys.argv)