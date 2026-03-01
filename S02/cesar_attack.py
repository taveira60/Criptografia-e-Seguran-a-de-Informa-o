import sys
import cesar

def preproc(str):
      l = []
      for c in str:
          if c.isalpha():
              l.append(c.upper())
      return "".join(l)  
  
def cesar_atack (argv):
    i,j,k= 0,0,False 
    pals=argv[2:]
    incr=argv[1]
    alfabeto='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    seq = list(pals)
    for l in alfabeto:
        morkagv = ['','dec',l,incr]
        paldic=preproc(cesar.cesar(morkagv))
        for p in seq:
            i = 0
            while i < len(paldic) and not(k):
                if paldic[i] == p[j]:
                    i += 1
                    j += 1
                    if j == len(p):
                        k = True
                        print(l)
                        print(paldic)

                else:
                    i += 1
                    j = 0

    if not(k):    
        print("Nada")
    
if __name__=="__main__":
    cesar_atack(sys.argv)
