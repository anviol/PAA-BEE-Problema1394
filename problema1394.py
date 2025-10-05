import sys

# Função que determina se o time 1 pode ser campeão
def pode_ser_campeao(N, M, G, jogos_informados):
    
    # Inicializa a contagem de pontos e jogos jogados
    pontos = [0] * N
    jogos_jogados = [[0] * N for _ in range(N)]

    # Processa os jogos informados
    for jogo in jogos_informados:

        # Divide a string do jogo em time_a, resultado e time_b conforme primícias
        time_a, resultado, time_b = jogo.split()

        # Atualiza a contagem de jogos jogados entre os times
        jogos_jogados[int(time_a)][int(time_b)] += 1
        jogos_jogados[int(time_b)][int(time_a)] += 1

        # Atualiza a contagem de pontos conforme o resultado
        if resultado == "<":
            pontos[int(time_b)] += 2
        elif resultado == ">":
            pontos[int(time_a)] += 2
        else:
            pontos[int(time_a)] += 1
            pontos[int(time_b)] += 1

    return True

def main():
    """
    Função principal para ler a entrada e chamar o resolvedor para cada caso de teste.
    """
    # Pega todas as linhas da entrada
    linhas = sys.stdin.readlines()

    # Índice para percorrer as linhas e controle de parada do loop
    idx = 0

    # Lista para armazenar os resultados de cada caso de teste
    resultado = []

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
            print(f"Fim do arquivo na linha {idx}")
            break

        # Avança o índice para a próxima linha
        idx += 1

        # Lê os jogos concluídos
        jogos_concluidos = []
        for i in range(G):
            jogos_concluidos.append(linhas[idx + i].strip())

        # Avança o índice após ler os jogos concluídos
        idx += G

        # Chama a função que resolve o problema e armazena o resultado
        if pode_ser_campeao(N, M, G, jogos_concluidos):
            resultado.append(f"Y")
        else:
            resultado.append(f"N")
    
    print("\n".join(resultado))

if __name__ == "__main__":
    main()