import threading
import random
import time

#definições inicias do mapa
print("Escolha as dimensões NxN do mapa:")
N = int(input())
print("Escolha a quantidade de queijos dispostos pelo mapa:")
num_queijos = int(input())
print("Escolha o número de jogadores da rodada:")
NUM_JOGADORES = int(input())


movimentos = ['cima', 'baixo', 'direita', 'esquerda']

mapa = [['X' for a in range(N)] for a in range(N)]
posicao_jogador = [None] * NUM_JOGADORES
pontuacao = [0] * NUM_JOGADORES

#inicia-se zerado e é atualizado com o decorrer das rodadas
mutexes = [[None for b in range(N)] for b in range(N)]
contador_mutex = 0
contador_celulas = 0

#classe do mutex para a competição por queijos
#lock() protege o acesso da célula e garante que não ocorra acesso simultâneo
class Mutex:
    def __init__(self):
        self.lock = threading.Lock()

    def acquire(self):
        self.lock.acquire()

    def release(self):
        self.lock.release()

#classe do semáforo para organizar os turnos
#self.cond.wait() faz com que as demais threads aguardem a notificação de forma assíncrona para poderem realizar seus movimentos
#self.cond.notify() por sua vez notifica todas as threads que aguardam a mensagem assíncrona
class Semaforo:
    def __init__(self, count=1):
        self.count = count
        self.cond = threading.Condition()

    def acquire(self):
        with self.cond:
            while self.count == 0:
                self.cond.wait()
            self.count -= 1

    def release(self):
        with self.cond:
            self.count += 1
            self.cond.notify()

#inicialização dos mutexes para cada célula do mapa
for i in range(N):
    for j in range(N):
        mutexes[i][j] = Mutex()

semaforo = Semaforo(count=1)  

#função para gerar o mapa inicial
def inicializar_mapa():
    global num_queijos
    queijos_colocados = 0
    while queijos_colocados < num_queijos:
        x = random.randint(0, N - 1)
        y = random.randint(0, N - 1)
        if mapa[x][y] == 'X':
            mapa[x][y] = 'Q'
            queijos_colocados += 1
    print("Mapa inicial:")
    for linha in mapa:
        print(' '.join(linha))
    print()

#contador de queijos para garantir o final do jogo
def contar_queijos():
    return sum(row.count('Q') for row in mapa)

#função para imprimir o mapa atualizado
def imprimir_mapa():
    for linha in mapa:
        print(' '.join(linha))
    print()

#função para definir a movimentação dos jogadores
def movimentar_jogador(jogador):
    global contador_mutex, contador_celulas

    #semáforo controla a vez dos jogadores
    semaforo.acquire()

    #randomizando as escolhas de movimentação para o jogo ser dinâmico e englobar mais resultados finais
    movimento = random.choice(movimentos)
    x, y = posicao_jogador[jogador]

    if movimento == 'cima':
        x = max(0, x - 1)
    elif movimento == 'baixo':
        x = min(N - 1, x + 1)
    elif movimento == 'direita':
        y = min(N - 1, y + 1)
    elif movimento == 'esquerda':
        y = max(0, y - 1)

    nova_posicao = (x, y)
    print(f"Jogador {jogador + 1} se moveu para {nova_posicao}")
    posicao_jogador[jogador] = nova_posicao

    #adquirindo o mutex da nova posição
    mutexes[x][y].acquire()
    
    #verificando competição por queijo
    if mapa[x][y] == 'Q':
        competidores = [j for j in range(NUM_JOGADORES) if posicao_jogador[j] == nova_posicao]
        if len(competidores) > 1:
            print(f"Competição detectada para queijo na posição ({x}, {y}) por jogadores: {competidores}")
            contador_mutex += 1
        
        #se ainda houver queijo na posição após adquirir o mutex
        if mapa[x][y] == 'Q' and posicao_jogador[jogador] == nova_posicao:
            pontuacao[jogador] += 1
            mapa[x][y] = 'X'
            print(f"Jogador {jogador + 1} pegou um queijo na posição ({x}, {y})!")
    
    #verificando competição por célula vazia
    elif mapa[x][y] == 'X':
        competidores = [j for j in range(NUM_JOGADORES) if posicao_jogador[j] == nova_posicao]
        if len(competidores) > 1:
            print(f"Competição detectada por célula vazia na posição ({x}, {y}) por jogadores: {competidores}")
            contador_celulas += 1

    mutexes[x][y].release()

    semaforo.release()


#função para começar e terminar o jogo
#implementação das threads dependendo do número de jogadores escolhidos
def jogo():
    inicializar_mapa()

    for i in range(NUM_JOGADORES):
        posicao_jogador[i] = (random.randint(0, N - 1), random.randint(0, N - 1))

    while contar_queijos() > 0:
        print("Rodada")
        threads = [threading.Thread(target=movimentar_jogador, args=(i,)) for i in range(NUM_JOGADORES)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        imprimir_mapa()
        time.sleep(1)

    print("Fim do jogo!")
    for i, pontos in enumerate(pontuacao):
        print(f"Jogador {i + 1}: {pontos} queijos")
    print(f"Total de competições por queijo (mutex adquirido): {contador_mutex}")
    print(f"Total de competições por células vazias: {contador_celulas}")

jogo()