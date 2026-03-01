import sys
import vigenere

def preproc(str):
      l = []
      for c in str:
          if c.isalpha():
              l.append(c.upper())
      return "".join(l)  
  
def vigenere_atack (argv):
    num = int(argv[1])
    mens= preproc(argv[2])
    palavras=argv[3:]
    print(num)
    key=''
    for k in range(num):
        dic={}
        partes=mens[k::num]
        for i in partes:
            if i not in dic:
                dic[i]=0
            dic[i]+=1
        ordenado = sorted(dic, key=dic.get, reverse=True)
        
        if ordenado:
            maisfreq=ordenado[0]
            ind=(ord(maisfreq) - ord('A')) %26
            res=chr(ind+ord('a'))
            key+=res
            key=preproc(key)
    mokargv=['','dec',key,mens]
    ans=vigenere.vigenere(mokargv)
    ans=preproc(ans)
    for p in palavras:
        if p.upper() in ans:
            print(key)
            
if __name__=="__main__":
    vigenere_atack(sys.argv)
