import sys
from colorama import Fore
from example_graph import FixedGraph, DynamicGraph
from classes.graph import Graph
from utils.notify import notify
from utils.menu import Menu
from classes.algorithms import procura_BFS, procura_DFS

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
        notify("info", "Running with dynamic graph")
        graph = DynamicGraph()
    else:
        notify("warning", "Invalid arguments. Usage: python main.py [test|run_dynamic|run_irl]")
    graph_menu = Menu("Selecione uma opção:")
    graph_menu.add_entry("[Imprimir] Grafo", lambda: print(graph.graph))
    graph_menu.add_entry("[Imprimir] Nodos", lambda: graph.print_nodes())
    graph_menu.add_entry("[Imprimir] Arestas", lambda: graph.print_edges())
    graph_menu.add_entry("[Desenhar] Grafo", lambda: graph.draw_graph())
    graph_menu.add_entry("[Desenhar] Mapa", lambda: graph.draw_map())
    graph_menu.add_entry("[Resolver] com DFS", lambda: resolve_with_dfs(graph))
    graph_menu.add_entry("[Resolver] com BFS", lambda: resolve_with_bfs(graph))
    graph_menu.add_entry("[Resolver] com A*", lambda: print("Resolver com A*"))
    graph_menu.add_entry("[Resolver] com Greedy", lambda: print("Resolver com Greedy"))
    graph_menu.add_entry("[Resolver] com Uniform Cost", lambda: print("Resolver com Uniform Cost"))
    graph_menu.add_entry("[Resolver] com Hill Climbing", lambda: print("Resolver com Hill Climbing"))
    graph_menu.add_entry("[Resolver] com Simulated Annealing", lambda: print("Resolver com Simulated Annealing"))
    graph_menu.add_entry("[Resolver] com Genetic Algorithm", lambda: print("Resolver com Genetic Algorithm"))
    graph_menu.add_entry("[Resolver] com Estratégia Desenvolvida", lambda: print("Resolver com Estratégia Desenvolvida pelo grupo"))
    graph_menu.default_exit(exit_program)
    graph_menu.show()

def resolve_with_dfs(graph: Graph):
    #start_node = input(Fore.YELLOW + "Digite o nome da zona inicial: " + Fore.RESET).strip()
    #end_node = input(Fore.YELLOW + "Digite o nome da zona final: " + Fore.RESET).strip()
    start_node = graph.get_camp_node()
    end_nodes = graph.get_affected_nodes()
    notify("debug", f"A resolver com DFS de {start_node} para {end_nodes}")
    path = []
    visited = set()
    res = procura_DFS(start_node, end_nodes, graph, path, visited)
    if res != None:
        notify("info", f"Resultado: {res}") # Exemplo usando o grafo fixo: Angola -> Malawi ((['Angola', 'Botswana', 'Namibia', 'Zambia', 'Zimbabwe', 'Malawi'], 7730))

def resolve_with_bfs(graph: Graph):
    start_node = input(Fore.YELLOW + "Digite o nome da zona inicial: " + Fore.RESET).strip()
    end_node = input(Fore.YELLOW + "Digite o nome da zona final: " + Fore.RESET).strip()
    #carga = int(input(Fore.YELLOW + "Digite a carga que será transportada (em kg): " + Fore.RESET))
    #vehicle = Vehicle()
    #vehicle.set_carga_atual(carga)
    #print(vehicle.get_possible_vehicles())
    #graph.bfs(start_node, end_node, vehicle)
    print("Resolver com BFS")
    print(procura_BFS(start_node, end_node, graph))

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
