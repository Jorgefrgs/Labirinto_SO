🐭 Corrida dos Ratos
Corrida dos Ratos é um jogo multiplayer onde jogadores competem para coletar o máximo de queijos possíveis em um mapa de dimensões N x N. O objetivo é acumular pontos ao coletar queijos distribuídos aleatoriamente pelo mapa. O jogo acontece em turnos, e cada jogador se move de acordo com uma ação aleatória ("cima", "baixo", "direita" ou "esquerda") em cada rodada.

🎮 Regras do Jogo
Número de Jogadores: A quantidade de jogadores é requisitada pelo terminal. Cada jogador é representado por um "rato" no mapa.

Movimentação: Em cada rodada, os jogadores se movem aleatoriamente em uma das quatro direções possíveis: cima, baixo, direita ou esquerda.

Coleta de Queijos: Quando um jogador se move para uma célula com um queijo, ele coleta o queijo, e a célula é atualizada para indicar que o queijo foi removido.

Conflitos:

Coleta de Queijo: Se dois ou mais jogadores tentarem coletar o mesmo queijo ao mesmo tempo, há um conflito sobre quem realmente coleta o queijo. O uso de mutexes garante que apenas um jogador possa coletar o queijo.
Células Vazias: Quando vários jogadores se movem para a mesma célula vazia, a competição é registrada, mas não afeta o jogo.
Condição de Término: O jogo continua até que todos os queijos sejam coletados. O jogador com o maior número de queijos ao final do jogo é o vencedor.

🛠️ Pré-requisitos
Python 3.6 ou superior

🚀 Iniciando o Jogo
Clone o repositório:

bash
git clone https://github.com/Jorgefrgs/Labirinto_SO.git
cd corrida-dos-ratos
Execute o jogo:

bash
python3 corrida_dos_ratos.py
Siga as instruções no terminal:

Escolha as dimensões do mapa (NxN).
Escolha a quantidade de queijos.
Escolha o número de jogadores.

📊 Condições de Corrida
Mutex: Protege o acesso às células do mapa durante a coleta de queijos. Garante que apenas um jogador possa acessar uma célula de cada vez.
Semáforo: Coordena o acesso ao processo de movimentação e coleta de queijos, garantindo que apenas um jogador realize a movimentação por vez, evitando conflitos.

🏆 Resultado Final
Após todas as rodadas, o jogo exibirá:

A pontuação de cada jogador (quantidade de queijos coletados).
O número total de competições por queijo.
O número total de competições por células vazias.

💡 Exemplo de Execução
plaintext
Copiar código
Escolha as dimensões NxN do mapa:
5
Escolha a quantidade de queijos dispostos pelo mapa:
3
Escolha o número de jogadores da rodada:
4

Mapa inicial:
X Q X X X
X X X X X
X X Q X X
X X X X X
X X X Q X

Rodada
Jogador 1 se moveu para (2, 2)
Jogador 2 se moveu para (1, 2)
Jogador 3 se moveu para (3, 3)
Jogador 4 se moveu para (0, 1)
Jogador 4 pegou um queijo na posição (0, 1)!

...

Fim do jogo!
Jogador 1: 1 queijos
Jogador 2: 0 queijos
Jogador 3: 1 queijos
Jogador 4: 1 queijos
Total de competições por queijo (mutex adquirido): 2
Total de competições por células vazias: 3