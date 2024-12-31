from classes.graph import Graph
from queue import Queue
from utils.notify import notify
from classes.vehicle import Vehicle, get_fastest_capable_vehicle
import copy

def procura_DFS(start_node: str, end_nodes: list[str], graph: Graph, path: list = [], visited: set[str] = set(), peso: int = 0, vehicle: Vehicle = None):
    """
    Busca em profundidade modificada (DFS) com TTL e troca de veículo baseado no peso.
    :param start_node: Nodo inicial.
    :param end_nodes: Lista de nodos finais.
    :param graph: Grafo.
    :param path: Caminho atual, incluindo nós e trocas de veículos.
    :param visited: Conjunto de nodos já visitados.
    :param peso: Peso a ser transportado.
    :return: Tupla (caminho, custo_total) se encontrar, caso contrário, None.
    """
    # Se não houver mais zonas finais acessíveis
    if not end_nodes:
        return None

    # Make a copy of the end_nodes to avoid modifying the graph
    end_nodes_copy = copy.deepcopy(end_nodes)

    path.append(start_node)
    visited.add(start_node)

    # Se o nodo atual for uma zona final
    if start_node in end_nodes_copy:
        custo_total = graph.calcula_custo(path)
        return (path, custo_total, vehicle)

    for (adjacente, edge_data) in graph.graph[start_node]:
        travel_time, fuel_cost, _, vehicles = edge_data

        # Verificar se o nodo adjacente não foi visitado
        if adjacente not in visited:
            print(f"Visitando {adjacente}")
            # Encontrar um veículo adequado que possa transportar o peso neste arco, o que tem maior velocidade e mesmo assim aguenta o peso
            current_vehicle = get_fastest_capable_vehicle(peso)

            # Atualizar o combustível do veículo
            if current_vehicle is not None:
                if current_vehicle.get_range() < fuel_cost:
                    notify("warning", f"Combustível seria insuficiente para chegar a {adjacente}")
                    continue
                current_vehicle.set_range(current_vehicle.get_range() - fuel_cost)
                print(f"Veículo {current_vehicle.get_name()} com {current_vehicle.get_range()} de combustível")

            # Se não houver veículo adequado, continue
            if current_vehicle is None:
                continue

            # A cada rua andada, Atualizar o TTL de todas as zonas finais
            for end_node_name in end_nodes_copy[:]:  # Iterate over the copy, not the original
                end_zone = graph.get_node(end_node_name)
                end_zone.set_ttl(end_zone.get_ttl() - travel_time)
                print(f"Zona {end_node_name} com TTL {end_zone.get_ttl()}")
                if end_zone.get_ttl() <= 0:
                    notify("warning", f"Zona {end_node_name} removida por TTL")
                    end_nodes_copy.remove(end_node_name)  # Remove from the copy, not from the graph

            # Recursão com o veículo atualizado
            resultado = procura_DFS(adjacente, end_nodes_copy, graph, path, visited, peso, current_vehicle)
            if resultado is not None:
                return resultado
            else:
                # Se não encontrámos nenhuma end zone e os recursos acabaram então os últimos gastos ficam sem efeito e vamos verificar os restantes caminhos
                current_vehicle.set_range(current_vehicle.get_range() + fuel_cost) # Restaurar o valor do combustível nesta zona
                notify("info", f"BackTracking to {path[-1]}: Veículo {current_vehicle.get_name()} com {current_vehicle.get_range()} de combustível")
                for end_node_name in end_nodes_copy[:]:  # Iterate over the copy, not the original
                    end_zone = graph.get_node(end_node_name)
                    end_zone.set_ttl(end_zone.get_ttl() + travel_time) # Restaurar o valor do TTL nesta zona
                    notify("info", f"BackTracking to {path[-1]}: Zona {end_node_name} com TTL {end_zone.get_ttl()}")


    # Remover o último nó do caminho se não houver solução
    path.pop()
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