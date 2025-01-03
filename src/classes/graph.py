import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd
import math
from shapely.geometry import Point
from typing import Any

from classes.zone import Zone
from classes.zone import Zone

import warnings
warnings.filterwarnings("ignore", category=UserWarning) # Hide UserWarning messages from geopandas

class Graph:
    def __init__(self, directed: bool=False):
        """
        Representa um grafo.
        :param directed: Booleano indicando se o grafo é direcionado.
        """
        self.graph: dict[str, list[Any]] = {}
        self.nodes: list[Zone] = []
        self.directed = directed
        self.heuristics: dict[str, int] = {}

    """ Getters """
    def get_nodes(self) -> list[Zone]:
        return self.nodes
    
    def get_node(self, node: str) -> Zone:
        for n in self.nodes:
            if n.get_name() == node:
                return n
        return None
    
    def get_heuristics(self) -> dict[str, int]:
        return self.heuristics
    
    def get_heuristic(self, node: str) -> int:
        if node not in self.heuristics.keys():
            return math.inf
        else:
            return self.heuristics[node]
    
    def get_graph(self) -> dict[str, list[Any]]:
        return self.graph
    
    def is_directed(self) -> bool:
        return self.directed
    
    """ Setters """
    def add_node(self, node: Zone):
        self.nodes.append(node)

    def add_heuristic(self, node: str, value: int):
        n1 = Zone(node)
        if n1 in self.nodes:
            self.heuristics[node] = value

    def set_directed(self, directed: bool):
        self.directed = directed

    def set_graph(self, graph: dict[str, list[Any]]):
        self.graph = graph

    """ Methods """
    def add_edge(self, zone1: Zone, zone2: Zone, travel_time: int, fuel_cost: int, good_conditions: bool, vehicles: set):
        """
        Add an edge between two zones.
        :param zone1: Zone 1.
        :param zone2: Zone 2.
        :param travel_time: Travel time between the two zones.
        :param fuel_cost: Fuel cost between the two zones.
        :param good_conditions: Boolean indicating if the road conditions are good.
        :param vehicles: List of vehicles permitted for the edge.
        """
        if not isinstance(zone1, Zone) or not isinstance(zone2, Zone):
            raise ValueError("Both arguments must be of type Zone.")
        # Ensure the zones are added to the graph
        node1 = zone1.get_name()
        node2 = zone2.get_name()
        if zone1 not in self.nodes:
            self.add_node(zone1)
            self.graph[node1] = []
        if zone2 not in self.nodes:
            self.add_node(zone2)
            self.graph[node2] = []
        # Adding vehicles permitted for each edge
        self.graph[node1].append((node2, (travel_time, fuel_cost, good_conditions, vehicles)))
        if not self.directed:
            self.graph[node2].append((node1, (travel_time, fuel_cost, good_conditions, vehicles))) # Add edge in both directions (undirected graph)

    def has_edge(self, zone1: Zone, zone2: Zone) -> bool:
        """
        Check if there is an edge between two zones.
        :param zone1: Zone 1.
        :param zone2: Zone 2.
        :return: True if there is an edge between the two zones, False otherwise.
        """
        if not isinstance(zone1, Zone) or not isinstance(zone2, Zone):
            raise ValueError("Both arguments must be of type Zone.")
        node1 = zone1.get_name()
        node2 = zone2.get_name()
        if node1 in self.graph:
            for (adjacente, _) in self.graph[node1]:
                if adjacente == node2:
                    return True
        return False

    def print_nodes(self):
        for node in self.nodes:
            print("Zone:", node.get_name(), node.get_population(), node.get_severity(), node.get_ttl(), node.is_camp())

    def print_edges(self):
        for node in self.nodes:
            node_name = node.get_name()
            print(f"Node: {node_name}")
            for (adjacente, (travel_time, fuel_cost, good_conditions, vehicles)) in self.graph[node_name]:
                print(f"  -> {adjacente} ({travel_time}, {fuel_cost}, {good_conditions}, {vehicles})")

    def heuristic_function(self, node: Zone) -> int:
        """
        Calculate the heuristic value for a node. (Heuristic function definition)
        :param node: Node for which to calculate the heuristic.
        :return: Heuristic value for the node.
        """
        return node.get_severity() * 100 + node.get_population() // 100

    def edge_cost_function(self, node1: Zone, node2: Zone) -> int:
        """
        Calculate the cost of an edge between two nodes. (Cost function definition)
        :param node1: Node 1.
        :param node2: Node 2.
        :return: Cost of the edge between the two nodes.
        """
        # o custo será o tempo de viagem entre os dois nodos a dividir pelo custo do combustível e se não houver boas condições o tempo é 1.5 vezes maior
        formula = lambda travel_time, fuel_cost, good_conditions: travel_time / fuel_cost if good_conditions else travel_time / fuel_cost * 1.5
        costAux = math.inf
        node_edges = self.graph[node1] # lista de arestas para aquele nodo
        for (node, (travel_time, fuel_cost, good_conditions, _)) in node_edges:
            if node == node2:
                costAux = formula(travel_time, fuel_cost, good_conditions)
        return costAux
    
    def calcula_custo(self, path: list[str]) -> int:
        """
        Calculate the cost of a path.
        :param path: List of nodes in the path.
        :return: Cost of the path.
        """
        cost = 0
        for i in range(len(path) - 1):
            cost += self.edge_cost_function(path[i], path[i + 1])
        return cost

    def get_camp_node(self) -> str:
        """
        Get the name of the camp node.
        :return: Name of the camp node.
        """
        for node in self.nodes:
            if node.is_camp():
                return node.get_name()
        return None
    
    def get_affected_nodes(self) -> list[str]:
        """
        Get the names of the affected zones (zones with severity > 0).
        :return: List of affected zones.
        """
        affected_nodes = []
        for node in self.nodes:
            if node.get_severity() > 0:
                affected_nodes.append(node.get_name())
        return affected_nodes
    
    def get_neighbours(self, node: str) -> list:
        """
        Get the neighbours of a node.
        :param node: Name of the node.
        :return: List of neighbours of the node.
        """
        neighbours = []
        for (adjacente, (travel_time, fuel_cost, good_conditions, vehicles)) in self.graph[node]:
            neighbours.append((adjacente, travel_time, fuel_cost, good_conditions, vehicles))
        return neighbours

    def draw_graph(self):
        g = nx.Graph()
        for node in self.nodes:
            node_name = node.get_name()
            g.add_node(node_name)
            for (adjacente, (travel_time, fuel_cost, good_conditions, vehicles)) in self.graph[node_name]:
                g.add_edge(node_name, adjacente, travel_time=travel_time, fuel_cost=fuel_cost, good_conditions=good_conditions, vehicles=vehicles)
        pos = nx.spring_layout(g, seed=39) # Seed for reproducibility of the graph layout
        plt.figure(figsize=(12, 8))
        plt.subplots_adjust(left=0, right=1, top=0.95, bottom=0) # Make it full screen without margins but keep room for the title
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold', node_size=800, node_color='skyblue')
        labels = {(u, v): f"({d['travel_time']}, {d['fuel_cost']}, {d['good_conditions']}, {d['vehicles']})" for u, v, d in g.edges(data=True)}
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
        plt.title("Graph of Zones")
        plt.show()

    def draw_map(self):
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        places = [node.get_name() for node in self.nodes]
        selected_countries = world[world['name'].isin(places)] # Filter only the countries in the graph
        fig, ax = plt.subplots(figsize=(12, 8))
        selected_countries.boundary.plot(ax=ax, color='lightgrey') # Draw the boundaries of the countries
        # Paint the countries according to the severity of the zones
        max_severity = max([node.get_severity() for node in self.nodes])
        for node in self.nodes:
            zone_severity = node.get_severity()
            if zone_severity > 0:
                alpha_value = zone_severity / max_severity
                selected_countries[selected_countries['name'] == node.get_name()].plot(ax=ax, color='darkred', alpha=alpha_value)
        # Paint the camp country in blue
        camp_country = None
        for node in self.nodes:
            if node.is_camp():
                camp_country = node.get_name()
                break
        if camp_country:
            selected_countries[selected_countries['name'] == camp_country].plot(ax=ax, color='blue')
        # Add the name of the countries
        for _, row in selected_countries.iterrows():
            ax.text(row.geometry.centroid.x, row.geometry.centroid.y, row['name'], fontsize=8)
        # Draw the roads between the countries
        max_travel_time = max([travel_time for node in self.nodes for (_, (travel_time, _, _, _)) in self.graph[node.get_name()]])
        for node in self.nodes:
            node_name = node.get_name()
            for (adjacente, (travel_time, fuel_cost, good_conditions, vehicles)) in self.graph[node_name]:
                adjacente_country = world[world['name'] == adjacente]
                node_centroid_x = selected_countries[selected_countries['name'] == node_name].geometry.centroid.x.values[0]
                node_centroid_y = selected_countries[selected_countries['name'] == node_name].geometry.centroid.y.values[0]
                adjacente_centroid_x = adjacente_country.geometry.centroid.x.values[0]
                adjacente_centroid_y = adjacente_country.geometry.centroid.y.values[0]
                line_color = 'k-' if good_conditions else 'r-'
                permitted_vehicles = ', '.join([str(vehicle) for vehicle in vehicles])
                road_label = f"({fuel_cost}, {permitted_vehicles})"
                ax.plot([node_centroid_x, adjacente_centroid_x], [node_centroid_y, adjacente_centroid_y], line_color, linewidth=travel_time/max_travel_time*3)
                ax.text((node_centroid_x + adjacente_centroid_x) / 2, ((node_centroid_y + adjacente_centroid_y) / 2) + 0.5, road_label, fontsize=12, color='black', fontweight='bold')
        # Hovering over the countries to show the zone information
        def on_plot_hover(event):
            if event.xdata is None or event.ydata is None:
                return
            for node in self.nodes:
                zone_name = node.get_name()
                zone_country = world[world['name'] == zone_name]
                zone_heuristic = self.get_heuristic(zone_name)
                if not zone_country.empty:
                    geometry = zone_country.geometry.iloc[0]
                    if geometry.contains(Point(event.xdata, event.ydata)):
                        ax.set_title(f"Zone: {zone_name}\nPopulation: {node.get_population()}\nSeverity: {node.get_severity()}\nTTL: {node.get_ttl()}\nCamp: {node.is_camp()}\nHeuristic: {zone_heuristic}")
                        fig.canvas.draw_idle()
                        break
                    else:
                        ax.set_title("Map of Zones")
                        fig.canvas.draw_idle()
        fig.canvas.mpl_connect('motion_notify_event', on_plot_hover)
        # Add the legend
        plt.title("Map of Zones")
        plt.subplots_adjust(left=0.04, right=1, top=0.83, bottom=0.05)
        plt.axis('equal')
        ax.set_aspect('auto')
        ax.plot([], [], 'k-', label='Road (Fuelt Cost, Permitted Vehicles)')
        ax.plot([], [], 'r-', label='Bad Weather Conditions')
        ax.plot([], [], 'k-', linewidth=4, label='Higher Travel Time')
        ax.plot([], [], 'ro', label='Affected Zone')
        ax.plot([], [], 'bo', label='Camp Base')
        ax.legend()
        plt.show()