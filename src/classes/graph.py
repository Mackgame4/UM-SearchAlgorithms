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
    
    def get_graph(self) -> dict[str, list[Any]]:
        return self.graph
    
    def get_heuristics(self) -> dict[str, int]:
        return self.heuristics
    
    def is_directed(self) -> bool:
        return self.directed
    
    """ Setters """
    def add_node(self, node: Zone):
        self.nodes.append(node)

    def set_heuristic(self, node: str, value: int):
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
        n1 = Zone(node1)
        n2 = Zone(node2)
        if n1 not in self.nodes:
            n1_id = len(self.nodes)
            n1.set_id(n1_id)
            self.nodes.append(n1)
            self.graph[node1] = []
        if n2 not in self.nodes:
            n2_id = len(self.nodes)
            n2.set_id(n2_id)
            self.nodes.append(n2)
            self.graph[node2] = []
        # Adding vehicles permitted for each edge
        self.graph[node1].append((node2, (travel_time, fuel_cost, good_conditions, vehicles)))
        if not self.directed:
            self.graph[node2].append((node1, (travel_time, fuel_cost, good_conditions, vehicles))) # Add edge in both directions (undirected graph)

    def print_edges(self) -> dict[str, list[Any]]:
        for node in self.nodes:
            node_name = node.get_name()
            print(f"Node: {node_name}")
            for (adjacente, (travel_time, fuel_cost, good_conditions, vehicles)) in self.graph[node_name]:
                print(f"  -> {adjacente} ({travel_time}, {fuel_cost}, {good_conditions}, {vehicles})")

    def draw_graph(self):
        g = nx.Graph()
        for node in self.nodes:
            node_name = node.get_name()
            g.add_node(node_name)
            for (adjacente, (travel_time, fuel_cost, good_conditions, vehicles)) in self.graph[node_name]:
                g.add_edge(node_name, adjacente, travel_time=travel_time, fuel_cost=fuel_cost, good_conditions=good_conditions, vehicles=vehicles)
        pos = nx.spring_layout(g, seed=39)
        plt.figure(figsize=(12, 8))
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold', node_size=800, node_color='skyblue')
        labels = {(u, v): f"({d['travel_time']}, {d['fuel_cost']}, {d['good_conditions']}, {d['vehicles']})" for u, v, d in g.edges(data=True)}
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
        plt.title("Graph of Zones")
        plt.show()