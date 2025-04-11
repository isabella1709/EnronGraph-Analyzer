from collections import defaultdict

def getOrder(graph):
    return graph.order

def getSize(graph):
    return graph.size

def getIsolatedVertices(graph):
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

    sortedVertices = sorted(vertices, key=lambda x: x[1], reverse=True)

    return sortedVertices[:20]


def getMaximumEnterDegrees(graph):
    enter_degrees = defaultdict(int)

    for u in graph.graph:
        for v, _ in graph.graph[u]:
            enter_degrees[v] += 1

    for v in graph.graph:
        if v not in enter_degrees:
            enter_degrees[v] = 0

    sortedVertices = sorted(enter_degrees.items(), key=lambda x: x[1], reverse=True)

    return sortedVertices[:20]