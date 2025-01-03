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

class RandomGraph(Graph):
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

from classes.zone import Zone
from classes.graph import Graph
from classes.vehicle import VehicleType, VEHICLE_TYPES
import random
import geopandas as gpd
import networkx as nx  # Using NetworkX for graph connectivity check

import warnings
warnings.filterwarnings("ignore", category=FutureWarning) # Hide FutureWarning messages from geopandas

class DynamicGraph(Graph):
    def __init__(self, continent="Africa", edge_update_probability=0.2, max_edges_per_zone=2, fixed_affected_zones=2):
        """
        DynamicGraph creates a graph where the zones and streets are fixed but travel times and meteorologic conditions change.
        """
        super().__init__()
        self.continent = continent
        self.edge_update_probability = edge_update_probability
        self.max_edges_per_zone = max_edges_per_zone
        self.fixed_affected_zones = fixed_affected_zones
        self.zone_ttl_limits = (800, 980)
        self.zone_good_conditions_weights = [0.85, 0.15]
        self.zone_travel_time_limits = (30, 180)
        self.fuel_cost_limits = (35, 70)
        self.edge_vehicle_limits = (3, 4)

        self.create_fixed_graph()

    def create_fixed_graph(self):
        """
        Creates a fixed graph with static zones and edges, but dynamic travel times and conditions.
        """
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        continent = world[world['continent'] == self.continent]

        self.zones: dict[int, Zone] = {}
        for index, row in continent.iterrows():
            zone_ttl = random.randint(*self.zone_ttl_limits)  # Random TTL
            self.zones[index] = Zone(str(row['name']), int(row['pop_est']), 0, zone_ttl, False)

        # Set Angola as the camp zone by name
        camp_zone = None
        for zone in self.zones.values():
            if zone.get_name() == "Angola":
                camp_zone = zone
                break
        if camp_zone is None:
            raise ValueError("Angola not found in the zones.")
        
        camp_zone.set_camp(True)

        # Set Mali and Niger as the fixed affected zones
        mali_zone = None
        niger_zone = None
        for zone in self.zones.values():
            if zone.get_name() == "Mali":
                mali_zone = zone
            elif zone.get_name() == "Niger":
                niger_zone = zone
        
        if not mali_zone or not niger_zone:
            raise ValueError("Mali and/or Niger not found in the zones.")

        # Set severity for Mali and Niger
        mali_zone.set_severity(2)
        niger_zone.set_severity(4)

        # Create limited static edges between zones
        zone_keys = list(self.zones.keys())
        for zone1_key in zone_keys:
            zone1 = self.zones[zone1_key]
            neighbors_added = 0
            for zone2_key in random.sample(zone_keys, len(zone_keys)):
                if neighbors_added >= self.max_edges_per_zone:
                    break
                if zone1_key != zone2_key and not self.has_edge(self.zones[zone1_key], self.zones[zone2_key]):
                    zone2 = self.zones[zone2_key]
                    fuel_cost = random.randint(*self.fuel_cost_limits)
                    vehicles = set(
                        VehicleType(random.randint(0, VEHICLE_TYPES.__len__() - 1))
                        for _ in range(random.randint(*self.edge_vehicle_limits))
                    )
                    travel_time = random.randint(*self.zone_travel_time_limits)
                    good_conditions = random.choices(
                        [True, False], weights=self.zone_good_conditions_weights, k=1
                    )[0]

                    self.add_edge(zone1, zone2, travel_time, fuel_cost, good_conditions, vehicles)
                    neighbors_added += 1

        # Calculate heuristics for each zone
        for zone in self.zones.values():
            self.add_heuristic(zone.get_name(), self.heuristic_function(zone))

    def update_conditions(self):
        """
        Randomly update the travel times and conditions of edges based on the defined probability.
        This method will update the conditions of the edges in the graph (travel time and road conditions).
        """
        for node in self.nodes:
            node_name = node.get_name()
            for idx, (adjacente, (_, fuel_cost, _, vehicles)) in enumerate(self.graph[node_name]):
                # If the edge needs to be updated (based on probability)
                if random.random() < self.edge_update_probability:
                    # Update the travel time randomly
                    new_travel_time = random.randint(*self.zone_travel_time_limits)
                    # Randomly update the good conditions (True/False based on defined weights)
                    new_good_conditions = random.choices([True, False], weights=self.zone_good_conditions_weights, k=1)[0]
                    # Update the edge in the graph with the new values
                    self.graph[node_name][idx] = (adjacente, (new_travel_time, fuel_cost, new_good_conditions, vehicles))
                    # For undirected graphs, we also need to update the reverse edge
                    if not self.directed:
                        # Find the reverse edge (from adjacente to node_name) and update it
                        for rev_idx, (rev_adj, (_, _, _, _)) in enumerate(self.graph[adjacente]):
                            if rev_adj == node_name:
                                self.graph[adjacente][rev_idx] = (node_name, (new_travel_time, fuel_cost, new_good_conditions, vehicles))
                                break

    def simulate(self):
        """
        Run a simulation step that updates the edge conditions.
        """
        self.update_conditions()