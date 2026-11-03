import random
import time
import matplotlib.pyplot as plt


def flip(e_atual, indice_inicio, tamanho_bloco):
    novo_e = []
    for bit in e_atual:
        novo_e.append(bit)
        
    cont = indice_inicio
    
    while cont < (indice_inicio + tamanho_bloco):
        if cont < len(novo_e):
            if novo_e[cont] == 1:
                novo_e[cont] = 0
            else:
                novo_e[cont] = 1
        cont += 1   
    
    return novo_e

def bfs(e_inicial, e_alvo):
    fila = [ [e_inicial, [], 0] ]
    visitados = [e_inicial]
    
    while len(fila) > 0:
        elemento = fila.pop(0)
        
        e_atual = elemento[0]
        caminho = elemento[1]
        custo = elemento[2]
        
        if e_atual == e_alvo:
            return caminho, custo
            
        i = 0
        while i < len(e_atual):
            tamanho = 1
            while (i + tamanho) <= len(e_atual):
               novo_estado = flip(e_atual, i, tamanho)
               if novo_estado not in visitados:
                   visitados.append(novo_estado)
                   fila.append([novo_estado, caminho + [(i, tamanho)], custo + 1]) 
               tamanho += 1
            
            i += 1

def heuristica(estado):
    blocos = 0
    em_bloco_de_um = False
    
    for bit in estado:
        if bit == 1:
            if em_bloco_de_um == False:
                blocos = blocos + 1
                em_bloco_de_um = True
        else:
            em_bloco_de_um = False
        
    return blocos

def greedy(e_inicial, e_alvo):
    fila = [ [e_inicial, [], 0] ]
    visitados = [e_inicial]
    
    while len(fila) > 0:
        indice_menor = 0
        menor_nota = heuristica(fila[0][0])
        
        j = 1
        while j < len(fila):
            nota_atual = heuristica(fila[j][0])
            if nota_atual < menor_nota:
                menor_nota = nota_atual
                indice_menor = j
            j += 1
            
        elemento = fila.pop(indice_menor)
        
        e_atual = elemento[0]
        caminho = elemento[1]
        custo = elemento[2]
        
        if e_atual == e_alvo:
            return caminho, custo
            
        i = 0
        while i < len(e_atual):
            tamanho = 1
            while (i + tamanho) <= len(e_atual):
               novo_estado = flip(e_atual, i, tamanho)
               if novo_estado not in visitados:
                   visitados.append(novo_estado)
                   fila.append([novo_estado, caminho + [(i, tamanho)], custo + 1]) 
               tamanho += 1
            
            i += 1

def gerar_sequencia(tamanho):
    sequencia = []
    cont = 0
    while cont < tamanho:
        bit = random.choice([0, 1])
        sequencia.append(bit)
        cont += 1
    return sequencia

def avaliar_desempenho(L, N):
    soma_custo_bfs = 0
    soma_custo_greedy = 0
    
    par = 0
    while par < N:
        inicio = gerar_sequencia(L)
        fim = gerar_sequencia(L)
        
        custo_bfs = bfs(inicio, fim)
        soma_custo_bfs = soma_custo_bfs + custo_bfs
        
        custo_greedy = greedy(inicio, fim)
        soma_custo_greedy = soma_custo_greedy + custo_greedy
        
        par += 1
        
    media_bfs = soma_custo_bfs / N
    media_greedy = soma_custo_greedy / N
    
    return media_bfs, media_greedy

'''
tamanhos = [10, 15, 20, 50, 100]
indice_tamanho = 0

print("INICIANDO OS TESTES")

while indice_tamanho < len(tamanhos):
    L = tamanhos[indice_tamanho]
    
    e_inicial = []
    e_alvo = []
    
    cont = 0
    while cont < L:
        e_inicial.append(random.choice([0, 1]))
        e_alvo.append(0)
        cont += 1
        
    print(f"\ntestando tamanho L = {L}")
    print(f"Seq Inicial: {e_inicial}")
    print(f"Seq Alvo:    {e_alvo}")
    
    caminho_b, custo_b = bfs(e_inicial, e_alvo)
    print(f"BFS    -> Custo: {custo_b}")
    
    caminho_g, custo_g = greedy(e_inicial, e_alvo)
    print(f"GULOSO -> Custo: {custo_g}")
    
    indice_tamanho += 1
'''

seq_inicial = [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1]

seq_alvo = []
cont = 0
while cont < len(seq_inicial):
    seq_alvo.append(0)
    cont += 1

print("\nRESULTADO GULOSO")
caminho_g, custo_g = greedy(seq_inicial, seq_alvo)
print(f"Custo: {custo_g}")
print(f"Operações (índice, tamanho): {caminho_g}")


def gerar_sequencia(tamanho):
    return [random.choice([0, 1]) for _ in range(tamanho)]

def gerar_grafico_desempenho():
    tamanhos_bfs = [2, 4, 6, 8, 10, 12]
    tamanhos_greedy = [2, 4, 6, 8, 10, 15, 20, 50]

    tempos_bfs = []
    tempos_greedy = []

    print("\ncalculando tempos do BFS...")
    for L in tamanhos_bfs:
        e_inicial = gerar_sequencia(L)
        e_alvo = [0] * L
        
        t0 = time.time()
        bfs(e_inicial, e_alvo)
        tempos_bfs.append(time.time() - t0)

    print("calculando tempos do guloso...")
    for L in tamanhos_greedy:
        e_inicial = gerar_sequencia(L)
        e_alvo = [0] * L
        
        t0 = time.time()
        greedy(e_inicial, e_alvo)
        tempos_greedy.append(time.time() - t0)

    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(tamanhos_bfs, tempos_bfs, 'o-', color='#d9534f', linewidth=2, label='BFS')
    plt.plot(tamanhos_greedy, tempos_greedy, 's-', color='#0275d8', linewidth=2, label='Algoritmo Guloso')

    plt.yscale('log')
    plt.xlabel('tamanho da sequencia ($L$)', fontsize=12)
    plt.ylabel('tempo de execucao (s) - escala logaritmica', fontsize=12)
    plt.title('comparação de desempenho: BFS vs. Algoritmo Guloso', fontsize=13, fontweight='bold')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(fontsize=11)
    plt.tight_layout()

    plt.savefig('desempenho_bfs_greedy.png', dpi=300)
    print("-> imagem 'desempenho_bfs_greedy.png' salva")

    plt.show()

if __name__ == "__main__":
    gerar_grafico_desempenho()