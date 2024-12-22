import sys
from colorama import Fore
from dynamic_graph import DynamicGraph
from fixed_graph import FixedGraph
from irl_graph import IRLGraph
from vehicle import Vehicle


def main():
    args = sys.argv
    graph = None
    if len(args) < 2:
        print(Fore.RED + "Invalid arguments. Select the type of graph you want to use:" + Fore.RESET)
        print(Fore.YELLOW + "1 - " + Fore.RESET + "Grafo Fixo")
        print(Fore.YELLOW + "2 - " + Fore.RESET + "Grafo Dinâmico")
        print(Fore.YELLOW + "3 - " + Fore.RESET + "Grafo IRL")
        print(Fore.YELLOW + "0 - " + Fore.RESET + "Sair")
        option = int(input(Fore.YELLOW + "Escolha uma opcao: " + Fore.RESET))
        if option == 1:
            args.append("test")
        elif option == 2:
            args.append("run_dynamic")
        elif option == 3:
            args.append("run_irl")
        else:
            exit_program()
        print("\033c")  # clean the console
        main()  # re-run the program with the new argument
    elif args[1] == "test":  # "make args='test'"
        print(Fore.GREEN + "DEBUG: Running with fixed test graph" + Fore.RESET)
        graph = FixedGraph()
    elif args[1] == "run_dynamic":  # "make args='run_dynamic'"
        print(Fore.GREEN + "DEBUG: Running with dynamic graph" + Fore.RESET)
        graph = DynamicGraph()
    elif args[1] == "run_irl":  # "make args='run_irl'"
        print(Fore.GREEN + "DEBUG: Running with IRL graph" + Fore.RESET)
        graph = IRLGraph()
    else:
        print(Fore.RED + "Invalid arguments. Usage: python main.py [test|run_dynamic|run_irl]" + Fore.RESET)
        exit_program()

    # Run the program
    option = -1
    while option != 0:
        print(Fore.YELLOW + "1 - " + Fore.RESET + "Imprimir Grafo")
        print(Fore.YELLOW + "2 - " + Fore.RESET + "Desenhar Grafo")
        print(Fore.YELLOW + "3 - " + Fore.RESET + "Desenhar Mapa")
        print(Fore.YELLOW + "4 - " + Fore.RESET + "Resolver com DFS")
        print(Fore.YELLOW + "5 - " + Fore.RESET + "Resolver com BFS escolhendo o melhor veículo")
        print(Fore.YELLOW + "0 - " + Fore.RESET + "Sair")

        if not graph:
            print(Fore.RED + "Graph is not initialized." + Fore.RESET)
            exit_program()

        option = int(input(Fore.YELLOW + "Escolha uma opcao: " + Fore.RESET))
        if option == 0:
            exit_program()
        elif option == 1:
            print(graph.graph)
            input("Prima" + Fore.YELLOW + " ENTER " + Fore.RESET + "para continuar")
        elif option == 2:
            graph.draw_graph()
            input("Prima" + Fore.YELLOW + " ENTER " + Fore.RESET + "para continuar")
        elif option == 3:
            graph.draw_map()
            input("Prima" + Fore.YELLOW + " ENTER " + Fore.RESET + "para continuar")
        elif option == 4:
            print("Resolver com DFS")
            input("Prima" + Fore.YELLOW + " ENTER " + Fore.RESET + "para continuar")
        elif option == 5:
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
            input("Prima" + Fore.YELLOW + " ENTER " + Fore.RESET + "para continuar")
        else:
            print(Fore.RED + "Opcao invalida." + Fore.RESET)

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

def exit_program():
    print(Fore.RED + "Exiting..." + Fore.RESET)
    sys.exit()

if __name__ == "__main__":
    main()
