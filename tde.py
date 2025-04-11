import os
import re
from collections import defaultdict
import heapq
import numpy as np

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.order = 0
        self.size = 0

    def __str__(self):
        return self.print_adj_list()

    def save_adj_list(self, txt):
        with open(txt, "w") as f:
            for v in self.graph:
                linha = f"{v}: "
                for edge in self.graph[v]:
                    linha += f"('{edge[0]}', {edge[1]}) -> "
                linha = linha.rstrip(" -> ")
                f.write(linha + "\n")

    def node_exists(self, v):
        if v in self.graph:
            return v in self.graph
        else:
            return False

    def edge_exists(self, u, v):
        for edge in self.graph[u]:
            if edge[0] == v:
                return True
        return False

    def enter_degree(self, u):
        if self.node_exists(u):
          count = 0
          for v in self.graph:
              for edge in self.graph[v]:
                  if edge[0] == u:
                      count += 1
          return count
        else:
            return None

    def out_degree(self, u):
        if self.node_exists(u):
            return len(self.graph[u])
        else:
            return None

    def degree(self, u):
        if self.node_exists(u):
            return self.enter_degree(u) + self.out_degree(u)
        else:
            return None

    def get_weight(self, u, v):
        for edge in self.graph[u]:
            if edge[0] == v:
                return edge[1]
        return None

    def valid_weight(self, w):
        if w > 0:
            return True
        else:
            print("The weight cannot be negative!")
            return False

    def add_node(self, v):
        if self.node_exists(v):
            print("This node already exists in the graph!")
        else:
            self.graph[v] = []
            self.order += 1

    def add_edge(self, u, v, w):
        if self.valid_weight(w):
            if not self.node_exists(u):
                self.add_node(u)
            if not self.node_exists(v):
                self.add_node(v)

            if self.edge_exists(u, v):
                for i in range(len(self.graph[u])):
                    if self.graph[u][i][0] == v:
                        self.graph[u][i] = (v, w)
            else:
                self.graph[u].append((v, w))
                self.size += 1
            return True
        else:
            return False

    def remove_edge(self, u, v):
        if (self.node_exists(u) and self.node_exists(v)) and (self.edge_exists(u, v)):
            temp_size = len(self.graph[u])
            self.graph[u] = [edge for edge in self.graph[u] if edge[0] != v]
            remove_size = temp_size - len(self.graph[u])
            self.size -= remove_size
        else:
            print(f"Edge ({u, v}) cannot be removed!")

    def remove_node(self, v):
        if self.node_exists(v):
            self.size -= len(self.graph[v])
            self.graph.pop(v)
            self.order -= 1

            for u in self.graph:
                temp_size = len(self.graph[u])
                self.graph[u] = [edge for edge in self.graph[u] if edge[0] != v]
                remove_size = temp_size - len(self.graph[u])
                self.size -= remove_size
        else:
            print(f"Node {v} cannot be removed")
            
    def get_adjacent(self, node):
        return [item[0] for item in self.graph[node]]


    def dijkstra_distancia(self, source_node, d):
        visited = [] # lista de vértices visitados
        costs = {node: [np.inf, None] for node in self.graph}  # custo acumulado dos vértices
        costs[source_node][0] = 0
        heap = [(0, source_node)]  # fila de prioridade => (distância, vértice)

        # enquanto a fila não estiver vazia
        while heap:
            _, current_node = heapq.heappop(heap) # retorna elemento com o menor custo!
            if current_node not in visited:
                adjacent_nodes = self.get_adjacent(current_node)
                # vértices adjacentes do vértice atual
                for adj in adjacent_nodes:
                    if adj not in visited:
                        # custo acumulado do vértice atual até o adj
                        accumulated_cost = costs[current_node][0] + self.get_weight(current_node, adj)
                        # atualiza o custo e vértice de origem se o custo calculado for menor
                        if accumulated_cost < costs[adj][0]:
                            costs[adj][0] = accumulated_cost
                            costs[adj][1] = current_node
                            if costs[adj][0] <= d: # se dentro da distância D
                                heapq.heappush(heap, (accumulated_cost, adj)) # adiciona na fila
                visited.append(current_node) # coloca como visitado
        return visited

# PART 1
path = "Amostra Enron - 2016/"
caminhos = os.listdir(path)

grafo = Graph()

for caminho in caminhos:
    c = path + caminho + "/"
    caminhos2 = os.listdir(c)

    for caminho2 in caminhos2:
        caminho3 = c + caminho2 + "/"
        arquivos = os.listdir(caminho3)

        for arquivo in arquivos:
            caminho_arquivo = caminho3 + arquivo

            if not os.path.isfile(caminho_arquivo):
                continue

            with open(caminho_arquivo, "r") as a:
                conteudo = a.read()
           
            f = r'(?:From:)\s([\w.-]+@[\w.-]+)'
            emails_from = re.findall(f, conteudo)
            emails_to = []

            to_pattern = r'To:(.*?)(?:\n\S|$)'
            to_match = re.search(to_pattern, conteudo, re.DOTALL | re.IGNORECASE)

            if to_match:
                raw_destinatarios = to_match.group(1).replace('\n', ' ') 
                candidatos = re.findall(r'[\w\.-]+@[\w\.-]+', raw_destinatarios)
                emails_to = [email.lower() for email in candidatos]

            if emails_from and emails_to:
                remetente = emails_from[0].lower()
                destinatarios = emails_to

                destinatarios_filtrados = []

                for d in destinatarios:
                    if "@" in d:
                        d = d.strip().lower()
                        destinatarios_filtrados.append(d)

                destinatarios = destinatarios_filtrados
                
                if not destinatarios:
                    continue
         
                for destinatario in destinatarios:
                    if grafo.edge_exists(remetente, destinatario):
                        peso_atual = grafo.get_weight(remetente, destinatario)
                        grafo.add_edge(remetente, destinatario, peso_atual + 1)
                    else:
                        grafo.add_edge(remetente, destinatario, 1)

grafo.save_adj_list("lista_de_adjacencias.txt")


# PART 2

def getOrder(graph):
    return graph.order

print(f"Graph order: {getOrder(grafo)}")

def getSize(graph):
    return graph.size

print(f"Graph size: {getSize(grafo)}")

def getIsolatedVertices(graph):
    count = 0
    for key in graph.graph:
        if graph.graph[key] == []:
            count +=1

    return count

print(f"Graph isolated vertices: {getIsolatedVertices(grafo)}\n")

def getMaximumOutDegrees(graph):
    vertices = []

    for key in graph.graph:
        outDegree = graph.out_degree(key)
        vertices.append((key, outDegree))

    sortedVertices = sorted(vertices, key=lambda x: x[1], reverse=True)

    return sortedVertices[:20]


print(f"Graph top 20 vertices with highest out-degree of the graph: \n")

for i in range(0, len(getMaximumOutDegrees(grafo))):
    print(f"{i + 1}: Email: {getMaximumOutDegrees(grafo)[i][0]} | Out Degree: {getMaximumOutDegrees(grafo)[i][1]}")

def getMaximumEnterDegrees(graph):
    vertices = []

    for key in graph.graph:
        enterDegree = graph.enter_degree(key)
        vertices.append((key, enterDegree))

    sortedVertices = sorted(vertices, key=lambda x: x[1], reverse=True)

    return sortedVertices[:20]

print(f"\nGraph top 20 vertices with highest in-degree of the graph: \n")

for i in range(0, len(getMaximumEnterDegrees(grafo))):
    print(f"{i + 1}: Email: {getMaximumEnterDegrees(grafo)[i][0]} | Enter Degree: {getMaximumEnterDegrees(grafo)[i][1]}")


# PART 3
def conexo(graph):
    def dfs(v, visited, g):
        visited.add(v)
        for neighbor in g.graph[v]:
            if neighbor[0] not in visited:
                dfs(neighbor[0], visited, g)

    if not graph.graph:
        return True  # grafo vazio é considerado fortemente conexo

    start_node = next(iter(graph.graph))
    visited = set()
    dfs(start_node, visited, graph)
    if len(visited) != len(graph.graph):
        return False

    # cria o grafo transposto
    transposto = Graph()
    for u in graph.graph:
        for v, w in graph.graph[u]:
            transposto.add_edge(v, u, w) # aresta invertida

    visited = set()
    dfs(start_node, visited, transposto)
    if len(visited) != len(transposto.graph):
        return False

    return True


def eureliano(graph, nome_arquivo_saida):
    eureliano = True
    motivos = []
    balanceados = []

    if not conexo(graph):
        eureliano = False
        motivos.append("O grafo não é fortemente conexo.")

    for node in graph.graph:
        in_degree = graph.enter_degree(node)
        out_degree = graph.out_degree(node)
        if in_degree != out_degree:
            eureliano = False
            motivos.append(f"O vértice '{node}' tem grau de entrada {in_degree} e grau de saída {out_degree}.")
        else: 
            balanceados.append(f"O vértice '{node}' tem grau de entrada e saída iguais: {in_degree}.")
    with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
        f.write("🔎 Verificação de Eulerianidade do grafo:\n")
        if eureliano:
            f.write("O grafo é Eureliiano.\n")
        else:
            f.write("O grafo NÃO é Eureliano. Motivos:\n")
            for motivo in motivos:
                f.write(f" - {motivo}\n")
        f.write(" Vértices com grau de entrada igual ao grau de saída:\n")
        for linha in balanceados:
            f.write(f" - {linha}\n")

    return eureliano


eureliano(grafo, "verificacao_eureliano.txt")

def conexo(graph):
    def dfs(v, visited, g):
        visited.add(v)
        for neighbor in g.graph[v]:
            if neighbor[0] not in visited:
                dfs(neighbor[0], visited, g)

    if not graph.graph:
        return True  # grafo vazio é considerado fortemente conexo

    start_node = next(iter(graph.graph))
    visited = set()
    dfs(start_node, visited, graph)
    if len(visited) != len(graph.graph):
        return False

    # cria o grafo transposto
    transposto = Graph()
    for u in graph.graph:
        for v, w in graph.graph[u]:
            transposto.add_edge(v, u, w) # aresta invertida

    visited = set()
    dfs(start_node, visited, transposto)
    if len(visited) != len(transposto.graph):
        return False

    return True


def eureliano(graph, nome_arquivo_saida):
    eureliano = True
    motivos = []
    balanceados = []

    if not conexo(graph):
        eureliano = False
        motivos.append("O grafo não é fortemente conexo.")

    for node in graph.graph:
        in_degree = graph.enter_degree(node)
        out_degree = graph.out_degree(node)
        if in_degree != out_degree:
            eureliano = False
            motivos.append(f"O vértice '{node}' tem grau de entrada {in_degree} e grau de saída {out_degree}.")
        else: 
            balanceados.append(f"O vértice '{node}' tem grau de entrada e saída iguais: {in_degree}.")
    with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
        f.write("🔎 Verificação de Eulerianidade do grafo:\n")
        if eureliano:
            f.write("O grafo é Eureliiano.\n")
        else:
            f.write("O grafo NÃO é Eureliano. Motivos:\n")
            for motivo in motivos:
                f.write(f" - {motivo}\n")
        f.write(" Vértices com grau de entrada igual ao grau de saída:\n")
        for linha in balanceados:
            f.write(f" - {linha}\n")

    return eureliano


eureliano(grafo, "verificacao_eureliano.txt")


def conexo(graph):
    def dfs(v, visited, g):
        visited.add(v)
        for neighbor in g.graph[v]:
            if neighbor[0] not in visited:
                dfs(neighbor[0], visited, g)

    if not graph.graph:
        return True  # grafo vazio é considerado fortemente conexo

    start_node = next(iter(graph.graph))
    visited = set()
    dfs(start_node, visited, graph)
    if len(visited) != len(graph.graph):
        return False

    # cria o grafo transposto
    transposto = Graph()
    for u in graph.graph:
        for v, w in graph.graph[u]:
            transposto.add_edge(v, u, w) # aresta invertida

    visited = set()
    dfs(start_node, visited, transposto)
    if len(visited) != len(transposto.graph):
        return False

    return True


def eureliano(graph, nome_arquivo_saida):
    eureliano = True
    motivos = []
    balanceados = []

    if not conexo(graph):
        eureliano = False
        motivos.append("O grafo não é fortemente conexo.")

    for node in graph.graph:
        in_degree = graph.enter_degree(node)
        out_degree = graph.out_degree(node)
        if in_degree != out_degree:
            eureliano = False
            motivos.append(f"O vértice '{node}' tem grau de entrada {in_degree} e grau de saída {out_degree}.")
        else: 
            balanceados.append(f"O vértice '{node}' tem grau de entrada e saída iguais: {in_degree}.")
    with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
        f.write("🔎 Verificação de Eulerianidade do grafo:\n")
        if eureliano:
            f.write("O grafo é Eureliiano.\n")
        else:
            f.write("O grafo NÃO é Eureliano. Motivos:\n")
            for motivo in motivos:
                f.write(f" - {motivo}\n")
        f.write(" Vértices com grau de entrada igual ao grau de saída:\n")
        for linha in balanceados:
            f.write(f" - {linha}\n")

    return eureliano


eureliano(grafo, "verificacao_eureliano.txt")

resultado = eureliano(grafo, "verificacao_eureliano.txt")
print("É eureliano?" , resultado)

# PART 4
print(grafo.dijkstra_distancia('jons@amerexenergy.com', 1))

# PART 5
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
                vizinhos = [vizinho[0] for vizinho in grafo.graph[no_atual]]

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

diametro, caminho = dijkstra_diametro(grafo)
print(f"Diâmetro do grafo: {diametro}")
print("Caminho mais longo (menor caminho mais longo):")
for v in caminho:
    print("->", v)

