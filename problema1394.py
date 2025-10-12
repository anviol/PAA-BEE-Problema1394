import sys
from collections import deque

# Fluxo máximo simples (Edmonds–Karp) para deixar o código mais didático
def construir_grafo(qtd_nos):
    return [[] for _ in range(qtd_nos)]

def adicionar_aresta(grafo, origem, destino, capacidade):
    grafo[origem].append([destino, capacidade, len(grafo[destino])])
    grafo[destino].append([origem, 0, len(grafo[origem]) - 1])

def fluxo_maximo(grafo, fonte, sorvedouro):
    fluxo = 0
    n = len(grafo)
    while True:
        pai = [(-1, -1)] * n  # (no_anterior, indice_aresta_no_anterior)
        fila = deque([fonte])
        pai[fonte] = (fonte, -1)
        while fila and pai[sorvedouro][0] == -1:
            u = fila.popleft()
            for idx, (v, cap, _) in enumerate(grafo[u]):
                if cap > 0 and pai[v][0] == -1:
                    pai[v] = (u, idx)
                    fila.append(v)
        if pai[sorvedouro][0] == -1:
            break  # não há mais caminho aumentante

        # Encontra gargalo
        gargalo = 10 ** 9
        v = sorvedouro
        while v != fonte:
            u, ei = pai[v]
            cap = grafo[u][ei][1]
            if cap < gargalo:
                gargalo = cap
            v = u

        # Aplica fluxo no caminho
        v = sorvedouro
        while v != fonte:
            u, ei = pai[v]
            destino, cap, rev = grafo[u][ei]
            grafo[u][ei][1] -= gargalo
            grafo[destino][rev][1] += gargalo
            v = u
        fluxo += gargalo
    return fluxo


# Função que determina se o time 0 pode ser campeão único
def pode_ser_campeao(N, M, G, jogos_informados):
    # Pontos atuais e jogos já jogados entre pares
    pontos = [0] * N
    jogos_jogados = [[0] * N for _ in range(N)]

    for jogo in jogos_informados:
        time_a, resultado, time_b = jogo.split()
        a = int(time_a)
        b = int(time_b)
        jogos_jogados[a][b] += 1
        jogos_jogados[b][a] += 1

        if resultado == "<":  # a perdeu de b
            pontos[b] += 2
        elif resultado == ">":  # a venceu b (se aparecer)
            pontos[a] += 2
        elif resultado == "=":  # empate
            pontos[a] += 1
            pontos[b] += 1
        else:
            return False

    # Considere que o time 0 vence todos os jogos restantes dele
    pontos0 = pontos[0]
    for oponente in range(1, N):
        restantes = M - jogos_jogados[0][oponente]
        if restantes < 0:
            return False
        pontos0 += 2 * restantes

    # Limites máximos de pontos dos outros times (devem ser estritamente menores que pontos0)
    limite = [0] * N
    for t in range(1, N):
        limite[t] = pontos0 - 1 - pontos[t]
        if limite[t] < 0:
            return False

    # Total de pontos a serem distribuídos em jogos entre times 1..N-1
    jogos_restantes_outros = []  # (i,j, qtd)
    total_pontos_necessarios = 0
    for i in range(1, N):
        for j in range(i + 1, N):
            restantes = M - jogos_jogados[i][j]
            if restantes < 0:
                return False
            if restantes > 0:
                jogos_restantes_outros.append((i, j, restantes))
                total_pontos_necessarios += 2 * restantes

    if total_pontos_necessarios == 0:
        # Sem jogos entre outros times; já garantimos limites
        return True

    # Constrói rede de fluxo: fonte -> jogo_k (cap 2*qtd), jogo_k -> i (2*qtd), jogo_k -> j (2*qtd), i -> sorvedouro (limite[i])
    num_jogos = len(jogos_restantes_outros)
    # Nós: [fonte] 0, nós de jogo 1..num_jogos, nós de times (1..N-1) depois
    fonte = 0
    primeiro_jogo = 1
    primeiro_time = primeiro_jogo + num_jogos
    sorvedouro = primeiro_time + (N - 1)
    grafo = construir_grafo(sorvedouro + 1)

    # Adiciona arestas dos jogos
    for k, (i, j, qtd) in enumerate(jogos_restantes_outros):
        no_jogo = primeiro_jogo + k
        adicionar_aresta(grafo, fonte, no_jogo, 2 * qtd)
        adicionar_aresta(grafo, no_jogo, primeiro_time + (i - 1), 2 * qtd)
        adicionar_aresta(grafo, no_jogo, primeiro_time + (j - 1), 2 * qtd)

    # Arestas dos times para o sorvedouro com sua capacidade limite
    for t in range(1, N):
        cap = max(0, limite[t])
        adicionar_aresta(grafo, primeiro_time + (t - 1), sorvedouro, cap)

    fluxo = fluxo_maximo(grafo, fonte, sorvedouro)
    return fluxo == total_pontos_necessarios

def principal():
    """
    Função principal para ler a entrada e chamar o resolvedor para cada caso de teste.
    """
    # Pega todas as linhas da entrada
    linhas = sys.stdin.readlines()

    # Índice para percorrer as linhas e controle de parada do loop
    idx = 0

    # Lista para armazenar os resultados de cada caso de teste
    saida = []

    # Loop principal para processar cada caso de teste
    while idx < len(linhas):

        # Lê a linha atual e avança o índice
        linha = linhas[idx].strip()

        # Se a linha estiver vazia, apenas avança o índice
        if not linha:
            idx += 1
            continue

        # Divide a linha em N, M e G
        N, M, G = map(int, linha.split())

        # Se N, M e G forem todos zero, termina o processamento
        if N == 0 and M == 0 and G == 0:
            # print(f"Fim do arquivo na linha {idx}")
            break

        # Avança o índice para a próxima linha
        idx += 1

        # Lê os jogos concluídos
        jogos_concluidos = []
        for _ in range(G):
            jogos_concluidos.append(linhas[idx].strip())
            # Avança o índice para a próxima linha lida
            idx += 1

        # Chama a função que resolve o problema e armazena o resultado
        if pode_ser_campeao(N, M, G, jogos_concluidos):
            saida.append(f"Y")
        else:
            saida.append(f"N")
    
    print("\n".join(saida))

if __name__ == "__main__":
    principal()