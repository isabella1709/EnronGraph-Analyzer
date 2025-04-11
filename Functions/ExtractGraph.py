from collections import defaultdict

def getOrder(graph):
    return graph.order # Retorna o número de vértices do grafo

def getSize(graph):
    return graph.size # Retorna o número de arestas do grafo

def getIsolatedVertices(graph): # Retorna vétices sem grau de saída ou entrada
    count = 0
    for key in graph.graph:
        if (graph.degree(key) == 0):
            count +=1
    
    return count

def getMaximumOutDegrees(graph): 
    vertices = []

    for key in graph.graph:
        outDegree = graph.out_degree(key)
        vertices.append((key, outDegree))

    sortedVertices = sorted(vertices, key=lambda x: x[1], reverse=True) # Ordena a lista de tuplas a partir do grau

    return sortedVertices[:20] # Retorna os 20 vértices com maior grau de saída


def getMaximumEnterDegrees(graph):
    enter_degrees = defaultdict(int)

    for u in graph.graph: # Conta o grau de entrada de todos os nós
        for v, _ in graph.graph[u]:
            enter_degrees[v] += 1

    for v in graph.graph: # Garante que todos os nós estejam no dicionário 
        if v not in enter_degrees:
            enter_degrees[v] = 0

    sortedVertices = sorted(enter_degrees.items(), key=lambda x: x[1], reverse=True) # Ordena os nós pelo grau de entrada

    return sortedVertices[:20] # Retorna os 20 vértices com maior grau de entrada
