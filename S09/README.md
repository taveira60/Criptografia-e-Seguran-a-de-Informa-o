# Questão 1

R.: Após visualisação do ficheiro[Alice.txt], inicialmente conseguimos ver que ambas as chaves publica e privada tem o mesmo modulo (n), seguidamente nos sabemos que ambas tambem tem a mesma public key(public exponent), sabemos ainda pelas propriedades do rsa que a private key sera o inverso da public key mod n, isto quer dizer que nos sabemos que ambas tem o mesmo n e o mesmo public key, sabemos que a chave privada sera a chave correta desse par, o que se confirma que esta par sim sera válido.

# Questão 2 

R.: No procedimento de verificação, os campos que devem ser objeto de atenção são Subject (Identidade), 
o Issuer(emissor), a Validade dos certificados e as Extensões, que nos dizem para o que é que serve o
certificado, ou seja temos de verificar se podemos usar para o que queremos.

# Questão 3 

R.: Para provrocar um erro na validação do certificado, podemos usar um certificado expirado, alterar os atributos
esperados do sujeito ou utilizar um certificado que não tenha sido emitido por uma entidade de certificação confiável.
Para provocar erros na validação de assinatura, podemos alterar o conteúdo do ficheiro após a sua assinatura podemos utilizar uma chave pública / certificado diferente do que foi utilizado para assinar ou podemos também corromper a própria assinatura. 