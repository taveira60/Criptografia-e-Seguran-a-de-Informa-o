import sys

def preproc(str):
      l = []
      for c in str:
          if c.isalpha():
              l.append(c.upper())
      return "".join(l)  


def cesar(argv):
    newstring=''
    if argv[1] == 'enc':
        for l in argv[3]:
            temp = (ord(l) + ord(argv[2])) % 26 + ord('a')
            newstring += chr(temp)
            # print(newstring)
    elif argv[1]== 'dec':
        for l in argv[3]:
            temp = (ord(l) - ord(argv[2])) % 26 + ord('a')
            newstring += chr(temp)
    else:
        print('There is no other option.')
    return newstring

        
# The informatics Engineering
    

if __name__=="__main__":
    print(preproc(cesar))