import networkx as nx
import matplotlib.pyplot as plt
from classes.node import Node
import geopandas as gpd
from classes.zone import Zone
from collections import deque
import warnings

warnings.filterwarnings("ignore", category=UserWarning)  # Hide UserWarning messages from geopandas

class Graph:
    def __init__(self):
        self.nodes = []
        self.graph = {}
        self.zones = {}
        self.camp = None

    def add_zone(self, zone):
        """Add a zone to the graph."""
        if not isinstance(zone, Zone):
            raise ValueError("Argument must be of type Zone")
        self.zones[zone.get_name()] = zone

    def add_edge(self, zone1, zone2, travel_time, fuel_cost, good_conditions):
        """Add an edge between two zones."""
        if not isinstance(zone1, Zone) or not isinstance(zone2, Zone):
            raise ValueError("Both arguments must be of type Zone")

        # Ensure the zones are added to the graph
        self.add_zone(zone1)
        self.add_zone(zone2)

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

        # Adding vehicles permitted for each edge
        self.graph[node1].append((node2, (travel_time, fuel_cost, good_conditions)))
        self.graph[node2].append((node1, (travel_time, fuel_cost, good_conditions)))  # Add edge in both directions (undirected graph)

    def bfs_with_vehicle(self, start_node_name, end_node_name, vehicle):
        if start_node_name not in self.graph or end_node_name not in self.graph:
            print(f"Node {start_node_name} or {end_node_name} not found in the graph")
            return None, None

        visited = set()
        queue = deque([(start_node_name, [start_node_name], 0, 0)])  # (current_node, path, total_cost, total_distance)

        while queue:
            current_node, path, total_cost, total_distance = queue.popleft()

            # Verifica se chegamos ao nó final
            if current_node == end_node_name:
                return path, total_cost

            if current_node not in visited:
                visited.add(current_node)

                for neighbor, (travel_time, fuel_cost, good_conditions) in self.graph[current_node]:
                    # Verifica se o veículo é permitido e se tem autonomia suficiente para o próximo trajeto
                    permitted_vehicles = self.zones[current_node].get_permitted_vehicles()
                    distance = travel_time  # A distância é equivalente ao tempo de viagem para simplificação

                    # Condição para verificar se o veículo é adequado para o trecho
                    if vehicle.get_tipo() in permitted_vehicles:
                        if good_conditions or vehicle.get_tipo() in {1, 2, 5}:  # Verifica se as condições são boas ou se o veículo é adequado
                            if vehicle.get_autonomia() >= (total_distance + distance):  # Verifica se a autonomia é suficiente
                                if neighbor not in visited:
                                    # Calcular o custo ponderado e adicionar à fila
                                    custo_ponderado = (distance / vehicle.get_velocidade()) + fuel_cost  # Exemplo de cálculo de custo
                                    queue.append((neighbor, path + [neighbor], total_cost + custo_ponderado, total_distance + distance))

        # Caso nenhum caminho seja encontrado
        print(f"No valid path found from {start_node_name} to {end_node_name}. Prioritizing finding a path...")
        return None, None

    # Other methods are unchanged

    def get_nodes(self):
        return self.nodes

    def add_node(self, node):
        self.nodes.append(node)

    def get_graph(self):
        return self.graph

    def get_zones(self):
        return self.zones

    def get_camp(self):
        return self.camp

    def set_zones(self, zones):
        self.zones = zones

    def add_zone(self, zone):
        self.zones[zone.get_name()] = zone

    def set_camp(self, camp):
        self.camp = camp

    def get_edges_data(self):
        edges = []
        for node in self.nodes:
            node_name = node.get_name()
            for (adjacente, (travel_time, fuel_cost, good_conditions)) in self.graph[node_name]:
                edges.append((node_name, adjacente, travel_time, fuel_cost, good_conditions))
        return edges

    def get_nodes_data(self):
        nodes = []
        for node in self.nodes:
            node_name = node.get_name()
            nodes.append((node_name, self.zones[node_name].get_population(), self.zones[node_name].get_severity(), self.zones[node_name].get_ttl(), self.zones[node_name].get_permitted_vehicles()))
        return nodes

    def draw_graph(self):
        g = nx.Graph()

        for node in self.nodes:
            node_name = node.get_name()
            g.add_node(node_name)
            for (adjacente, (travel_time, fuel_cost, good_conditions)) in self.graph[node_name]:
                g.add_edge(node_name, adjacente, travel_time=travel_time, fuel_cost=fuel_cost, good_conditions=good_conditions)

        pos = nx.spring_layout(g, seed=39)
        plt.figure(figsize=(12, 8))

        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold', node_size=800, node_color='skyblue')
        labels = {(u, v): f"({d['travel_time']}, {d['fuel_cost']}, {d['good_conditions']})" for u, v, d in g.edges(data=True)}
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.title("Graph of Zones")
        plt.show()

    def draw_map(self):
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        places = [node.get_name() for node in self.nodes]
        selected_countries = world[world['name'].isin(places)]

        fig, ax = plt.subplots(figsize=(12, 12))
        selected_countries.boundary.plot(ax=ax, color='lightgrey')

        max_severity = max([zone.get_severity() for zone in self.zones.values()])
        for zone in self.zones:
            zone_severity = self.zones[zone].get_severity()
            if zone_severity > 0:
                alpha_value = zone_severity / max_severity
                selected_countries[selected_countries['name'] == self.zones[zone].get_name()].plot(ax=ax, color='darkred', alpha=alpha_value)

        selected_countries[selected_countries['name'] == self.camp.get_name()].plot(ax=ax, color='blue')

        for _, row in selected_countries.iterrows():
            ax.text(row.geometry.centroid.x, row.geometry.centroid.y, row['name'], fontsize=8)

        max_travel_time = max([travel_time for node in self.nodes for (_, (travel_time, _, _)) in self.graph[node.get_name()]])
        for node in self.nodes:
            node_name = node.get_name()
            for (adjacente, (travel_time, fuel_cost, good_conditions)) in self.graph[node_name]:
                adjacente_country = world[world['name'] == adjacente]
                node_centroid_x = selected_countries[selected_countries['name'] == node_name].geometry.centroid.x.values[0]
                node_centroid_y = selected_countries[selected_countries['name'] == node_name].geometry.centroid.y.values[0]
                adjacente_centroid_x = adjacente_country.geometry.centroid.x.values[0]
                adjacente_centroid_y = adjacente_country.geometry.centroid.y.values[0]
                line_color = 'k-' if good_conditions else 'r-'
                ax.plot([node_centroid_x, adjacente_centroid_x], 
                        [node_centroid_y, adjacente_centroid_y], line_color, linewidth=travel_time/max_travel_time*3)
                ax.text((node_centroid_x + adjacente_centroid_x) / 2, 
                        ((node_centroid_y + adjacente_centroid_y) / 2) + 0.5,
                        str(fuel_cost), fontsize=12, color='black', fontweight='bold')

        def on_plot_hover(event):
            if event.xdata is None or event.ydata is None:
                return
            for zone in self.zones:
                zone_name = self.zones[zone].get_name()
                zone_severity = self.zones[zone].get_severity()
                zone_population = self.zones[zone].get_population()
                zone_country = world[world['name'] == zone_name]
                zone_ttl = self.zones[zone].get_ttl()
                zone_permitted_vehicles = self.zones[zone].get_permitted_vehicles()
                permitted_vehicles_list = ', '.join([str(vehicle) for vehicle in zone_permitted_vehicles])
                if not zone_country.empty:
                    geometry = zone_country.geometry.iloc[0]
                    if geometry.contains(Point(event.xdata, event.ydata)):
                        ax.set_title(f"Zone: {zone_name}\nPopulation: {zone_population}\nSeverity: {zone_severity}\nTTL: {zone_ttl}\nPermitted vehicles: [{permitted_vehicles_list}]")
                        fig.canvas.draw_idle()
                        break
                    else:
                        ax.set_title("Map of Zones")
                        fig.canvas.draw_idle()

        fig.canvas.mpl_connect('motion_notify_event', on_plot_hover)

        plt.title("Map of Zones")
        plt.axis('equal')
        ax.set_aspect('auto')

        ax.plot([], [], 'k-', label='Roads')
        ax.plot([], [], 'r-', label='Bad weather conditions')
        ax.plot([], [], 'k-', linewidth=4, label='Higher Travel time')
        ax.plot([], [], 'ro', label='Affected zone')
        ax.plot([], [], 'bo', label='ONU base')
        ax.legend()
        plt.show()
