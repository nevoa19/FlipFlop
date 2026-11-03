# FlipFlop

Mini-projeto 00 (IA): transformação de sequências de bits por BFS, busca gulosa e gradiente descendente.

## Requisitos
- Python 3.8 ou superior (testado com 3.12)
- matplotlib

    pip install matplotlib

## Como executar

### Parte I: buscas clássicas
    python greedyBFS-flipflop.py

Executa a busca gulosa na sequência oficial (L = 23), sorteia 20 pares por tamanho
e compara BFS, gulosa com listas e gulosa por blocos.
Tempo aproximado: alguns minutos (a BFS com listas é executada até L = 12).

BFS da sequência oficial (opcional, ~45 s): alterar `RODAR_BFS_OFICIAL = False`
para `True` no início da seção correspondente do arquivo.

### Parte II: gradiente descendente
    python gradiente.py

Executa o gradiente descendente na sequência oficial, varia a taxa de aprendizado (η)
e o peso do custo (λ) e confere o gradiente analítico por diferenças finitas.

## Saídas
As figuras são salvas em `resultados/`:
fig_caminho, fig_custo, fig_tempo, fig_estados, fig_ramificacao (Parte I) e
fig_eta, fig_delta, fig_lambda (Parte II).
Os valores numéricos são impressos no terminal.