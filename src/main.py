import sys
from colorama import Fore
from dynamic_graph import DynamicGraph
from fixed_graph import FixedGraph
from irl_graph import IRLGraph
from classes.vehicle import Vehicle
from utils.notify import notify
from utils.menu import Menu

def run_main():
    main_menu = Menu("Selecione o tipo de grafo que deseja utilizar:")
    main_menu.add_entry("Fixed Graph", lambda: (run_menu(["", "test"]), main_menu.close()))
    main_menu.add_entry("Dynamic Graph", lambda: (run_menu(["", "run_dynamic"]), main_menu.close()))
    main_menu.add_entry("IRL Graph", lambda: (run_menu(["", "run_irl"]), main_menu.close()))
    main_menu.default_exit(exit_program)
    main_menu.show()

def run_menu(args):
    graph = None
    if args[1] == "test": # "make args='test'"
        notify("info", "Running with fixed graph")
        graph = FixedGraph()
    elif args[1] == "run_dynamic": # "make args='run_dynamic'"
        notify("info", "Running with dynamic graph")
        graph = DynamicGraph()
    elif args[1] == "run_irl": # "make args='run_irl'"
        notify("info", "Running with IRL graph")
        graph = IRLGraph()
    else:
        notify("warning", "Invalid arguments. Usage: python main.py [test|run_dynamic|run_irl]")
    graph_menu = Menu("Selecione uma opção:")
    graph_menu.add_entry("Imprimir Grafo", lambda: print(graph.graph))
    graph_menu.add_entry("Desenhar Grafo", lambda: graph.draw_graph())
    graph_menu.add_entry("Desenhar Mapa", lambda: graph.draw_map())
    graph_menu.add_entry("Resolver com DFS", lambda: print("Resolver com DFS"))
    graph_menu.add_entry("Resolver com BFS", lambda: resolve_with_bfs(graph))
    graph_menu.default_exit(exit_program)
    graph_menu.show()

def resolve_with_bfs(graph):
    start_node = input(Fore.YELLOW + "Digite o nome da zona inicial para BFS: " + Fore.RESET).strip()
    end_node = input(Fore.YELLOW + "Digite o nome da zona final para BFS: " + Fore.RESET).strip()
    carga = int(input(Fore.YELLOW + "Digite a carga que será transportada (em kg): " + Fore.RESET))

    # Primeiro, encontrar um caminho válido usando BFS
    path, cost = graph.bfs_find_path(start_node, end_node)

    if path is None:
        print(Fore.RED + f"Nenhum caminho válido encontrado de {start_node} para {end_node}." + Fore.RESET)
    else:
        print(Fore.GREEN + f"Caminho encontrado: {path} com custo total de {cost}" + Fore.RESET)
        # Escolher o melhor veículo baseado na carga
        veiculo_escolhido = escolher_veiculo(carga)
        print(Fore.CYAN + f"Veículo escolhido: {veiculo_escolhido.get_tipo_name()}" + Fore.RESET)

        # Resolver com o veículo escolhido
        path, cost = graph.bfs_with_vehicle(start_node, end_node, veiculo_escolhido)

        if path is None:
            print(Fore.RED + f"Nenhum caminho válido encontrado de {start_node} para {end_node} com o veículo escolhido." + Fore.RESET)
        else:
            print(Fore.GREEN + f"Caminho encontrado com o veículo {veiculo_escolhido.get_tipo_name()}: {path} com custo total de {cost}" + Fore.RESET)

def escolher_veiculo(carga):
    veiculos = [
        Vehicle(tipo=0),  # Drone (carga máxima 5 kg)
        Vehicle(tipo=1),  # Helicóptero (carga máxima 1000 kg)
        Vehicle(tipo=2),  # Caminhão (carga máxima 20000 kg)
        Vehicle(tipo=3),  # Carro (carga máxima 500 kg)
        Vehicle(tipo=4),  # Moto (carga máxima 50 kg)
        Vehicle(tipo=5),  # Barco (carga máxima 5000 kg)
    ]

    for veiculo in veiculos:
        if carga <= veiculo.get_carga_max():
            return veiculo
    raise ValueError("Nenhum veículo disponível para transportar essa carga.")

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
