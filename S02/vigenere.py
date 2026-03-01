import cesar
import sys

def vigenere(argv):
    atr, key, msg = argv[1],argv[2],argv[3]
    newstring=''
    msg = cesar.preproc(msg)
    size_key = len(key)
    i = 0
    if atr == 'enc':
        for l in msg:
            temp = (ord(l) + ord(key[i])) % 26 + ord('a')
            newstring += chr(temp)
            i += 1
            i = i % size_key
    elif atr == 'dec':
        for l in msg:
            temp = (ord(l) - ord(key[i])) % 26 + ord('a')
            newstring += chr(temp)
            i += 1
            i = i % size_key
    else:
        print('There is no other option.')
    print(cesar.preproc(newstring))
    return newstring

if __name__=="__main__":
    vigenere(sys.argv)