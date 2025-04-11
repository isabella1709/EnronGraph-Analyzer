from collections import defaultdict

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
        return [item[0] for item in self.graph[node]] # retorna todos vértices adjacentes / vizinhos