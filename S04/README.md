### QUESTÃO: Q1

Qual será o impacto de executar o programa `chacha20_int_attck.py` sobre um criptograma produzido pelo seu programa? Justifique.

R.:Se executar-mos o programa chacha20_int_attack.py sobre um criptograma produzido pelo nosso programa, que é feito em cifra autenticada ( que no caso usa ChaCha20Poly1305), o ataque não terá sucesso.
Numa cifra sequencial, o criptograma é obtido da seguinte forma:
	-A chave + iv são usados para gerar um fluxo pseudo-aleatório, que é do mesmo tamanho da mensagem;
	-Após isso o criptograma é obtido fazendo XOR, entre o texto limpo e o fluxo de chave.
Isto significa que o atacante pode modificar bits do criptograma, que como não existe verificação de integridade no programa, o sistema aceita o texto alterado.
Contrariamente, ao usar-mos o ChaCha20Poly1305 estamos a combinar uma cifra sequencial(ChaCha20) e um mecanismo de autenticação(Poly1305) o que nos garante simultaneamente confidencialidade, integridade e autenticidade: 
Posto isto, se qualquer bit do criptograma tiver sido alterado o programa falha e o texto não é devolvido.
Concluido, se usarmos o chacha20_int_atack.py sobre um criptograma produzido por este programa, o ataque não funciona.

### QUESTÃO: Q2

Um ataque a um MAC consiste em, após ter acesso pares de *mensagem/tag* válidos, 
conseguir produzir um novo par *msg/tag* válido sem conhecer a chave respectiva.

Mostre como é possível atacar a versão do MAC que inclui o vector aleatório.

R.: Como a Tag é formada através da Mensagem + o IV, o ataque é possível porque o IV é aleatório e não fixo. Como nós sabemos qual é a Tag que o sistema espera e o IV pode ser qualquer um, nós conseguimos alterar o IV de maneira a que a nossa nova mensagem, juntamente com esse IV que nós escolhemos, dê exatamente a mesma Tag que a mensagem original dava.

Isto mostra a grande diferença para um IV fixo, pois se o IV fosse sempre o mesmo, o atacante não teria como ajustar o cálculo e a única mensagem que daria aquela Tag seria a original. No caso do IV aleatório, o atacante usa-o para "compensar" a mudança na mensagem e enganar o sistema para chegar ao mesmo resultado final.