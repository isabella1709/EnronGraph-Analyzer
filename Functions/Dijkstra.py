import heapq
import numpy as np

def dijkstra_distancia(grafo, source_node, d):
        visited = [] # lista de vértices visitados
        costs = {node: [np.inf, None] for node in grafo.graph}  # custo acumulado dos vértices
        costs[source_node][0] = 0
        heap = [(0, source_node)]  # fila de prioridade => (distância, vértice)

        # enquanto a fila não estiver vazia
        while heap:
            _, current_node = heapq.heappop(heap) # retorna elemento com o menor custo!
            if current_node not in visited:
                adjacent_nodes = grafo.get_adjacent(current_node)
                # vértices adjacentes do vértice atual
                for adj in adjacent_nodes:
                    if adj not in visited:
                        # custo acumulado do vértice atual até o adj
                        accumulated_cost = costs[current_node][0] + grafo.get_weight(current_node, adj)
                        # atualiza o custo e vértice de origem se o custo calculado for menor
                        if accumulated_cost < costs[adj][0]:
                            costs[adj][0] = accumulated_cost
                            costs[adj][1] = current_node
                            if costs[adj][0] <= d: # se dentro da distância D
                                heapq.heappush(heap, (accumulated_cost, adj)) # adiciona na fila
                visited.append(current_node) # coloca como visitado
        return visited

def dijkstra_diametro(grafo):
    diametro = 0
    caminho_mais_longo = []

    for origem in grafo.graph:
        visitados = [] 
        custos = {no: [np.inf, None] for no in grafo.graph}  # innicializar como infinito e nó pai
        custos[origem][0] = 0  #  comeca com custo 0 no nó de origem
        fila = [(0, origem)]  # fila de prioridade (custo, nó)

        while fila:
            _, no_atual = heapq.heappop(fila)  # pega o nó com o menor custo
            if no_atual not in visitados:
                # pega todos os vizinhos do nó atual
                vizinhos = grafo.get_adjacent(no_atual)

                for vizinho in vizinhos:
                    if vizinho not in visitados:
                        # calcula o custo acumulado até esse vizinho
                        custo_acumulado = custos[no_atual][0] + grafo.get_weight(no_atual, vizinho)
                        if custo_acumulado < custos[vizinho][0]:  # se novo custo < anterior, atualiza
                            custos[vizinho][0] = custo_acumulado
                            custos[vizinho][1] = no_atual
                            heapq.heappush(fila, (custo_acumulado, vizinho))  # adiciona na fila

                visitados.append(no_atual)

        # pega menor caminho de todos os pontos para todos
        # verifica qual é o maior menor caminho de todos
        for destino in grafo.graph:
            distancia = custos[destino][0]
            if distancia != np.inf and distancia > diametro: 
                diametro = distancia 

                # reconstruir caminho até o destino para pegar todos os custos
                caminho = []
                atual = destino
                while atual is not None:
                    caminho.insert(0, atual)  # insere no início para formar o caminho na ordem certa
                    atual = custos[atual][1]  # vai para o pai do atual
                caminho_mais_longo = caminho  # atualiza o caminho mais longo encontrado

    return diametro, caminho_mais_longo