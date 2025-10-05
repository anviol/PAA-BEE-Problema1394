import sys

# Implementação do Algoritmo de Edmonds-Karp para Fluxo Máximo
def bfs(graph, s, t, parent):
    """
    Busca em largura para encontrar um caminho de aumento no grafo residual.
    """
    visited = [False] * len(graph)
    queue = []
    queue.append(s)
    visited[s] = True
    parent[s] = -1
    while queue:
        u = queue.pop(0)
        for v, capacity in enumerate(graph[u]):
            if not visited[v] and capacity > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == t:
                    return True
    return False

def edmonds_karp(graph, source, sink):
    """
    Calcula o fluxo máximo de uma fonte para um sumidouro em um grafo.
    """
    parent = [0] * len(graph)
    max_flow = 0
    while bfs(graph, source, sink, parent):
        path_flow = float('Inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]

        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]

        max_flow += path_flow
    return max_flow

def pode_ser_campeao(N, M, G, jogos_data):
    """
    Lógica principal para determinar se o time 0 pode ser campeão,
    modelando o problema como um de fluxo máximo.
    """
    pontos = [0] * N
    jogos_jogados = [[0] * N for _ in range(N)]

    for jogo_str in jogos_data:
        partes = jogo_str.split()
        time_i, comp, time_j = int(partes[0]), partes[1], int(partes[2])

        jogos_jogados[time_i][time_j] += 1
        jogos_jogados[time_j][time_i] += 1

        if comp == '<':
            pontos[time_j] += 2
        elif comp == '=':
            pontos[time_i] += 1
            pontos[time_j] += 1

    # Calcular a pontuação máxima possível para o time 0
    pontuacao_max_time_0 = pontos[0]
    for i in range(1, N):
        jogos_restantes_time_0 = M - jogos_jogados[0][i]
        pontuacao_max_time_0 += 2 * jogos_restantes_time_0

    # Identificar jogos restantes que não envolvem o time 0
    jogos_restantes = []
    for i in range(1, N):
        for j in range(i + 1, N):
            num_jogos = M - jogos_jogados[i][j]
            for _ in range(num_jogos):
                jogos_restantes.append((i, j))

    total_pontos_jogos_restantes = 2 * len(jogos_restantes)

    # Construir a rede de fluxo
    # Nós: 0=source, 1=sink, [2, 2+len(jogos_restantes)-1]=jogos, [2+len(jogos_restantes), ...]=times
    num_nos_jogo = len(jogos_restantes)
    num_nos_time = N - 1
    total_nos = 2 + num_nos_jogo + num_nos_time

    source = 0
    sink = 1

    capacidade = [[0] * total_nos for _ in range(total_nos)]

    # Mapeamento de time para nó
    time_para_no = {i: 2 + num_nos_jogo + (i - 1) for i in range(1, N)}

    # Arestas: source -> jogos
    for idx, jogo in enumerate(jogos_restantes):
        no_jogo = 2 + idx
        capacidade[source][no_jogo] = 2

        # Arestas: jogos -> times
        time_i, time_j = jogo
        no_time_i = time_para_no[time_i]
        no_time_j = time_para_no[time_j]
        capacidade[no_jogo][no_time_i] = 2
        capacidade[no_jogo][no_time_j] = 2

    # Arestas: times -> sink
    for i in range(1, N):
        no_time = time_para_no[i]
        limite_pontos = pontuacao_max_time_0 - 1 - pontos[i]

        if limite_pontos < 0:
            return False # Impossível, time já tem mais pontos

        capacidade[no_time][sink] = limite_pontos

    fluxo_maximo = edmonds_karp(capacidade, source, sink)

    return fluxo_maximo == total_pontos_jogos_restantes


def main():
    """
    Função principal para ler a entrada e chamar o resolvedor para cada caso de teste.
    """
    linhas = sys.stdin.readlines()
    idx = 0
    while idx < len(linhas):
        linha = linhas[idx].strip()
        if not linha:
            idx += 1
            continue

        N, M, G = map(int, linha.split())
        if N == 0 and M == 0 and G == 0:
            break

        idx += 1
        jogos_concluidos = []
        for i in range(G):
            jogos_concluidos.append(linhas[idx + i].strip())
        idx += G

        if pode_ser_campeao(N, M, G, jogos_concluidos):
            print('Y')
        else:
            print('N')

if __name__ == "__main__":
    main()