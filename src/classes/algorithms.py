from classes.graph import Graph
from utils.notify import notify
from classes.vehicle import Vehicle, VehicleType, get_fastest_capable_vehicle, get_start_capable_vehicle
import copy
from collections import deque
from queue import Queue
from heapq import heappush, heappop

def DFS(start_node: str, end_nodes: list[str], graph: Graph, peso: int = 0, path: list = None, visited: set = None, vehicle: Vehicle = None):
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
    # Initialize path and visited set on the first call if they are not passed
    if path is None:
        path = []
    if visited is None:
        visited = set()
    # If no more accessible final zones
    if not end_nodes:
        return None
    path.append(start_node)
    visited.add(start_node)
    # If the current node is a final zone
    if start_node in end_nodes:
        custo_total = graph.calcula_custo(path)
        return (path, custo_total, vehicle)
    for (adjacente, edge_data) in graph.graph[start_node]:
        travel_time, fuel_cost, _, vehicleTypes = edge_data
        # Check if the adjacent node hasn't been visited
        if adjacente not in visited:
            notify("debug", f"Testando rota {path+[adjacente]}")
            # Find an appropriate vehicle that can carry the load on this edge, which has higher speed and can still carry the weight
            vehicle_list = [v.get_vehicle() for v in vehicleTypes]
            current_vehicle = get_fastest_capable_vehicle(vehicle_list, peso)
            # Update vehicle fuel
            if current_vehicle is not None:
                # Notify if vehicle has changed
                if vehicle is not None and current_vehicle != vehicle:
                    notify("warning", f"Troca de veículo de {vehicle.get_name()} para {current_vehicle.get_name()} em {adjacente}")
                if current_vehicle.get_range() < fuel_cost:
                    notify("warning", f"Combustível seria insuficiente para chegar a {adjacente}, reabasteça {abs(current_vehicle.get_range()-fuel_cost)} de combustível")
                    continue
                current_vehicle.set_range(current_vehicle.get_range() - fuel_cost)
                notify("debug", f"Veículo {current_vehicle.get_name()} com {current_vehicle.get_range()} de combustível ao chegar a {adjacente}")
            # If no suitable vehicle, continue
            if current_vehicle is None:
                notify("debug", f"Não há nenhum veículo capaz de realizar esta rota, {path+[adjacente]}, com esta carga: {peso}")
                continue
            # For each step, update TTL of all final zones
            for end_node_name in end_nodes[:]:  # Iterate over the copy, not the original
                end_zone = graph.get_node(end_node_name)
                end_zone.set_ttl(end_zone.get_ttl() - travel_time)
                if end_zone.get_ttl() <= 0:
                    notify("warning", f"Zona {end_node_name} removida por TTL")
                    end_nodes.remove(end_node_name) # Remove from the copy, not from the graph
            # Recursion with the updated vehicle and fresh path/visited
            resultado = DFS(adjacente, end_nodes, graph, peso, path.copy(), visited.copy(), current_vehicle)
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

def BFS(start_node: str, end_nodes: list[str], graph: Graph, peso: int=0):
    """
    Busca em largura modificada (BFS) com TTL e troca de veículo baseado no peso.
    :param start_node: Nodo inicial.
    :param end_nodes: Lista de nodos finais.
    :param graph: Grafo.
    :param peso: Peso a ser transportado.
    :return: Tupla (caminho, custo_total, veículo) se encontrar, caso contrário, None.
    """
    # Se não houver zonas finais acessíveis
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
        current_node, current_path, vehicle, current_end_nodes_ttl, current_path_fuel_needed = queue.popleft()


        notify("debug", f"A analizar os vizinhos de {current_node}")
        # Explorar nós adjacentes
        for (adjacente, edge_data) in graph.graph[current_node]:
            travel_time, fuel_cost, _, vehicles = edge_data

            # Verificar se o nodo adjacente não foi visitado
            if adjacente not in visited:
                notify("debug", f"Testando rota {current_path+[adjacente]}")

                # Encontrar um veículo que possa atravessar esta aresta com esta carga e que seja rápido mas também adequado à carga qeu irá transportar
                vehicle_list = [v.get_vehicle() for v in vehicles]
                current_vehicle = get_fastest_capable_vehicle(vehicle_list, peso)

                # Validar combustível
                if current_vehicle is not None:
                    if vehicle is not None and current_vehicle != vehicle:
                        notify("warning", f"Troca de veículo de {vehicle.get_name()} para {current_vehicle.get_name()} em {adjacente}")
                    # Se o veículo tiver autonomia para percorrer este potencial path
                    if current_vehicle.get_range() < current_path_fuel_needed + fuel_cost:
                        notify("warning", f"Combustível seria insuficiente por esta rota para chegar a {adjacente}, reabasteça {abs(current_vehicle.get_range() - (current_path_fuel_needed + fuel_cost))}")
                        continue
                    notify("debug", f"Veículo {current_vehicle.get_name()} ficaria com {current_vehicle.get_range() - (current_path_fuel_needed + fuel_cost)} de combustível ao chegar a {adjacente}")

                # Se não houver veículo adequado, continuar
                if current_vehicle is None:
                    notify("debug", f"Não há nenhum veículo capaz de realizar esta rota, {current_path+[adjacente]}, com esta carga: {peso}")
                    continue
                
                # Atualizar TTL das zonas finais
                new_end_nodes_ttl = []
                for end_zone, ttl in current_end_nodes_ttl:
                    new_ttl = ttl - travel_time
                    if new_ttl > 0:
                        new_end_nodes_ttl.append((end_zone, new_ttl))
                        notify("debug", f"Zona {end_zone} ficaria com TTL {new_ttl}")
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


def AStar(start_node: str, end_nodes: list[str], graph: Graph, peso: int = 0):
    """
    Busca A* modificada com TTL e troca de veículo baseado no peso.
    :param start_node: Nodo inicial.
    :param end_nodes: Lista de nodos finais.
    :param graph: Grafo.
    :param peso: Peso a ser transportado.
    :return: Tupla (caminho, custo_total, veículo) se encontrar, caso contrário, None.
    """
    # Se não houver zonas finais acessíveis
    if not end_nodes:
        return None

    # Se o nodo incial for uma zona final
    if start_node in end_nodes:
        return ([start_node], 0, None)

    # Queue prioritária para A* (min-heap)
    # Queue prioritária tuplos: (f_score, current_path_cost, current_node, path, current_vehicle, end_nodes_ttl, fuel_used)
    open_set = []
    heappush(open_set, (0, 0, start_node, [start_node], None, 
                        [(end_node, graph.get_node(end_node).get_ttl()) for end_node in end_nodes], 0))

    # Guardar os melhores custos de rota para cada nodo
    g_score = {start_node: 0}
    visited = set()

    while open_set:
        _, current_cost, current_node, current_path, vehicle, current_end_nodes_ttl, current_path_fuel = heappop(open_set)

        # Se o nodo atual for um nodo objetivo
        if any(current_node == end_zone for end_zone, _ in current_end_nodes_ttl):
            custo_total = graph.calcula_custo(current_path)
            return (current_path, custo_total, vehicle)

        notify("debug", f"A analisar os vizinhos de {current_node}")

        for (adjacente, edge_data) in graph.graph[current_node]:
            travel_time, fuel_cost, _, vehicles = edge_data

            if adjacente in visited:
                continue
            notify("debug", f"Testando rota {current_path+[adjacente]}")

            # Calcular o potencial custo de rota para o nodo adjacente
            tentative_g_score = current_cost + graph.calcula_custo(current_path + [adjacente])

            # Calcular a heurística do nodo adjacente e completar a função custo: custo rota + heuristica 
            heuristic = graph.get_heuristic(adjacente)
            f_score = tentative_g_score + heuristic

            # Se o valor do custo da rota do nodo for melhor doq que o seu último valor, atualizar
            if tentative_g_score < g_score.get(adjacente, float('inf')):
                g_score[adjacente] = tentative_g_score

            # Encontrar um veículo que possa atravessar esta aresta com esta carga e que seja rápido mas também adequado à carga que irá transportar
            vehicle_list = [v.get_vehicle() for v in vehicles]
            current_vehicle = get_fastest_capable_vehicle(vehicle_list, peso)

            # Validar combustível
            if current_vehicle is not None:
                if vehicle is not None and current_vehicle != vehicle:
                    notify("warning", f"Troca de veículo de {vehicle.get_name()} para {current_vehicle.get_name()} em {adjacente}")
                # Se o veículo tiver autonomia para percorrer este potencial path
                if current_vehicle.get_range() < current_path_fuel + fuel_cost:
                    notify("warning", f"Combustível seria insuficiente por esta rota para chegar a {adjacente}, reabasteça {abs(current_vehicle.get_range() - (current_path_fuel + fuel_cost))}")
                    continue
                notify("debug", f"Veículo {current_vehicle.get_name()} ficaria com {current_vehicle.get_range() - (current_path_fuel + fuel_cost)} de combustível ao chegar a {adjacente}")

            # Se não houver veículo adequado, continuar
            if current_vehicle is None:
                notify("debug", f"Não há nenhum veículo capaz de realizar esta rota, {current_path+[adjacente]}, com esta carga: {peso}")
                continue

            # Atualizar TTL para end zones
            new_end_nodes_ttl = []
            for end_zone, ttl in current_end_nodes_ttl:
                new_ttl = ttl - travel_time
                if new_ttl > 0:
                    new_end_nodes_ttl.append((end_zone, new_ttl))
                    notify("debug", f"Zona {end_zone} ficaria com TTL {new_ttl}")
                else:
                    notify("warning", f"Zona {end_zone} removida pois excederia TTL para esta rota")

            # Se o nodo adjacente é um nodo objetivo
            if any(adjacente == end_zone for end_zone, _ in new_end_nodes_ttl):
                custo_total = graph.calcula_custo(current_path + [adjacente])
                return (current_path + [adjacente], custo_total, current_vehicle)

            # Inserir o novo estado na queue
            heappush(open_set, (f_score, tentative_g_score, adjacente, current_path + [adjacente], 
                                current_vehicle, new_end_nodes_ttl, current_path_fuel + fuel_cost))

        visited.add(current_node)

    return None  # No path found


def Greedy(start_node: str, end_nodes: list[str], graph: Graph, peso: int = 0): 
    open_list = set([start_node])
    closed_list = set([])
    parents = {}
    parents[start_node] = start_node
    old_vehicle = copy.deepcopy(get_start_capable_vehicle(peso))
    while len(open_list) > 0:
        n = None
        # Encontra o nodo com a menor heurística
        for v in open_list:
            if n == None or graph.heuristics[v] < graph.heuristics[n]:
                n = v
        if n == None:
            return None
        # Se o nodo corrente é o destino
        if n in end_nodes:
            reconst_path = []
            while parents[n] != n:
                reconst_path.append(n)
                n = parents[n]
            reconst_path.append(start_node)
            reconst_path.reverse()
            return (reconst_path, graph.calcula_custo(reconst_path), new_vehicle)
        # Para todos os vizinhos do nodo corrente
        for (m, travel_time, fuel_cost, _, vehicleTypes) in graph.get_neighbours(n):
            # Se o nodo corrente não está na open nem na closed list, adicioná-lo à open_list
            if m not in open_list and m not in closed_list:
                open_list.add(m)
                parents[m] = n
        # Remover n da open_list e adicionar à closed_list, pois todos os seus vizinhos foram inspecionados
        open_list.remove(n)
        closed_list.add(n)
        # Other logic
        # Update the TTL of all final zones for each step
        for end_node_name in end_nodes[:]:
            end_zone = graph.get_node(end_node_name)
            end_zone.set_ttl(end_zone.get_ttl() - travel_time)
            if end_zone.get_ttl() <= 0:
                notify("warning", f"Zona {end_node_name} removida por TTL")
                end_nodes.remove(end_node_name)
        # Verificar se o veículo tem combustível suficiente para a próxima viagem
        vehicle_list = [v.get_vehicle() for v in vehicleTypes]
        new_vehicle = get_fastest_capable_vehicle(vehicle_list, peso)
        if new_vehicle is None:
            continue
        # Add the vehicle change notification
        if new_vehicle is not None:
            if new_vehicle != old_vehicle:
                if old_vehicle is not None:
                    notify("warning", f"Troca de veículo de {old_vehicle.get_name()} para {new_vehicle.get_name()} em {n}")
                old_vehicle = new_vehicle
        if new_vehicle.get_range() < fuel_cost:
            # Notificar que o veículo precisa de reabastecimento
            notify("warning", f"Combustível insuficiente para ir de {n} para {m}, reabasteça!")
            continue
        # Deduzir o combustível para a próxima viagem
        new_vehicle.set_range(new_vehicle.get_range() - fuel_cost)
    return None

def UniformCost(start_node: str, end_nodes: list[str], graph: Graph, peso: int = 0):  
    """
    Uniform Cost Search for pathfinding using Queue and deque, prioritizing the least total cost (fuel cost).
    :param start_node: Nodo inicial.
    :param end_nodes: Lista de nodos finais.
    :param graph: Grafo.
    :param peso: Peso a ser transportado.
    :return: Tupla (caminho, custo_total, veículo) se encontrar, caso contrário, None.
    """
    # Queue for the exploration process
    open_list = Queue()
    open_list.put((0, start_node, None))  # (cumulative cost, node, vehicle)
    
    # Dictionaries to store the minimum cost to reach each node and the parent node
    min_cost = {start_node: 0}
    parents = {start_node: None}
    vehicles = {start_node: None}  # To track the vehicle used to reach each node
    
    old_vehicle = copy.deepcopy(get_start_capable_vehicle(peso))  # Initialize the starting vehicle

    print(old_vehicle)
    if old_vehicle is None:
        return None # if no vehicle can carry the load at the start, we will assume the load is impossible for the entire path
    
    while not open_list.empty():
        current_cost, current_node, vehicle = open_list.get()  # Get the node with lowest cumulative cost
        
        # If we reached one of the end nodes, reconstruct the path
        if current_node in end_nodes:
            path = []
            node = current_node
            while node is not None:
                path.append(node) # TODO: fix this, only add if the vehicle going there is not None and other rules (also check it for other ones)
                node = parents[node]
            path.reverse()
            total_cost = current_cost
            return (path, total_cost, vehicle)
        
        # Process each adjacent node
        for (adjacente, edge_data) in graph.graph[current_node]:
            travel_time, fuel_cost, _, vehicleTypes = edge_data
            new_cost = current_cost + fuel_cost  # Total cost to reach the adjacent node
            
            # Check if we found a cheaper way to reach the adjacent node
            if adjacente not in min_cost or new_cost < min_cost[adjacente]:
                min_cost[adjacente] = new_cost
                parents[adjacente] = current_node
                
                # Find the most appropriate vehicle for this edge
                vehicle_list = [v.get_vehicle() for v in vehicleTypes]
                new_vehicle = get_fastest_capable_vehicle(vehicle_list, peso)
                print(new_vehicle)
                print(adjacente)
                if new_vehicle is not None:
                    print(new_vehicle.get_range())
                
                if new_vehicle is None:
                    continue  # If no vehicle can carry the load, skip
                
                # Check if the vehicle has enough fuel
                if new_vehicle.get_range() < fuel_cost:
                    notify("warning", f"Combustível insuficiente para viajar de {current_node} para {adjacente}, reabasteça!")
                    continue  # Skip this path if fuel is insufficient
                
                # Deduct the fuel for this journey
                new_vehicle.set_range(new_vehicle.get_range() - fuel_cost)
                
                # Notify if the vehicle changed
                if new_vehicle != old_vehicle and new_vehicle is not None:
                    if old_vehicle is not None:
                        notify("warning", f"Troca de veículo de {old_vehicle.get_name()} para {new_vehicle.get_name()} em {adjacente}")
                    old_vehicle = new_vehicle

                # Add to the open list
                open_list.put((new_cost, adjacente, new_vehicle))
                vehicles[adjacente] = new_vehicle
        
        # Update TTL for the end zones at each step
        for end_node_name in end_nodes[:]:
            end_zone = graph.get_node(end_node_name)
            end_zone.set_ttl(end_zone.get_ttl() - travel_time)
            if end_zone.get_ttl() <= 0:
                notify("warning", f"Zona {end_node_name} removida por TTL")
                end_nodes.remove(end_node_name)
    return None  # Return None if no path is found

def HillClimbing():
    pass

def SimulatedAnnealing():
    pass

def GeneticAlgorithm():
    pass