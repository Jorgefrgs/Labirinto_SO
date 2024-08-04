import threading
import random
import time

N = 10
num_queijos = 80
NUM_JOGADORES = 6

movimentos = ['cima', 'baixo', 'direita', 'esquerda']

mapa = [['X' for _ in range(N)] for _ in range(N)]
posicao_jogador = [None] * NUM_JOGADORES
pontuacao = [0] * NUM_JOGADORES

mutexes = [[None for _ in range(N)] for _ in range(N)]
contador_mutex = 0
contador_celulas = 0

#classe do mutex para a competição por queijos
class Mutex:
    def __init__(self):
        self.locked = False
        self.cond = threading.Condition()

    def acquire(self):
        with self.cond:
            while self.locked:
                self.cond.wait()
            self.locked = True

    def release(self):
        with self.cond:
            self.locked = False
            self.cond.notify_all()

#classe do semáforo para organizar os turnos
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

# Inicialização dos mutexes para cada célula do mapa
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
    
#função que controla a movimentação dos jogadores
def movimentar_jogador(jogador):
    global contador_mutex, contador_celulas

    #semáforo controla a vez dos jogadores
    semaforo.acquire()

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
    posicao_jogador[jogador] = nova_posicao

    competidores = [j for j in range(NUM_JOGADORES) if posicao_jogador[j] == nova_posicao]
    if mapa[x][y] == 'Q':
        if len(competidores) > 1:
            print(f"Competição detectada para queijo na posição ({x}, {y}) por jogadores: {competidores}")
            contador_mutex += 1
        mutexes[x][y].acquire()
        if mapa[x][y] == 'Q' and posicao_jogador[jogador] == nova_posicao:
            pontuacao[jogador] += 1
            mapa[x][y] = 'X'
            print(f"Jogador {jogador + 1} pegou um queijo na posição ({x}, {y})!")
        mutexes[x][y].release()
    elif mapa[x][y] == 'X':
        if len(competidores) > 1:
            print(f"Competição detectada por célula vazia na posição ({x}, {y}) por jogadores: {competidores}")
            contador_celulas += 1

    semaforo.release()

#função para começar o jogo
def jogo():
    inicializar_mapa()

    while contar_queijos() > 0:
        print("Rodada")
        for i in range(NUM_JOGADORES):
            posicao_jogador[i] = (random.randint(0, N - 1), random.randint(0, N - 1))
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
