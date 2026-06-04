from cryptography import x509
import datetime


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



def valida_certALICE(ca_cert):
    try:
        cert = cert_load("BOB.crt")
        # obs: pressupõe que a cadeia de certifica só contém 2 níveis
        cert.verify_directly_issued_by(ca_cert)
        # verificar período de validade...
        cert_validtime(cert)
        # verificar identidade... (e.g.)
        cert_validsubject(cert, [(x509.NameOID.COMMON_NAME, "CSI BOB")])
        # verificar aplicabilidade... (e.g.)
        #cert_validexts(cert, [(x509.ExtensionOID.EXTENDED_KEY_USAGE, lambda e: x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH in e)])
        #print("Certificate is valid!")
        return True
    except:
        #print("Certificate is invalid!")
        return False

if __name__ == "__main__":
    ca_cert = cert_load("CA.crt")  # certificado da autoridade certificadora
    resultado = valida_certALICE(ca_cert)

    if resultado:
        print("Certificado válido")
    else:
        print("Certificado inválido")


#Resposta: 
# No procedimento de verificação, os campos que devem ser objeto de atenção são Subject (Identidade), 
# o Issuer(emissor), a Validade dos certificados e as Extensões, que nos dizem para o que é que 
# serve o certificado, ou seja temos de verificar se podemos usar para o que queremos.