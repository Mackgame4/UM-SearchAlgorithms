from classes.graph import Graph
from queue import Queue

def procura_DFS(start_node, end_nodes, graph: Graph, path: list[str]=[], visited: set[str]={}):
        path.append(start_node)
        visited.add(start_node)
        if start_node in end_nodes:
            # calcular o custo do caminho funçao calcula custo.
            custoT = graph.calcula_custo(path)
            return (path, custoT)
        for (adjacente, _) in graph.graph[start_node]:
            if adjacente not in visited: # TODO: only add to visited if the vehicle is capable of going there
                resultado = procura_DFS(adjacente, end_nodes, graph, path, visited)
                if resultado is not None:
                    return resultado
        path.pop() # se nao encontra remover o que está no caminho
        return None

def procura_BFS(start, end, graph=Graph()):
        # definir nodos visitados para evitar ciclos
        visited = set()
        fila = Queue()
        custo = 0
        # adicionar o nodo inicial à fila e aos visitados
        fila.put(start)
        visited.add(start)

        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()
            if nodo_atual == end:
                path_found = True
            else:
                for (adjacente, peso) in graph.graph[nodo_atual]:
                    if adjacente not in visited:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)

        # reconstruir o caminho

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            # funçao calcula custo caminho
            custo = graph.calcula_custo(path)
        return (path, custo)