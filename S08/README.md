# Cfish NikeSig - Comunicação Segura

Este projeto foi o resultado de um guião prático sobre **Criptografia NikeSig**. Basicamente, crieamos uma ferramenta em Python que permite que dois utilizadores (como a Alice e o Bob) troquem ficheiros sem que ninguém consiga ler o conteúdo e, mais importante, garantindo que ninguém alterou os dados pelo caminho.
## O que aprendemos
Fazer este trabalho ajudou-nos a perceber como os conceitos teóricos de segurança funcionam na "vida real":
Aprendemos que para confiar numa chave pública (neste caso, a Diffie-Hellman), ela deve ser assinada por outra chave de confiança (RSA). É como ter um cartão de cidadão para a tua chave digital. Percebemos que cifrar não chega. Precisamos de assinar para garantir que o ficheiro que chega ao destino é exatamente o mesmo que saiu. No código de decifração, aprendemos que primeiro verificamos se a assinatura é válida e só depois é que tentamos abrir o ficheiro.