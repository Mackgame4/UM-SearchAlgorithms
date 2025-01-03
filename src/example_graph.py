from classes.zone import Zone
from classes.graph import Graph
from classes.vehicle import VehicleType, VEHICLE_TYPES
import random
import geopandas as gpd
import networkx as nx  # Using NetworkX for graph connectivity check

import warnings
warnings.filterwarnings("ignore", category=FutureWarning) # Hide FutureWarning messages from geopandas

class FixedGraph(Graph): # Inherit from Graph
    def __init__(self):
        """
        FixedGraph extends graph and creates a fixed graph with fixed zones and edges (defined manually).
        """
        super().__init__() # Initialize the parent Graph class
        self.example_graph() # Set up the example graph

    def example_graph(self):
        # Create nodes
        self.zones = {
            0: Zone("Botswana", 100, 0, 700, False),
            1: Zone("Namibia", 400, 0, 400, False),
            2: Zone("Zimbabwe", 300, 0, 600, False),
            3: Zone("Angola", 400, 0, 500, True), # Camp base
            4: Zone("Zambia", 500, 0, 800, False),
            5: Zone("Tanzania", 600, 1, 900, False), # Affected zone
            6: Zone("Malawi", 700, 2, 1000, False) # Most affected zone
        }
        self.add_edge(self.zones[0], self.zones[1], 100, 10, True, {VehicleType(0), VehicleType(1), VehicleType(2)})
        self.add_edge(self.zones[0], self.zones[2], 70, 18, True, {VehicleType(2), VehicleType(3), VehicleType(0)})
        self.add_edge(self.zones[0], self.zones[3], 55, 25, True, {VehicleType(0), VehicleType(3), VehicleType(4)})
        self.add_edge(self.zones[0], self.zones[4], 110, 22, True, {VehicleType(1), VehicleType(2), VehicleType(3)})
        self.add_edge(self.zones[4], self.zones[2], 40, 90, True, {VehicleType(0), VehicleType(1), VehicleType(2)})
        self.add_edge(self.zones[4], self.zones[5], 190, 27, True, {VehicleType(2), VehicleType(3), VehicleType(4)})
        self.add_edge(self.zones[4], self.zones[3], 130, 30, True, {VehicleType(0), VehicleType(1), VehicleType(3)})
        self.add_edge(self.zones[1], self.zones[3], 70, 11, False, {VehicleType(2), VehicleType(3), VehicleType(4)})
        self.add_edge(self.zones[1], self.zones[4], 80, 19, True, {VehicleType(0), VehicleType(1), VehicleType(2)})
        self.add_edge(self.zones[6], self.zones[4], 90, 28, True, {VehicleType(2), VehicleType(3), VehicleType(4)})
        self.add_edge(self.zones[6], self.zones[5], 95, 37, True, {VehicleType(0), VehicleType(1), VehicleType(2)})
        self.add_edge(self.zones[6], self.zones[2], 115, 20, False, {VehicleType(2), VehicleType(3), VehicleType(4)})
        for zone in self.zones.values():
            self.add_heuristic(zone.get_name(), self.heuristic_function(zone))

class DynamicGraph(Graph):
    def __init__(self, continent="Africa", max_edges_per_zone=1, max_affected_zones=2, edge_max_vehicles=4):
        super().__init__()
        self.continent = continent
        self.max_edges_per_zone = max_edges_per_zone
        self.max_affected_zones = max_affected_zones
        self.zone_severity_limits = (2, 4)
        self.zone_travel_time_limits = (30, 180)
        self.zone_fuel_cost_limits = (35, 70)
        self.zone_good_conditions_weights = [0.85, 0.15]
        self.zone_ttl_limits = (800, 980)
        self.edge_vehicle_limits = (3, edge_max_vehicles)
        self.example_graph()

    def example_graph(self):
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        continent = world[world['continent'] == self.continent]
        # Initialize zones with each country
        self.zones: dict[int, Zone] = {}
        for index, row in continent.iterrows():
            zone_ttl = random.randint(*self.zone_ttl_limits)  # Random TTL
            self.zones[index] = Zone(str(row['name']), int(row['pop_est']), 0, zone_ttl, False)
        # Randomly choose one country as the camp
        camp_zone = random.choice(list(self.zones.values()))
        camp_zone.set_camp(True)
        # Randomly choose countries to be affected
        affected_zones = random.sample(list(self.zones.values()), self.max_affected_zones)
        for zone in affected_zones:
            zone.set_severity(random.randint(*self.zone_severity_limits))
        # Create edges between zones
        zone_keys = list(self.zones.keys())  # Get zone keys
        for i in range(len(zone_keys)):
            zone1 = self.zones[zone_keys[i]]
            neighbors_added = 0
            for j in range(i + 1, len(zone_keys)):
                zone2 = self.zones[zone_keys[j]]
                if neighbors_added >= self.max_edges_per_zone:
                    break
                if random.random() < 0.15:  # 15% chance of connecting any two zones
                    travel_time = random.randint(*self.zone_travel_time_limits)
                    fuel_cost = random.randint(*self.zone_fuel_cost_limits)
                    good_conditions = random.choices([True, False], weights=self.zone_good_conditions_weights, k=1)[0]
                    vehicles = set()
                    for _ in range(random.randint(*self.edge_vehicle_limits)):
                        vehicles.add(VehicleType(random.randint(0, VEHICLE_TYPES.__len__() - 1)))
                    self.add_edge(zone1, zone2, travel_time, fuel_cost, good_conditions, vehicles)
                    neighbors_added += 1
        # Ensure connectivity by checking the graph
        self.ensure_connectivity()
        # Calculate heuristics for each zone
        for zone in self.zones.values():
            self.add_heuristic(zone.get_name(), self.heuristic_function(zone))

    def ensure_connectivity(self):
        """
        Ensure that the graph is connected. If not, add edges to make it connected.
        """
        # Create a simple NetworkX graph for checking connectivity
        g = nx.Graph()
        for zone in self.zones.values():
            g.add_node(zone.get_name())  # Add nodes
        # Add edges from the graph
        for zone1 in self.zones.values():
            for zone2 in self.zones.values():
                if self.has_edge(zone1, zone2):
                    g.add_edge(zone1.get_name(), zone2.get_name())  # Add edges
        # Check for connected components
        components = list(nx.connected_components(g))
        if len(components) > 1:
            # If there are more than one component, randomly connect them
            for i in range(len(components) - 1):
                zone1_name = list(components[i])[0]
                zone2_name = list(components[i + 1])[0]
                zone1 = self.get_node(zone1_name)
                zone2 = self.get_node(zone2_name)
                travel_time = random.randint(*self.zone_travel_time_limits)
                fuel_cost = random.randint(*self.zone_fuel_cost_limits)
                good_conditions = random.choices([True, False], weights=self.zone_good_conditions_weights, k=1)[0]
                vehicles = set()
                for _ in range(random.randint(*self.edge_vehicle_limits)):
                    vehicles.add(VehicleType(random.randint(0, VEHICLE_TYPES.__len__() - 1)))
                if zone1 and zone2:
                    self.add_edge(zone1, zone2, travel_time, fuel_cost, good_conditions, vehicles)

"""
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
"""