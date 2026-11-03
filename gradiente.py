
def calcular_loss(e_atual):
    soma_quadrados = 0
    i = 0
    while i < len(e_atual):
        # L(x) = (1/2) * x^2
        soma_quadrados = soma_quadrados + (0.5 * (e_atual[i] ** 2))
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

def gradiente_descendente(seq_inicial, alfa, tolerancia):
    x_atual = []
    for valor in seq_inicial:
        x_atual.append(float(valor)) 
        
    epoca = 0
    loss = calcular_loss(x_atual)
    
    while loss > tolerancia:
        if epoca % 10 == 0:
            print(f"Epoca {epoca:3d} | Loss: {loss:.6f}")
            
        i = 0
        while i < len(x_atual):
            gradiente = x_atual[i] 
            x_atual[i] = x_atual[i] - (alfa * gradiente)
            i += 1
            
        loss = calcular_loss(x_atual)
        epoca += 1
        
    print(f"Epoca {epoca:3d} | Loss Final: {loss:.6f}")
    return x_atual, epoca


seq_inicial_oficial = [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1]

taxa_aprendizagem = 0.1 
tolerancia_erro = 0.0001 

print("OTIMIZACAO CONTINUA")
resultado_continuo, total_epocas = gradiente_descendente(seq_inicial_oficial, taxa_aprendizagem, tolerancia_erro)

resultado_discreto = binarizar_sequencia(resultado_continuo)

print(f"\nconvergencia alcançada em {total_epocas} iteracoes.")
print(f"sequencia inicial:   {seq_inicial_oficial}")
print(f"sequencia binarizada:{resultado_discreto}")