import os
import random
import matplotlib.pyplot as plt

def calcular_loss(e_atual, alvo):
    soma_quadrados = 0
    i = 0
    while i < len(e_atual):
        # L(x) = (x - y)^2
        diferenca = e_atual[i] - alvo[i]
        soma_quadrados = soma_quadrados + (diferenca * diferenca)
        i += 1
    return soma_quadrados

def binarizar_sequencia(e_continuo):
    e_discreto = []
    i = 0
    while i < len(e_continuo):
        if e_continuo[i] < 0.5:
            e_discreto.append(0)
        else:
            e_discreto.append(1)
        i += 1
    return e_discreto

def gradiente_descendente(seq_inicial, alvo, alfa, tolerancia):
    x_atual = []
    for valor in seq_inicial:
        x_atual.append(float(valor))

    epoca = 0
    loss = calcular_loss(x_atual, alvo)

    while loss > tolerancia:
        if epoca % 10 == 0:
            print(f"Epoca {epoca:3d} | Loss: {loss:.6f}")

        i = 0
        while i < len(x_atual):
            # dL/dx = 2 (x - y)
            gradiente = 2 * (x_atual[i] - alvo[i])
            x_atual[i] = x_atual[i] - (alfa * gradiente)
            i += 1

        loss = calcular_loss(x_atual, alvo)
        epoca += 1

    print(f"Epoca {epoca:3d} | Loss Final: {loss:.6f}")
    return x_atual, epoca

def copiar(lista):
    nova = []
    for v in lista:
        nova.append(v)
    return nova

def calcular_z(x, alvo):
    # z_k = g_k^2, com g_k = dL/dx_k = 2 (x_k - y_k) 
    z = []
    i = 0
    while i < len(x):
        g = 2 * (x[i] - alvo[i])
        z.append(g * g)
        i += 1
    return z

def calcular_custo(z):
    # C(z) = soma (z_{k+1} - z_k)^2
    soma = 0
    i = 0
    while i < len(z) - 1:
        d = z[i + 1] - z[i]
        soma = soma + d * d
        i += 1
    return soma

def calcular_J(x, alvo, lam):
    return calcular_loss(x, alvo) + lam * calcular_custo(calcular_z(x, alvo))

def gradiente_J(x, alvo, lam):
    #dJ/dx_i = g_i + lam * dC/dz_i * dz_i/dx_i   (dz_i/dx_i = 4 g_i)
    n = len(x)
    g = []
    z = []
    i = 0
    while i < n:
        gi = 2 * (x[i] - alvo[i])
        g.append(gi)
        z.append(gi * gi)
        i += 1

    grad = []
    i = 0
    while i < n:
        dC = 0
        if i > 0:
            dC = dC + 2 * (z[i] - z[i - 1])
        if i < n - 1:
            dC = dC - 2 * (z[i + 1] - z[i])
        grad.append(g[i] + lam * dC * 4 * g[i])
        i += 1
    return grad

def conferir_gradiente(n_testes, L):
    pior = 0
    t = 0
    while t < n_testes:
        x = []
        y = []
        k = 0
        while k < L:
            x.append(random.random())
            y.append(random.choice([0, 1]))
            k += 1
        lam = random.uniform(0, 2)
        analitico = gradiente_J(x, y, lam)
        h = 0.000001
        k = 0
        while k < L:
            x_mais = copiar(x)
            x_menos = copiar(x)
            x_mais[k] = x_mais[k] + h
            x_menos[k] = x_menos[k] - h
            numerico = (calcular_J(x_mais, y, lam) - calcular_J(x_menos, y, lam)) / (2 * h)
            dif = analitico[k] - numerico
            if dif < 0:
                dif = -dif
            if dif > pior:
                pior = dif
            k += 1
        t += 1
    return pior

def descer(x0, alvo, eta, lam, max_passos, tolerancia):
    trajetoria = [copiar(x0)]
    x = copiar(x0)
    passo = 0
    while passo < max_passos:
        if lam == 0:
            grad = []
            i = 0
            while i < len(x):
                grad.append(2 * (x[i] - alvo[i]))
                i += 1
        else:
            grad = gradiente_J(x, alvo, lam)

        i = 0
        while i < len(x):
            x[i] = x[i] - eta * grad[i]
            i += 1
        trajetoria.append(copiar(x))
        passo += 1

        if calcular_loss(x, alvo) < tolerancia:
            break

        divergiu = False
        i = 0
        while i < len(x):
            if x[i] > 1000000 or x[i] < -1000000 or x[i] != x[i]:
                divergiu = True
            i += 1
        if divergiu:
            break
    return trajetoria

def menor_valor(trajetoria):
    menor = trajetoria[0][0]
    t = 0
    while t < len(trajetoria):
        k = 0
        while k < len(trajetoria[t]):
            if trajetoria[t][k] < menor:
                menor = trajetoria[t][k]
            k += 1
        t += 1
    return menor

def contar_blocos(v):
    blocos = 0
    em_bloco = False
    i = 0
    while i < len(v):
        if v[i] == 1:
            if em_bloco == False:
                blocos += 1
                em_bloco = True
        else:
            em_bloco = False
        i += 1
    return blocos

def flips_equivalentes(trajetoria):
    total = 0
    t = 0
    while t < len(trajetoria) - 1:
        antes = binarizar_sequencia(trajetoria[t])
        depois = binarizar_sequencia(trajetoria[t + 1])
        mudou = []
        k = 0
        while k < len(antes):
            if antes[k] != depois[k]:
                mudou.append(1)
            else:
                mudou.append(0)
            k += 1
        total = total + contar_blocos(mudou)
        t += 1
    return total

def transpor(trajetoria, ate):
    # linha = posicao do bit, coluna = passo (para o imshow)
    matriz = []
    k = 0
    while k < len(trajetoria[0]):
        linha = []
        t = 0
        while t < len(trajetoria) and t < ate:
            linha.append(trajetoria[t][k])
            t += 1
        matriz.append(linha)
        k += 1
    return matriz

def grafico_eta(x0, alvo):
    etas = [0.1, 0.25, 0.5, 0.75, 1.0]
    cores = ['#1f77b4', '#2ca02c', '#9467bd', '#ff7f0e', '#d62728']
    fig, eixos = plt.subplots(1, 2, figsize=(10, 3.8), dpi=200)
    i = 0
    while i < len(etas):
        tr = descer(x0, alvo, etas[i], 0, 20, 0)
        bit4 = []
        perdas = []
        t = 0
        while t < len(tr):
            bit4.append(tr[t][4])
            perdas.append(calcular_loss(tr[t], alvo) + 1e-30)
            t += 1
        eixos[0].plot(bit4, 'o-', markersize=3, color=cores[i], label=f"$\\eta={etas[i]}$")
        eixos[1].plot(perdas, color=cores[i], label=f"$\\eta={etas[i]}$")
        i += 1
    eixos[0].axhspan(-0.6, 0, color='#f4cccc', alpha=0.5)
    eixos[0].axhline(0, color='k', linewidth=0.5)
    eixos[0].set_title('bit 4 (1 -> 0): faixa rosa = fora de [0,1]', fontsize=9)
    eixos[0].set_xlabel('iteracao')
    eixos[0].set_ylabel('$x_4$')
    eixos[0].legend(fontsize=7)
    eixos[1].set_yscale('log')
    eixos[1].set_ylim(0.000000000001, 1000)
    eixos[1].set_title('erro $L(x_t)$', fontsize=9)
    eixos[1].set_xlabel('iteracao')
    plt.tight_layout()
    plt.savefig('resultados/fig_eta.png', dpi=200)
    plt.close()

def grafico_delta(x0, alvo, eta):
    tr = descer(x0, alvo, eta, 0, 12, 0)
    deltas = []
    k = 0
    while k < len(x0):
        linha = []
        t = 0
        while t < len(tr) - 1:
            linha.append(tr[t + 1][k] - tr[t][k])
            t += 1
        deltas.append(linha)
        k += 1
    fig, ax = plt.subplots(figsize=(8, 3.2), dpi=200)
    im = ax.imshow(deltas, aspect='auto', cmap='RdBu', vmin=-0.55, vmax=0.55)
    ax.set_xlabel('passo $t$')
    ax.set_ylabel('posicao $k$')
    ax.set_title(f"transformacoes $\\Delta x_t$ ($\\eta={eta}$, sem custo)", fontsize=10)
    plt.colorbar(im, ax=ax, label='$\\Delta x_k$')
    plt.tight_layout()
    plt.savefig('resultados/fig_delta.png', dpi=200)
    plt.close()

def grafico_lambda(x0, alvo, eta, lambdas):
    fig, eixos = plt.subplots(2, len(lambdas), figsize=(3 * len(lambdas), 5.2), dpi=200)
    j = 0
    while j < len(lambdas):
        tr = descer(x0, alvo, eta, lambdas[j], 60, 0.000000001)
        eixos[0][j].imshow(transpor(tr, 60), aspect='auto', cmap='coolwarm', vmin=-0.3, vmax=1.3)
        eixos[0][j].set_title(f"$\\lambda={lambdas[j]}$", fontsize=10)
        eixos[0][j].set_xlabel('iteracao')
        custos = []
        t = 0
        while t < len(tr):
            custos.append(calcular_custo(calcular_z(tr[t], alvo)) + 1e-30)
            t += 1
        eixos[1][j].semilogy(custos, color='#0275d8')
        eixos[1][j].set_xlabel('iteracao')
        eixos[1][j].grid(alpha=0.3)
        if j == 0:
            eixos[0][j].set_ylabel('posicao $k$')
            eixos[1][j].set_ylabel('$C(z_t)$')
        j += 1
    plt.tight_layout()
    plt.savefig('resultados/fig_lambda.png', dpi=200)
    plt.close()


seq_inicial_oficial = [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1]

seq_alvo_oficial = []
cont = 0
while cont < len(seq_inicial_oficial):
    seq_alvo_oficial.append(0)
    cont += 1

taxa_aprendizagem = 0.1
tolerancia_erro = 0.0001

print("OTIMIZACAO CONTINUA")
resultado_continuo, total_epocas = gradiente_descendente(seq_inicial_oficial, seq_alvo_oficial, taxa_aprendizagem, tolerancia_erro)

resultado_discreto = binarizar_sequencia(resultado_continuo)

print(f"\nconvergencia alcançada em {total_epocas} iteracoes.")
print(f"sequencia inicial:   {seq_inicial_oficial}")
print(f"sequencia binarizada:{resultado_discreto}")


if __name__ == "__main__":
    random.seed(2026)
    if not os.path.exists("resultados"):
        os.makedirs("resultados")

    x0 = []
    for valor in seq_inicial_oficial:
        x0.append(float(valor))

    print("\nEFEITO DA TAXA DE APRENDIZADO (sem custo, tolerancia 1e-6)")
    etas = [0.1, 0.25, 0.5, 0.75, 1.0, 1.05]
    i = 0
    while i < len(etas):
        tr = descer(x0, seq_alvo_oficial, etas[i], 0, 200, 0.000001)
        print(f"eta = {etas[i]:5} | passos: {len(tr) - 1:3d} | menor x: {menor_valor(tr):+.3f} | loss final: {calcular_loss(tr[len(tr) - 1], seq_alvo_oficial):.3e} | flips equivalentes: {flips_equivalentes(tr)}")
        i += 1

    tr = descer(x0, seq_alvo_oficial, 0.75, 0, 3, 0)
    print("\neta = 0.75, bit 4 nos primeiros passos:", tr[0][4], tr[1][4], tr[2][4], tr[3][4])

    print("\nCONFERENCIA DO GRADIENTE DE J (analitico x diferencas finitas)")
    print("maior diferenca:", conferir_gradiente(25, 23))

    print("\nEFEITO DE LAMBDA (eta = 0.05, tolerancia 1e-6)")
    eta = 0.05
    lambdas = [0, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0]
    j = 0
    while j < len(lambdas):
        tr = descer(x0, seq_alvo_oficial, eta, lambdas[j], 1000, 0.000001)
        soma_C = 0
        t = 0
        while t < len(tr):
            soma_C = soma_C + calcular_custo(calcular_z(tr[t], seq_alvo_oficial))
            t += 1
        c10 = calcular_custo(calcular_z(tr[min(10, len(tr) - 1)], seq_alvo_oficial))
        print(f"lambda = {lambdas[j]:4} | passos: {len(tr) - 1:4d} | C medio: {soma_C / len(tr):.4g} | C(z_10): {c10:.4g} | menor x: {menor_valor(tr):+.3f} | loss final: {calcular_loss(tr[len(tr) - 1], seq_alvo_oficial):.3e} | flips: {flips_equivalentes(tr)}")
        j += 1

    grafico_eta(x0, seq_alvo_oficial)
    grafico_delta(x0, seq_alvo_oficial, 0.25)
    grafico_lambda(x0, seq_alvo_oficial, eta, [0, 0.1, 0.2, 0.3])
    print("\nfiguras salvas na pasta resultados/")