from classes.graph import Graph
from utils.notify import notify
from classes.vehicle import Vehicle, get_fastest_capable_vehicle
import copy
from collections import deque

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
    path.append(start_node)
    visited.add(start_node)
    # Se o nodo atual for uma zona final
    if start_node in end_nodes:
        custo_total = graph.calcula_custo(path)
        return (path, custo_total, vehicle)
    for (adjacente, edge_data) in graph.graph[start_node]:
        travel_time, fuel_cost, _, _ = edge_data
        # Verificar se o nodo adjacente não foi visitado
        if adjacente not in visited:
            #print(f"Visitando {adjacente}")
            # Encontrar um veículo adequado que possa transportar o peso neste arco, o que tem maior velocidade e mesmo assim aguenta o peso
            current_vehicle = get_fastest_capable_vehicle(peso)
            # Atualizar o combustível do veículo
            if current_vehicle is not None:
                if current_vehicle.get_range() < fuel_cost:
                    notify("warning", f"Combustível seria insuficiente para chegar a {adjacente}, reabasteça {abs(current_vehicle.get_range()-fuel_cost)} de combustível")
                    continue
                current_vehicle.set_range(current_vehicle.get_range() - fuel_cost)
                #print(f"Veículo {current_vehicle.get_name()} com {current_vehicle.get_range()} de combustível")
            # Se não houver veículo adequado, continue
            if current_vehicle is None:
                continue
            # A cada rua andada, Atualizar o TTL de todas as zonas finais
            for end_node_name in end_nodes[:]:  # Iterate over the copy, not the original
                end_zone = graph.get_node(end_node_name)
                end_zone.set_ttl(end_zone.get_ttl() - travel_time)
                #print(f"Zona {end_node_name} com TTL {end_zone.get_ttl()}")
                if end_zone.get_ttl() <= 0:
                    notify("warning", f"Zona {end_node_name} removida por TTL")
                    end_nodes.remove(end_node_name)  # Remove from the copy, not from the graph
            # Recursão com o veículo atualizado
            resultado = procura_DFS(adjacente, end_nodes, graph, path, visited, peso, current_vehicle)
            if resultado is not None:
                return resultado
            # Backtracking não é utilizado no algoritmo DFS, mas será util para outros algoritmos
            #else:
                # Se não encontrámos nenhuma end zone e os recursos acabaram então os últimos gastos ficam sem efeito e vamos verificar os restantes caminhos
                #current_vehicle.set_range(current_vehicle.get_range() + fuel_cost) # Restaurar o valor do combustível nesta zona
                #notify("info", f"BackTracking to {path[-1]}: Veículo {current_vehicle.get_name()} com {current_vehicle.get_range()} de combustível")
                #for end_node_name in end_nodes[:]:
                    #end_zone = graph.get_node(end_node_name)
                    #end_zone.set_ttl(end_zone.get_ttl() + travel_time) # Restaurar o valor do TTL nesta zona
                    #notify("info", f"BackTracking to {path[-1]}: Zona {end_node_name} com TTL {end_zone.get_ttl()}")
    # Remover o último nó do caminho se não houver solução
    path.pop()
    return None

def procura_BFS(start_node: str, end_nodes: list[str], graph: Graph, peso: int=0):
    """
    Busca em largura modificada (BFS) com TTL e troca de veículo baseado no peso.
    :param start_node: Nodo inicial.
    :param end_nodes: Lista de nodos finais.
    :param graph: Grafo.
    :param peso: Peso a ser transportado.
    :return: Tupla (caminho, custo_total, veículo) se encontrar, caso contrário, None.
    """
    # Se não houver mais zonas finais acessíveis
    if not end_nodes:
        return None

    # Se o nodo incial for uma zona final
    if start_node in end_nodes:
        return ([start_node], 0, current_vehicle)
    
    # Para cada estado/path está associado o valor de combustível para o percorrer
    fuel_needed = 0 
    # Criar uma lista de (end_zone, TTL) para cada path possível a partir ds end_nodes
    end_nodes_ttl = [(end_node, graph.get_node(end_node).get_ttl()) for end_node in end_nodes]

    # Fila de exploração: (current_node, current_path, current_vehicle, end_nodes_ttl_copy, fuel_needed)
    # Cada elemento da fila é um possível estado 
    queue = deque([(start_node, [start_node], None, copy.deepcopy(end_nodes_ttl), fuel_needed)])
    visited = set()  # Usado para evitar revisitar zonas

    
    # Adição da zona de partida à lista de visitadas
    visited.add(start_node)
    while queue:
        # Pega no primeiro elemento da fila
        current_node, current_path, current_vehicle, current_end_nodes_ttl, current_path_fuel_needed = queue.popleft()


        print(f"A analisar os vizinhos de {current_node}")
        # Explorar nós adjacentes
        for (adjacente, edge_data) in graph.graph[current_node]:
            travel_time, fuel_cost, _, vehicles = edge_data

            # Verificar se o nodo adjacente não foi visitado
            if adjacente not in visited:
                print(f"Testando rota {current_path+[adjacente]}")
                # Encontrar um veículo adequado para transportar o peso
                current_vehicle = get_fastest_capable_vehicle(peso)

                # Validar combustível
                if current_vehicle is not None:
                    # Se o veículo tiver autonomia para percorrer este potencial path
                    if current_vehicle.get_range() < current_path_fuel_needed + fuel_cost:
                        notify("warning", f"Combustível seria insuficiente por esta rota para chegar a {adjacente}: {current_vehicle.get_range()- (current_path_fuel_needed + fuel_cost)}")
                        continue
                    print(f"Veículo {current_vehicle.get_name()} ficaria com {current_vehicle.get_range()- (current_path_fuel_needed + fuel_cost)} de combustível")

                # Se não houver veículo adequado, continuar
                if current_vehicle is None:
                    continue
                
                # Atualizar TTL das zonas finais
                new_end_nodes_ttl = []
                for end_zone, ttl in current_end_nodes_ttl:
                    new_ttl = ttl - travel_time
                    if new_ttl > 0:
                        new_end_nodes_ttl.append((end_zone, new_ttl))
                        print(f"Zona {end_zone} ficaria com TTL {new_ttl}")
                    else:
                        notify("warning", f"Zona {end_zone} removida pois excederia TTL para esta rota")


                 # Se o nodo adjacente for uma zona final
                if any(adjacente == end_zone for end_zone, _ in new_end_nodes_ttl):
                    custo_total = graph.calcula_custo(current_path + [adjacente])
                    return (current_path+[adjacente], custo_total, current_vehicle)
                
                # Adicionar o nó adjacente aos visitados e à fila com caminho atualizado
                visited.add(adjacente)
                queue.append((adjacente, current_path + [adjacente], current_vehicle, new_end_nodes_ttl, current_path_fuel_needed+fuel_cost))

    return None  # Se não encontrar nenhum caminho

def procura_UniformCost():
    pass

def procura_Greedy():
    pass