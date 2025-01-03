import sys
from colorama import Fore
import copy

from example_graph import FixedGraph, DynamicGraph
from classes.graph import Graph
from utils.notify import notify
from utils.menu import Menu
from classes.algorithms import BFS, DFS, Greedy, AStar, UniformCost, HillClimb
from classes.vehicle import VEHICLE_TYPES

def run_main():
    main_menu = Menu("Selecione o tipo de grafo que deseja utilizar:")
    main_menu.add_entry("Fixed Graph", lambda: (run_menu(["", "test"]), main_menu.close()))
    main_menu.add_entry("Dynamic Graph", lambda: (run_menu(["", "run_dynamic"]), main_menu.close()))
    #main_menu.add_entry("IRL Graph", lambda: (run_menu(["", "run_irl"]), main_menu.close()))
    main_menu.default_exit(exit_program)
    main_menu.show()

def run_menu(args: list):
    graph = None
    if args[1] == "test": # "make args='test'"
        notify("info", "Running with fixed graph")
        graph = FixedGraph()
    elif args[1] == "run": # "make args='run'"
        notify("info", "Running with dynamic graph") # TODO: Implement the IRLGraph class (a graph where the zones and streats are fixed but travel times and meteorologic conditions change)
        graph = DynamicGraph()
    else:
        notify("warning", "Invalid arguments. Usage: python main.py [test|run_dynamic|run_irl]")
    graph_menu = Menu("Selecione uma opção:")
    graph_menu.add_entry("[Imprimir] Grafo", lambda: print(graph.graph))
    graph_menu.add_entry("[Imprimir] Nodos", lambda: graph.print_nodes())
    graph_menu.add_entry("[Imprimir] Arestas", lambda: graph.print_edges())
    graph_menu.add_entry("[Desenhar] Grafo", lambda: graph.draw_graph())
    graph_menu.add_entry("[Desenhar] Mapa", lambda: graph.draw_map())
    graph_menu.add_entry("[Resolver] com DFS", lambda: resolve(graph, DFS))
    graph_menu.add_entry("[Resolver] com BFS", lambda: resolve(graph, BFS))
    graph_menu.add_entry("[Resolver] com A*", lambda: resolve(graph, AStar))
    graph_menu.add_entry("[Resolver] com Greedy", lambda: resolve(graph, Greedy))
    graph_menu.add_entry("[Resolver] com Uniform Cost", lambda: resolve(graph, UniformCost))
    graph_menu.add_entry("[Resolver] com Hill Climbing", lambda: resolve(graph, HillClimb))
    graph_menu.default_exit(exit_program)
    graph_menu.show()

def resolve(graph: Graph, algorithm):
    start_node = graph.get_camp_node()
    end_nodes = graph.get_affected_nodes()
    carga = int(input(Fore.YELLOW + "Digite a carga total que será transportada (em kg): " + Fore.RESET))
    if carga <= 0:
        notify("error", "Carga inválida. A carga deve ser maior que zero.")
        return
    max_vehicle_cap = max([v.get_capacity() for v in VEHICLE_TYPES.values()])
    if carga > max_vehicle_cap:
        notify("error", f"Carga inválida. A carga máxima suportada é de {max_vehicle_cap} kg.")
        return
    notify("info", f"Resolvendo com {algorithm.__name__} de {start_node} para {end_nodes} com carga de {carga} kg")
    start_node_copy = copy.deepcopy(start_node)
    end_nodes_copy = copy.deepcopy(end_nodes)
    graph_copy = copy.deepcopy(graph)
    #vehicles_copy = copy.deepcopy(VEHICLE_TYPES) # if we wanted the change of vehicles to keep the fuel level of that vehicle we would need to deepcopy the vehicles and pass them and do: path_vehicles = [v.get_vehicle() for v in vehicleTypes]; vehicle_list = [vehicles_copy for vehicles_copy in path_vehicles]; current_vehicle = get_fastest_capable_vehicle(vehicle_list, peso)
    res = algorithm(start_node_copy, end_nodes_copy, graph_copy, carga)
    if res is not None:
        notify("success", f"Resultado: {res[0]} com custo total de {int(res[1])} e veículo {res[2]}")
    else:
        notify("error", "Não foi possível chegar às zonas afetadas dadas as características dos caminhos existentes e os veículos à disposição.")

def main():
    args = sys.argv
    if len(args) < 2:
        notify("error", "Invalid arguments. Select the type of graph you want to use:")
        run_main()
    else:
        run_menu(args)

def exit_program():
    notify("warning", "Exiting...")
    sys.exit()

if __name__ == "__main__":
    main()
