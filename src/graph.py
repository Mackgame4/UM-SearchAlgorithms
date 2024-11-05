import networkx as nx
import matplotlib.pyplot as plt
from node import Node
import geopandas as gpd
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

class FixedGraph:
    def __init__(self):
        self.nodes = []
        self.graph = {}

        # Create example graph
        self.example_graph()

    def example_graph(self):
        self.add_edge("Botswana", "Namibia", 1, 10, 1)
        self.add_edge("Botswana", "Zimbabwe", 1, 8, 1)
        self.add_edge("Botswana", "Angola", 2, 15, 0)
        self.add_edge("Botswana", "Zambia", 1, 12, 1)
        self.add_edge("Zambia", "Zimbabwe", 1, 9, 1)
        self.add_edge("Zambia", "Tanzania", 1, 7, 1)
        self.add_edge("Zambia", "Angola", 1, 10, 1)
        self.add_edge("Namibia", "Angola", 1, 11, 0)
        self.add_edge("Namibia", "Zambia", 1, 9, 1)
        self.add_edge("Malawi", "Zambia", 1, 8, 1)
        self.add_edge("Malawi", "Tanzania", 1, 7, 1)
        self.add_edge("Malawi", "Zimbabwe", 3, 20, 0)

    def add_edge(self, node1, node2, travel_time, fuel_cost, good_conditions):
        n1 = Node(node1)
        n2 = Node(node2)
        if n1 not in self.nodes:
            n1_id = len(self.nodes)
            n1.setId(n1_id)
            self.nodes.append(n1)
            self.graph[node1] = []
        if n2 not in self.nodes:
            n2_id = len(self.nodes)
            n2.setId(n2_id)
            self.nodes.append(n2)
            self.graph[node2] = []
        self.graph[node1].append((node2, (travel_time, fuel_cost, good_conditions)))
        self.graph[node2].append((node1, (travel_time, fuel_cost, good_conditions))) # Add edge in both directions (undirected graph)

    def getNodes(self):
        return self.nodes

    # draw graph as a normal graph with nodes and edges
    def draw_graph(self):
        g = nx.Graph()
        
        for node in self.nodes:
            node_name = node.getName()
            g.add_node(node_name)
            for (adjacente, (travel_time, fuel_cost, good_conditions)) in self.graph[node_name]:
                # Set separate attributes for each edge
                g.add_edge(node_name, adjacente, travel_time=travel_time, fuel_cost=fuel_cost, good_conditions=good_conditions)

        pos = nx.spring_layout(g, seed=39)
        plt.figure(figsize=(12, 8))

        # Draw nodes and edges
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold', node_size=800, node_color='skyblue')
        
        # Create custom labels that display the three attributes
        labels = {(u, v): f"({d['travel_time']}, {d['fuel_cost']}, {d['good_conditions']})"
                for u, v, d in g.edges(data=True)}
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.title("Map of Southern Africa")
        plt.show()

    # draw map using OSMnx
    def draw_map(self):
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        places = [node.getName() for node in self.nodes]
        selected_countries = world[world['name'].isin(places)]

        # Plotting the boundaries
        fig, ax = plt.subplots(figsize=(12, 12))
        selected_countries.boundary.plot(ax=ax, color='lightgrey')
        #world.boundary.plot(ax=ax, color='lightgrey') # Optional: to show all countries
        
        # add name of the countries
        for x, y, label in zip(selected_countries.geometry.centroid.x, selected_countries.geometry.centroid.y, selected_countries['name']):
            ax.text(x, y, label, fontsize=8)

        # draw the edges (roads/lines) between the countries
        for node in self.nodes:
            node_name = node.getName()
            for (adjacente, (travel_time, fuel_cost, good_conditions)) in self.graph[node_name]:
                adjacente_country = world[world['name'] == adjacente]
                plt.plot([selected_countries[selected_countries['name'] == node_name].geometry.centroid.x.values[0], adjacente_country.geometry.centroid.x.values[0]], 
                        [selected_countries[selected_countries['name'] == node_name].geometry.centroid.y.values[0], adjacente_country.geometry.centroid.y.values[0]], 'k-')
        
        ax.set_title("Map of Southern Africa")
        #plt.axis('equal') # Maintain aspect ratio
        plt.show()