# Relatório da Semana 2

Este documento descreve as implementações e conceitos abordados na Semana 2, focando nas cifras de César, Vigenère e One-Time Pad (OTP).

## Índice
1. [Cifra de César](#1-cifra-de-cesar)
2. [Cifra de Vigenère](#2-cifra-de-vigenere)
3. [One-Time Pad (OTP)](#3-one-time-pad-otp)
4. [My OTP e Vulnerabilidades](#4-my-otp-e-vulnerabilidades)
5. [Questões Teóricas](#5-questoes-teoricas)

---

## 1. Cifra de César

A cifra de César caracteriza-se por realizar um deslocamento do alfabeto com que é escrita a mensagem.

* **[cesar.py](cesar.py)**: Implementa as operações `enc` e `dec` utilizando um deslocamento baseado num único carácter.
* **[cesar_attack.py](cesar_attack.py)**: Realiza um ataque de força bruta ao criptograma, validando o resultado contra uma lista de palavras conhecidas.

---

## 2. Cifra de Vigenère

A cifra de Vigenère aplica uma sequência de cifras de César, onde cada carácter da mensagem é cifrado de acordo com um carácter correspondente da chave.

* **[vigenere.py](vigenere.py)**: Implementa a cifra polialfabética. A chave é aplicada ciclicamente ao longo da mensagem utilizando a operação de módulo 26.
* **[vigenere_attack.py](vigenere_attack.py)**: Ataca a cifra dividindo o criptograma em "fatias" (baseadas no tamanho provável da chave) e aplicando análise de frequência em cada uma para determinar os caracteres da chave.

---

## 3. One-Time Pad (OTP)

A cifra One-Time Pad (OTP) utiliza o alfabeto binário e a operação **XOR**. É considerada inquebrável se a chave for perfeitamente aleatória e nunca reutilizada.


### Comandos do programa [otp.py](otp.py)
* **setup**: Gera bytes aleatórios seguros utilizando `os.urandom`.
* **enc**: Cifra um ficheiro e guarda o resultado com o sufixo `.enc`.
* **dec**: Decifra um ficheiro e guarda o resultado com o sufixo `.dec`.

---

## 4. My OTP e Vulnerabilidades

O programa [my_otp.py](my_otp.py) demonstra o perigo de utilizar geradores de números pseudo-aleatórios não seguros em criptografia.

### Funcionamento do my_prng
* Baseia-se na biblioteca `random` do Python alimentada por uma semente (seed) expandida.
* **Implementação Técnica**: Foi necessário converter a semente de bytes para um inteiro utilizando `int.from_bytes` para permitir as operações de bits na função `seed_expand`.

---

## 5. Questões Teóricas

### Questão Q1: Diferenças entre otp.py e my_otp.py
R.: A única e principal diferença encontra-se na maneira como as chaves são criadas. No my_otp, as chaves baseiam-se numa seed, o que as torna previsíveis e, consequentemente, inseguras. Por outro lado, o otp utiliza o os.urandom, que gera chaves mais seguras através do sistema operativo.

### Questão Q2: O ataque realizado no ponto anterior não entra em contradição com o resultado que estabelece a "segurança absoluta" da cifra *one-time pad*? Justifique.
R.: A vulnerabilidade que exploramos no ataque não é do algoritmo OTP em si mas sim de um método diferente de gerar números aleatórios, que torna o ataque por força bruta mais viável. Posto isto, não há contradição visto que nós não atacamos o OTP em si, mas sim um tipo de implementação deste algoritmo. Se tentássemos usar o ataque que fizemos para a funçao my_otp na versão otp, este não teria resultado.