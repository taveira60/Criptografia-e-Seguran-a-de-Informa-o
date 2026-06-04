# ex1
Neste exercicio transformamos uma mensagem binária de 128 bits numa representação adequada para operações numéricas dentro do anel Zq, e posteriormente recuperamos a mensagem original. Este proceosso é dividido em duas fases: o encode e o decode.Estes valores vão ser posteriormente organizados numa matriz n * n, que no caso será n=8.
Na fase do encode consiste em mapear cada valor inteiro x que pertence a  {0,1,2,3} para um elemento do anel Zq, através da operação de escala que nos é dada no enunciado. 
A fase de decode realiza o processo inverso. Cada valor da matriz, que pertence a Zq, é escalado de volta para o intervalo original através da expressão que também nos é dada no enunciado. Essa operação aproxima o valor ao inteiro mais próximo em {0,1,2,3}. Posto isto, cada inteiro é novamente convertido no correspondente par de bits, reconstruinod assim a mensagem original de tamanho 128 bits.

# ex2 
Neste exercício implementamos uma versão simplificada do exercício anterior. O processo é dividido em três fases principais: geração de chaves (key generation), encriptação e desencriptação.
Na fase de criação de chaves é criada uma matriz pública A, de dimensão n * n, a partir de uma seed aleatória. De seguida criamos duas matrizes S e E, que representam o segredo e o ruídom, respetivamente. Estas matrizes são obtidas através de uma distribuição secreta, centrada em 0, garantindo que os seus valores são pequenos. A chave pública é calculada como sendo B = A * S + E.
Na fase de encriptação, o utilizador controi o criptograma através da chave pública. Geramos novas matrizes de ruído S', E' e E'', e calcula-se c1 = S' * A + E'. Paralelamente calculamos V' = S * B + E''. A mensagem original é previamente codificada numa matriz M, utilizando o processo de encode do exercicio anterior. A esta matriz é depois adicionada V', obtendo-se c2 = V' + M. O criptograma final é o par (c1,c2).
Na fase de desencriptação, o utilizador usa a chave secreta S para recuperar a mensagem. Começa por calcular V = c1 * S, que aproxima o valor S' * A * S. De seguida, subtrain este valor a c2, obtendo M' = c2 - V, que corresponde à mensagem orginal com algum ruído resídual. Posto isto, aplica-se o processo de decode do exercício anterior para recuperar os bits originais.
Podemos concluir que ao reduzir os parâmetros n e q o sistema torna-se mais rápido, e consegue manter a correção porque o ruído é propositadamente baixo, mas isto leva a que a sua segurança também diminua pois a reduzida dimensão de n torna-o vulnerável a ataques reticulados.


# ex3
Neste exercício usamos as mesmas funções que no exercicio anterior mudando apenas a distribuição de ruído do esquema original.
Podemos concluir que, ao injetar o ruído do esquema original num sistema de módulo reduzido, a taxa de erro sobe bastante seação pode-se tornar inútil. respeitarmos os 15 bits de precisão da tabela. Com isto concluímos que não podemos aumentar a segurança (ruído) sem aumentar proporcionalmente os recursos (q), porque o canal de comunic




# Uso de IA
Nos utilizamos inteligencia artificial, para ver algumas funcões predefinidas do sagemath, bem como para corrigir alguns erros de tipos, e por fim para fazer um pretty print das matrizes.