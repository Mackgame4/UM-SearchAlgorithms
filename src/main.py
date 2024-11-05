import sys
from colorama import Fore
from dynamic_graph import DynamicGraph
from graph import FixedGraph

def main():
    args = sys.argv
    dynamic_graph = None
    fixed_graph = None
    if len(args) < 2:
        print(Fore.RED + "Invalid arguments. Select the type of graph you want to use:" + Fore.RESET)
        print(Fore.YELLOW + "1 - " + Fore.RESET + "Grafo Fixo")
        print(Fore.YELLOW + "2 - " + Fore.RESET + "Grafo Dinâmico")
        print(Fore.YELLOW + "0 - " + Fore.RESET + "Sair")
        option = int(input(Fore.YELLOW + "Escolha uma opcao: " + Fore.RESET))
        if option == 1:
            args.append("test")
        elif option == 2:
            args.append("run")
        else:
            exit()
        print("\033c") # clean the console
        main() # re-run the program with the new argument
    elif args[1] == "test": # "make args='test'"
        print(Fore.GREEN + "DEBUG: Running with fixed graph" + Fore.RESET)
        fixed_graph = FixedGraph()
    elif args[1] == "run": # "make args='run'"
        print(Fore.GREEN + "DEBUG: Running with dynamic graph" + Fore.RESET)
        endereco = "Freguesia da Misericordia, Lisbon, Portugal"
        dynamic_graph = DynamicGraph(endereco)
    else:
        print(Fore.RED + "Invalid arguments. Usage: python main.py [test|run]" + Fore.RESET)
        exit()

    # Run the program
    option = -1
    while option != 0:
        print(Fore.YELLOW + "1 - " + Fore.RESET + "Imprimir Grafo")
        print(Fore.YELLOW + "2 - " + Fore.RESET + "Desenhar Grafo")
        print(Fore.YELLOW + "3 - " + Fore.RESET + "Desenhar Mapa")
        print(Fore.YELLOW + "4 - " + Fore.RESET + "Resolver com DFS")
        print(Fore.YELLOW + "5 - " + Fore.RESET + "Resolver com BFS")
        print(Fore.YELLOW + "0 - " + Fore.RESET + "Sair")

        option = int(input(Fore.YELLOW + "Escolha uma opcao: " + Fore.RESET))
        if option == 0:
            exit()
        elif option == 1:
            if dynamic_graph: print(dynamic_graph.graph)
            if fixed_graph: print(fixed_graph.graph)
            input("Prima" + Fore.YELLOW + " ENTER " + Fore.RESET + "para continuar")
        elif option == 2:
            if dynamic_graph: dynamic_graph.desenha_freguesia()
            if fixed_graph: fixed_graph.draw_graph()
            input("Prima" + Fore.YELLOW + " ENTER " + Fore.RESET + "para continuar")
        elif option == 3:
            if fixed_graph: fixed_graph.draw_map()
            input("Prima" + Fore.YELLOW + " ENTER " + Fore.RESET + "para continuar")
        elif option == 4:
            print("Resolver com DFS")
            input("Prima" + Fore.YELLOW + " ENTER " + Fore.RESET + "para continuar")
        elif option == 5:
            print("Resolver com BFS")
            input("Prima" + Fore.YELLOW + " ENTER " + Fore.RESET + "para continuar")
        else:
            print(Fore.RED + "Opcao invalida." + Fore.RESET)
            input("Prima" + Fore.YELLOW + " ENTER " + Fore.RESET + "para continuar")

def exit():
    print(Fore.RED + "Exiting..." + Fore.RESET)
    sys.exit()

if __name__ == "__main__":
    main()