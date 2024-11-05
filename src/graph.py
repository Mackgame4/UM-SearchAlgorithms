import networkx as nx
import matplotlib.pyplot as plt
from node import Node
import geopandas as gpd
from zone import Zone

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

class FixedGraph:
    def __init__(self):
        self.nodes = []
        self.graph = {}
        self.zones = {}
        self.camp_zone = None

        # Create example graph
        self.example_graph()

    def example_graph(self):
        # Create nodes
        self.zones = {
            0: Zone("Botswana", 100, 2), # Most affected zone
            1: Zone("Namibia", 400, 1), # Affected zone
            2: Zone("Zimbabwe", 300, 0),
            3: Zone("Angola", 400, 0),
            4: Zone("Zambia", 500, 0),
            5: Zone("Tanzania", 600, 0),
            6: Zone("Malawi", 700, 0)
        }
        self.camp = self.zones[5] # ONU base
        self.add_edge(self.zones[0], self.zones[1], 100, 10, True)
        self.add_edge(self.zones[0], self.zones[2], 200, 8, True)
        self.add_edge(self.zones[0], self.zones[3], 120, 15, True)
        self.add_edge(self.zones[0], self.zones[4], 110, 12, True)
        self.add_edge(self.zones[4], self.zones[2], 170, 9, True)
        self.add_edge(self.zones[4], self.zones[5], 190, 7, True)
        self.add_edge(self.zones[4], self.zones[3], 130, 10, True)
        self.add_edge(self.zones[1], self.zones[3], 120, 11, False)
        self.add_edge(self.zones[1], self.zones[4], 100, 9, True)
        self.add_edge(self.zones[6], self.zones[4], 90, 8, True)
        self.add_edge(self.zones[6], self.zones[5], 95, 7, True)
        self.add_edge(self.zones[6], self.zones[2], 125, 20, False)

    def add_edge(self, zone1, zone2, travel_time, fuel_cost, good_conditions):
        node1 = zone1.get_name()
        node2 = zone2.get_name()
        n1 = Node(node1)
        n2 = Node(node2)
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
        self.graph[node1].append((node2, (travel_time, fuel_cost, good_conditions)))
        self.graph[node2].append((node1, (travel_time, fuel_cost, good_conditions))) # Add edge in both directions (undirected graph)

    def get_nodes(self):
        return self.nodes

    # draw graph as a normal graph with nodes and edges
    def draw_graph(self):
        g = nx.Graph()
        
        for node in self.nodes:
            node_name = node.get_name()
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
        places = [node.get_name() for node in self.nodes]
        selected_countries = world[world['name'].isin(places)]

        # Plotting the boundaries
        _, ax = plt.subplots(figsize=(12, 12))
        selected_countries.boundary.plot(ax=ax, color='lightgrey')

        # From the selected countries, paint the most affected zone in red (the higher value of severity the more dark red it is)
        max_severity = max([zone.get_severity() for zone in self.zones.values()])
        for zone in self.zones:
            zone_severity = self.zones[zone].get_severity()
            if zone_severity > 0:
                alpha_value = zone_severity / max_severity
                selected_countries[selected_countries['name'] == self.zones[zone].get_name()].plot(ax=ax, color='darkred', alpha=alpha_value)

        # Paint the camp zone in blue
        selected_countries[selected_countries['name'] == self.camp.get_name()].plot(ax=ax, color='blue')
        
        # Add name of the countries
        for _, row in selected_countries.iterrows():  # Iterate over each row in the GeoDataFrame
            ax.text(row.geometry.centroid.x, row.geometry.centroid.y, row['name'], fontsize=8)

        # Draw the edges (roads/lines) between the countries
        max_travel_time = max([travel_time for node in self.nodes for (_, (travel_time, _, _)) in self.graph[node.get_name()]])
        for node in self.nodes:
            node_name = node.get_name()
            for (adjacente, (travel_time, fuel_cost, good_conditions)) in self.graph[node_name]:
                adjacente_country = world[world['name'] == adjacente]
                # Get centroids for the two countries
                node_centroid_x = selected_countries[selected_countries['name'] == node_name].geometry.centroid.x.values[0]
                node_centroid_y = selected_countries[selected_countries['name'] == node_name].geometry.centroid.y.values[0]
                adjacente_centroid_x = adjacente_country.geometry.centroid.x.values[0]
                adjacente_centroid_y = adjacente_country.geometry.centroid.y.values[0]
                # Draw a line between the two countries
                line_color = 'k-' if good_conditions else 'r-'
                ax.plot([node_centroid_x, adjacente_centroid_x], 
                        [node_centroid_y, adjacente_centroid_y], line_color, linewidth=travel_time/max_travel_time*3)
                ax.text((node_centroid_x + adjacente_centroid_x) / 2, 
                        ((node_centroid_y + adjacente_centroid_y) / 2) + 0.5, # Add a offset to the y coordinate so the text doesn't overlap the line 
                        str(fuel_cost), fontsize=12, color='black', fontweight='bold')
        
        ax.set_title("Map of Southern Africa")
        #plt.axis('equal') # Maintain aspect ratio
        ax.set_aspect('auto')

        # add legend
        ax.plot([], [], 'k-', label='Roads')
        ax.plot([], [], 'r-', label='Bad weather conditions')
        ax.plot([], [], 'k-', linewidth=4, label='Higher Travel time')
        #ax.plot([], [], 'b-', label='Taken path')
        ax.plot([], [], 'ro', label='Affected zone')
        ax.plot([], [], 'bo', label='ONU base')
        ax.legend()
        plt.show()