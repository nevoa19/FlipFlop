import os
import random
import time
import matplotlib.pyplot as plt

nos_expandidos = 0
nos_visitados = 0


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
    global nos_expandidos, nos_visitados
    nos_expandidos = 0

    fila = [ [e_inicial, [], 0] ]
    visitados = [e_inicial]

    while len(fila) > 0:
        elemento = fila.pop(0)
        nos_expandidos += 1

        e_atual = elemento[0]
        caminho = elemento[1]
        custo = elemento[2]

        if e_atual == e_alvo:
            nos_visitados = len(visitados)
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
    global nos_expandidos, nos_visitados
    nos_expandidos = 0

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
        nos_expandidos += 1

        e_atual = elemento[0]
        caminho = elemento[1]
        custo = elemento[2]

        if e_atual == e_alvo:
            nos_visitados = len(visitados)
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

def sequencia_de_zeros(tamanho):
    zeros = []
    cont = 0
    while cont < tamanho:
        zeros.append(0)
        cont += 1
    return zeros

def diferenca(a, b):
    d = []
    k = 0
    while k < len(a):
        if a[k] != b[k]:
            d.append(1)
        else:
            d.append(0)
        k += 1
    return d

def guloso_blocos(e_inicial, e_alvo):
    d = diferenca(e_inicial, e_alvo)
    operacoes = []
    i = 0
    while i < len(d):
        if d[i] == 1:
            j = i
            while j < len(d) and d[j] == 1:
                j += 1
            operacoes.append((i, j - i))
            i = j
        else:
            i += 1
    return operacoes, len(operacoes)

def avaliar_desempenho(L, N, usar_bfs, usar_greedy):
    soma_custo_bfs = 0
    soma_tempo_bfs = 0
    soma_exp_bfs = 0
    soma_vis_bfs = 0
    soma_custo_greedy = 0
    soma_tempo_greedy = 0
    soma_exp_greedy = 0
    soma_custo_blocos = 0
    soma_tempo_blocos = 0

    par = 0
    while par < N:
        inicio = gerar_sequencia(L)
        fim = gerar_sequencia(L)
        d = diferenca(inicio, fim)
        zeros = sequencia_de_zeros(L)

        if usar_bfs:
            t0 = time.perf_counter()
            caminho, custo = bfs(d, zeros)
            soma_tempo_bfs = soma_tempo_bfs + (time.perf_counter() - t0)
            soma_custo_bfs = soma_custo_bfs + custo
            soma_exp_bfs = soma_exp_bfs + nos_expandidos
            soma_vis_bfs = soma_vis_bfs + nos_visitados

        if usar_greedy:
            t0 = time.perf_counter()
            caminho, custo = greedy(d, zeros)
            soma_tempo_greedy = soma_tempo_greedy + (time.perf_counter() - t0)
            soma_custo_greedy = soma_custo_greedy + custo
            soma_exp_greedy = soma_exp_greedy + nos_expandidos

        t0 = time.perf_counter()
        caminho, custo = guloso_blocos(inicio, fim)
        soma_tempo_blocos = soma_tempo_blocos + (time.perf_counter() - t0)
        soma_custo_blocos = soma_custo_blocos + custo

        par += 1

    resultado = {}
    resultado["L"] = L
    resultado["custo_bfs"] = soma_custo_bfs / N
    resultado["tempo_bfs"] = soma_tempo_bfs / N
    resultado["exp_bfs"] = soma_exp_bfs / N
    resultado["vis_bfs"] = soma_vis_bfs / N
    resultado["custo_greedy"] = soma_custo_greedy / N
    resultado["tempo_greedy"] = soma_tempo_greedy / N
    resultado["exp_greedy"] = soma_exp_greedy / N
    resultado["custo_blocos"] = soma_custo_blocos / N
    resultado["tempo_blocos"] = soma_tempo_blocos / N
    return resultado

def coletar_dados(N):
    tamanhos = [2, 4, 8, 12, 16, 24, 32, 64, 128, 256, 512, 1024, 2048, 4096]
    limite_bfs = 12
    limite_greedy = 32
    dados = []

    i = 0
    while i < len(tamanhos):
        L = tamanhos[i]
        r = avaliar_desempenho(L, N, L <= limite_bfs, L <= limite_greedy)
        dados.append(r)
        print(f"L = {L:5d} | custo medio (blocos): {r['custo_blocos']:.2f} | (L+1)/4 = {(L + 1) / 4:.2f} | tempo blocos: {r['tempo_blocos']:.6f}s")
        i += 1
    return dados

def pegar(dados, chave, limite_inferior_zero=True):
    xs = []
    ys = []
    i = 0
    while i < len(dados):
        if dados[i][chave] > 0:
            xs.append(dados[i]["L"])
            ys.append(dados[i][chave])
        i += 1
    return xs, ys

def gerar_graficos_novos(dados):
    if not os.path.exists("resultados"):
        os.makedirs("resultados")

    plt.figure(figsize=(7, 4.5), dpi=200)
    teorico_x = []
    teorico_y = []
    i = 0
    while i < len(dados):
        teorico_x.append(dados[i]["L"])
        teorico_y.append((dados[i]["L"] + 1) / 4)
        i += 1
    plt.plot(teorico_x, teorico_y, 'k--', linewidth=1.5, label='(L+1)/4')
    xs, ys = pegar(dados, "custo_blocos")
    plt.plot(xs, ys, 's-', color='#0275d8', linewidth=2, label='guloso por blocos')
    xs, ys = pegar(dados, "custo_bfs")
    plt.plot(xs, ys, 'o', color='#d9534f', markersize=9, markerfacecolor='none', markeredgewidth=2, label='BFS')
    xs, ys = pegar(dados, "custo_greedy")
    plt.plot(xs, ys, '^', color='#f0ad4e', markersize=6, label='guloso (fila)')
    plt.xscale('log', base=2)
    plt.yscale('log')
    plt.xlabel('tamanho da sequencia ($L$)', fontsize=12)
    plt.ylabel('custo medio da solucao', fontsize=12)
    plt.title('custo medio por tamanho', fontsize=13, fontweight='bold')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig('resultados/fig_custo.png', dpi=200)
    plt.close()

    plt.figure(figsize=(7, 4.5), dpi=200)
    xs, ys = pegar(dados, "tempo_bfs")
    plt.plot(xs, ys, 'o-', color='#d9534f', linewidth=2, label='BFS')
    xs, ys = pegar(dados, "tempo_greedy")
    plt.plot(xs, ys, '^-', color='#f0ad4e', linewidth=2, label='guloso (fila)')
    xs, ys = pegar(dados, "tempo_blocos")
    plt.plot(xs, ys, 's-', color='#0275d8', linewidth=2, label='guloso por blocos')
    plt.xscale('log', base=2)
    plt.yscale('log')
    plt.xlabel('tamanho da sequencia ($L$)', fontsize=12)
    plt.ylabel('tempo medio por par (s)', fontsize=12)
    plt.title('tempo de execucao por tamanho', fontsize=13, fontweight='bold')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig('resultados/fig_tempo.png', dpi=200)
    plt.close()

    plt.figure(figsize=(7, 4.5), dpi=200)
    xs, ys = pegar(dados, "exp_bfs")
    plt.plot(xs, ys, 'o-', color='#d9534f', linewidth=2, label='BFS (expandidos)')
    xs, ys = pegar(dados, "vis_bfs")
    plt.plot(xs, ys, 'o--', color='#d9534f', linewidth=2, label='BFS (visitados)')
    xs, ys = pegar(dados, "exp_greedy")
    plt.plot(xs, ys, '^-', color='#f0ad4e', linewidth=2, label='guloso (expandidos)')
    plt.xscale('log', base=2)
    plt.yscale('log')
    plt.xlabel('tamanho da sequencia ($L$)', fontsize=12)
    plt.ylabel('estados (media por par)', fontsize=12)
    plt.title('esforco de busca', fontsize=13, fontweight='bold')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig('resultados/fig_estados.png', dpi=200)
    plt.close()

    plt.figure(figsize=(7, 4.5), dpi=200)
    xs = []
    vizinhos = []
    total = []
    L = 2
    while L <= 32:
        xs.append(L)
        vizinhos.append(L * (L + 1) / 2)
        total.append(2.0 ** L)
        L += 1
    plt.semilogy(xs, vizinhos, 's-', color='#0275d8', label='vizinhos por estado L(L+1)/2')
    plt.semilogy(xs, total, 'o-', color='#d9534f', label='estados totais $2^L$')
    plt.axvline(23, color='gray', ls=':')
    plt.xlabel('tamanho da sequencia ($L$)', fontsize=12)
    plt.ylabel('quantidade', fontsize=12)
    plt.title('tamanho do espaco de busca', fontsize=13, fontweight='bold')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig('resultados/fig_ramificacao.png', dpi=200)
    plt.close()

def gerar_grafico_caminho(e_inicial, caminho):
    estados = [e_inicial]
    atual = e_inicial
    i = 0
    while i < len(caminho):
        atual = flip(atual, caminho[i][0], caminho[i][1])
        estados.append(atual)
        i += 1

    nomes = ['inicial']
    i = 0
    while i < len(caminho):
        nomes.append(f"flip ({caminho[i][0]},{caminho[i][1]})")
        i += 1

    fig, ax = plt.subplots(figsize=(8, 3.2), dpi=200)
    ax.imshow(estados, cmap='Greys', aspect='auto', vmin=0, vmax=1.4)
    i = 0
    while i < len(caminho):
        ax.add_patch(plt.Rectangle((caminho[i][0] - 0.5, i + 0.5), caminho[i][1], 1, fill=False, edgecolor='#d9534f', linewidth=2))
        i += 1
    ax.set_yticks(range(len(estados)))
    ax.set_yticklabels(nomes)
    ax.set_xlabel('posicao do bit')
    ax.set_title('sequencia oficial passo a passo (borda = bloco invertido)', fontsize=9)
    plt.tight_layout()
    plt.savefig('resultados/fig_caminho.png', dpi=200)
    plt.close()


# ----------------------------------------------------------------------
# BFS da sequencia oficial (L = 23)
# A bfs (com listas) nao termina em L = 23
# como um numero inteiro e usa um dicionario para os visitados. Leva ~1 min.
# ----------------------------------------------------------------------
RODAR_BFS_OFICIAL = False

def bfs_inteiros(sequencia, L):
    inicial = 0
    k = 0
    while k < L:
        if sequencia[k] == 1:
            inicial = inicial + (1 << k)
        k += 1

    mascaras = []
    i = 0
    while i < L:
        n = 1
        while i + n <= L:
            mascaras.append((((1 << n) - 1) << i, i, n))
            n += 1
        i += 1

    anterior = {inicial: None}
    fila = [inicial]
    inicio_fila = 0
    expandidos = 0
    while inicio_fila < len(fila):
        s = fila[inicio_fila]
        inicio_fila += 1
        expandidos += 1
        k = 0
        while k < len(mascaras):
            v = s ^ mascaras[k][0]
            if v not in anterior:
                anterior[v] = (s, (mascaras[k][1], mascaras[k][2]))
                if v == 0:
                    caminho = []
                    atual = v
                    while anterior[atual] is not None:
                        caminho.append(anterior[atual][1])
                        atual = anterior[atual][0]
                    caminho.reverse()
                    return caminho, len(caminho), expandidos, len(anterior)
                fila.append(v)
            k += 1


seq_inicial = [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1]

seq_alvo = []
cont = 0
while cont < len(seq_inicial):
    seq_alvo.append(0)
    cont += 1

print("\nRESULTADO GULOSO")
t0 = time.perf_counter()
caminho_g, custo_g = greedy(seq_inicial, seq_alvo)
tempo_g = time.perf_counter() - t0
print(f"Custo: {custo_g}")
print(f"Operações (índice, tamanho): {caminho_g}")
print(f"nos expandidos: {nos_expandidos} | nos visitados: {nos_visitados} | tempo: {tempo_g:.4f}s")

if RODAR_BFS_OFICIAL:
    print("\nRESULTADO BFS (versao com inteiros)")
    t0 = time.perf_counter()
    caminho_b, custo_b, exp_b, vis_b = bfs_inteiros(seq_inicial, len(seq_inicial))
    print(f"Custo: {custo_b}")
    print(f"Operações (índice, tamanho): {caminho_b}")
    print(f"nos expandidos: {exp_b} | nos visitados: {vis_b} | tempo: {time.perf_counter() - t0:.2f}s")

if __name__ == "__main__":
    random.seed(2026)

    if not os.path.exists("resultados"):
        os.makedirs("resultados")
    gerar_grafico_caminho(seq_inicial, caminho_g)

    print("\nESTATISTICAS DE DESEMPENHO (20 pares por tamanho)")
    dados = coletar_dados(20)
    gerar_graficos_novos(dados)

    print("\ntabela completa:")
    i = 0
    while i < len(dados):
        r = dados[i]
        print(r)
        i += 1

    print("\nfiguras salvas na pasta resultados/")
