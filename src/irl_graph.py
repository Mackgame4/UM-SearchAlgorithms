import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
from classes.node import Node
from classes.zone import Zone
from classes.graph import Graph

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# TODO: Implement the IRLGraph class
# attention, in this class we would need to change the "draw_map" method to use the osmnx library
class IRLGraph(Graph):
    def __init__(self):
        super().__init__()
        self.address = "Piedmont, California, USA"
        self.graph_obj = None

        self.create_example_graph()

    def create_example_graph(self):
        self.graph_obj = ox.graph_from_address(self.address, network_type='drive')
        self.zones = {}
        # for each node in the graph_obj (location) add to the zones
        for node in self.graph_obj.nodes:
            self.zones[node] = Zone(node, 100, 0)
        # for each edge in the graph_obj (location) add to the edges
        for edge in self.graph_obj.edges:
            self.add_edge(self.zones[edge[0]], self.zones[edge[1]], 100, 10, True)