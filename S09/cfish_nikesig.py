import sys
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.asymmetric import rsa,dh
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography import x509
import datetime

def mkpair(x, y):
   """ produz uma byte-string contendo o tuplo '(x,y)' ('x' e 'y' são byte-strings) """
   len_x = len(x)
   len_x_bytes = len_x.to_bytes(2, 'little')
   return len_x_bytes + x + y

def unpair(xy):
   """ extrai componentes de um par codificado com 'mkpair' """
   len_x = int.from_bytes(xy[:2], 'little')
   x = xy[2:len_x+2]
   y = xy[len_x+2:]
   return x, y

def cert_load(fname):
    """ lê certificado de ficheiro """
    with open(fname, "rb") as fcert:
        cert = x509.load_pem_x509_certificate(fcert.read())
    return cert


def cert_validtime(cert, now=None):
    """ valida que 'now' se encontra no período
    de validade do certificado. """
    if now is None:
        now = datetime.datetime.now(tz=datetime.timezone.utc)
    if now < cert.not_valid_before_utc or now > cert.not_valid_after_utc:
        raise x509.verification.VerificationError(
            "Certificate is not valid at this time")


def cert_validsubject(cert, attrs=[]):
    """ verifica atributos do campo 'subject'. 'attrs'
    é uma lista de pares '(attr,value)' que condiciona
    os valores de 'attr' a 'value'. """
    print(cert.subject)
    for attr in attrs:
        if cert.subject.get_attributes_for_oid(attr[0])[0].value != attr[1]:
            raise x509.verification.VerificationError("Certificate subject does not match expected value")


def cert_validexts(cert, policy=[]):
    """ valida extensões do certificado. 'policy' é uma lista de pares '(ext,pred)' onde 'ext' é o OID de uma extensão e 'pred'
    o predicado responsável por verificar o conteúdo dessa extensão. """
    for check in policy:
        ext = cert.extensions.get_extension_for_oid(check[0]).value
        if not check[1](ext):
            raise x509.verification.VerificationError(
            "Certificate extensions does not match expected value")

def valida_cert(ca_cert,nome):
    try:
        cert = cert_load(nome+".crt")
        # obs: pressupõe que a cadeia de certifica só contém 2 níveis
        cert.verify_directly_issued_by(ca_cert)
        # verificar período de validade...
        cert_validtime(cert)
        # verificar identidade... (e.g.)
        cert_validsubject(cert, [(x509.NameOID.COMMON_NAME, "CSI "+nome)])
        # verificar aplicabilidade... (e.g.)
        #cert_validexts(cert, [(x509.ExtensionOID.EXTENDED_KEY_USAGE, lambda e: x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH in e)])
        #print("Certificate is valid!")
        return True
    except:
        #print("Certificate is invalid!")
        return False

def cfish_nikesig(argv):
    type=argv[1]
    CA = cert_load("CA.crt")
    if type=="enc":
        user=argv[2]
        me = argv[3]
        fich = argv[4]
        
        
        
        public_key_rsa = cert_load(user+".crt").public_key()
        ##User Keys
        if valida_cert(CA,user):
            print("Cerificado Válido")
        else:
            print("Certificado Inválido")
            return
                    
        with open(me+".key",'rb') as f:   
            private_key_rsa = load_pem_private_key(f.read(),password=b"1234")
            
        with open(fich,"rb") as f:
            message = f.read()
            
        ciphertext = public_key_rsa.encrypt(
            message,
            padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
            )
        )    

        signature = private_key_rsa.sign(
            ciphertext,
            padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
       )

        with open(fich+'.enc',"wb") as f:
            f.write(mkpair(ciphertext,signature))
        

    elif type=="dec":
        user = argv[3]
        me = argv[2]
        fich = argv[4]
        with open(me+".key",'rb') as f:   
            private_key_rsa = load_pem_private_key(f.read(),password=b"1234")
            
        public_key_rsa = cert_load(user+".crt").public_key()
            
        if valida_cert(CA,user):
            print("Cerificado Válido")
        else:
            print("Certificado Inválido")
            return
            
        with open(fich,"rb") as f:
            message,sig = unpair(f.read())
            
        
        public_key_rsa.verify(
            sig,
            message,  
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        cleartext = private_key_rsa.decrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        with open(fich+".dec",'wb') as f:
            f.write(cleartext)


    else:
        print("erro")
        
if __name__ == "__main__":
    cfish_nikesig(sys.argv)
