# Jogo Corrida dos Ratos
Descrição do Jogo
O "Corrida dos Ratos" é um jogo multiplayer em que até seis jogadores competem para coletar o máximo de queijos possível em um mapa de dimensões N x N. O objetivo é acumular pontos ao coletar queijos distribuídos aleatoriamente pelo mapa. O jogo acontece em turnos, e cada jogador se move de acordo com uma ação aleatória ("cima", "baixo", "direita" ou "esquerda") em cada rodada.

Condições de Corrida:
Coleta de Queijo: Se dois ou mais jogadores tentarem coletar o mesmo queijo ao mesmo tempo, pode haver um conflito sobre quem realmente coleta o queijo. Sem um controle adequado, pode ocorrer uma competição não resolvida, onde o queijo pode ser removido sem ser atribuído a um jogador específico.
Células Vazias: Quando vários jogadores se movem para a mesma célula vazia, pode haver conflitos na contagem e na atualização das células.

Possíveis Soluções:
Semáforo: Utilizado para coordenar o acesso ao processo de movimentação e coleta de queijos. Garante que apenas um jogador realize a movimentação ou coleta por vez, evitando conflitos ao acessar células compartilhadas.
Mutex: Utilizado para proteger o acesso às células do mapa durante a coleta de queijos. Garante que apenas um jogador possa acessar uma célula de cada vez, evitando a sobrecarga.

Regras do Jogo:
Número de Jogadores: O jogo suporta de 2 a 6 jogadores. Cada jogador é representado por um "rato" no mapa.
Movimentação: Em cada rodada, os jogadores se movem aleatoriamente em uma das quatro direções possíveis: cima, baixo, direita ou esquerda.
Coleta de Queijos: Quando um jogador se move para uma célula com um queijo, ele coleta o queijo e a célula é atualizada para indicar que o queijo foi removido.
Conflitos: Se múltiplos jogadores tentarem coletar o mesmo queijo ao mesmo tempo, um mecanismo de semáforo e mutex garante que apenas um jogador possa coletar o queijo. A competição por células vazias é registrada, mas não afeta a coleta.

Condição de Término: O jogo continua até que todos os queijos sejam coletados. O jogador com o maior número de queijos ao final do jogo é o vencedor.