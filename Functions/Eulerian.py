from Functions.Graph import Graph

def dfs(v, visited, g):
    visited.add(v)
    for neighbor in g.graph[v]:
        if neighbor[0] not in visited:
            dfs(neighbor[0], visited, g) # chama a função novamente para registrar como visitado

def conexo(graph): 
    if not graph.graph:
        return False  # grafo vazio não é conexo

    start_node = next(iter(graph.graph)) # escolhe um vértice inicial
    visited = set()
    dfs(start_node, visited, graph)
    
    if len(visited) != len(graph.graph):
        return False # retorna falso se não visitou todos os vértices

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


def euleriano(graph):
    euleriano = True
    nao_conexo = False
    graus_diferentes = False
    motivos = [] 

    if not conexo(graph):
        euleriano = False
        nao_conexo = True
        motivos.append("O grafo não é fortemente conexo.")

    for node in graph.graph:
        in_degree = graph.enter_degree(node)
        out_degree = graph.out_degree(node)
        if in_degree != out_degree:
            euleriano = False
            graus_diferentes = True
            motivos.append(f"O vértice '{node}' tem grau de entrada {in_degree} e grau de saída {out_degree}.")

    
    print("\nVerificação da Eularidade do grafo:")
    if euleriano:
        print("\nO grafo é Euleriano.")
    else:
        print("\nO grafo não é Euleriano. \n\nMotivos:")
        if nao_conexo:
            print("- O grafo não é fortemente conexo.")
        if graus_diferentes:
            print("- Os graus de entrada e saída de alguns vértices não são iguais.")
            for condition in motivos[:10]:  
                print(f"  - {condition}")
        if len(motivos) > 10:
            print(f"  ... e mais {len(motivos) - 10} motivos.")

    return euleriano # Retorna True or False