import struct, os ,sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def chacha20_int_attack(argv):
    fl,pos,original,decryp = argv[1],int(argv[2]),argv[3].encode(), argv[4].encode()
    with open(fl,'rb') as f:
        msg_C = bytearray(f.read())
    
    for i in range(len(original)):
        j=pos+i
        
        byte_atual=msg_C[j]
        byte_nove=byte_atual^original[i]^decryp[i]
        
        
        msg_C[j]=byte_nove
    
    
    with open(fl + ".attck",'wb') as f:
        f.write(msg_C)

if __name__ == "__main__":
    chacha20_int_attack(sys.argv)