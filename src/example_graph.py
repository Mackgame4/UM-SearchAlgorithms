from classes.zone import Zone
from classes.graph import Graph
from classes.vehicle import Vehicle, VehicleType
import random
import geopandas as gpd

import warnings
warnings.filterwarnings("ignore", category=FutureWarning) # Hide FutureWarning messages from geopandas

class FixedGraph(Graph): # Inherit from Graph
    """
    FixedGraph extends graph and creates a fixed graph with fixed zones and edges (defined manually).
    """
    def __init__(self):
        super().__init__() # Initialize the parent Graph class
        self.example_graph() # Set up the example graph

    def example_graph(self):
        # Create nodes
        self.zones = {
            0: Zone("Botswana", 100, 2, 700, False), # Most affected zone
            1: Zone("Namibia", 400, 1, 400, False), # Affected zone
            2: Zone("Zimbabwe", 300, 0, 600, False),
            3: Zone("Angola", 400, 0, 500, True), # Camp base
            4: Zone("Zambia", 500, 0, 800, False),
            5: Zone("Tanzania", 600, 0, 900, False),
            6: Zone("Malawi", 700, 0, 1000, False)
        }
        self.add_edge(self.zones[0], self.zones[1], 100, 10, True, {VehicleType(0), VehicleType(1)})
        self.add_edge(self.zones[0], self.zones[2], 200, 8, True, {VehicleType(2), VehicleType(3)})
        self.add_edge(self.zones[0], self.zones[3], 120, 15, True, {VehicleType(0), VehicleType(3)})
        self.add_edge(self.zones[0], self.zones[4], 110, 12, True, {VehicleType(1), VehicleType(2), VehicleType(3)})
        self.add_edge(self.zones[4], self.zones[2], 170, 9, True, {VehicleType(0), VehicleType(1)})
        self.add_edge(self.zones[4], self.zones[5], 190, 7, True, {VehicleType(2), VehicleType(3)})
        self.add_edge(self.zones[4], self.zones[3], 130, 10, True, {VehicleType(0), VehicleType(1)})
        self.add_edge(self.zones[1], self.zones[3], 120, 11, False, {VehicleType(2), VehicleType(3)})
        self.add_edge(self.zones[1], self.zones[4], 100, 9, True, {VehicleType(0), VehicleType(1)})
        self.add_edge(self.zones[6], self.zones[4], 90, 8, True, {VehicleType(2), VehicleType(3)})
        self.add_edge(self.zones[6], self.zones[5], 95, 7, True, {VehicleType(0), VehicleType(1)})
        self.add_edge(self.zones[6], self.zones[2], 125, 20, False, {VehicleType(2), VehicleType(3)})
        # Heuristica é a gravidade da zone (definição da Função de Heuristica)
        for zone in self.zones.values():
            self.add_heuristic(zone.get_name(), zone.get_severity())

class DynamicGraph(Graph):
    def __init__(self, continent="Africa", max_edges_per_zone=3, max_affected_zones=2):
        """
        DynamicGraph extends graph and creates a dynamic graph with random zones and edges.
        :param continent: Continent to generate the graph.
        :param max_edges_per_zone: Maximum number of edges per zone.
        :param max_affected_zones: Maximum number of affected zones.
        """
        super().__init__()
        self.continent = continent
        self.max_edges_per_zone = max_edges_per_zone
        self.max_affected_zones = max_affected_zones
        self.zone_severity_limits = (0, 4)
        self.zone_travel_time_limits = (30, 200)
        self.zone_fuel_cost_limits = (5, 10)
        self.zone_good_conditions_weights = [0.85, 0.15]  # 85% chance of good conditions
        self.zone_ttl_limits = (80, 480)
        self.zone_max_vehicles = 5

        self.example_graph()

    def example_graph(self):
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        continent = world[world['continent'] == self.continent]

        # Initialize zones with each country
        self.zones = {}
        for index, row in continent.iterrows():
            zone_ttl = random.randint(*self.zone_ttl_limits)  # Random TTL
            veh = Vehicle()
            veh_types = veh.get_tipos()  # Get vehicle types
            zone_vehicles = set(random.choices(list(veh_types.values()), k=random.randint(2, self.zone_max_vehicles)))  # At least 2 vehicles per zone
            self.zones[index] = Zone(str(row['name']), int(row['pop_est']), 0, zone_ttl, zone_vehicles)  # Just add the zone, no severity

        # Randomly choose one country as the camp
        self.set_camp(random.choice(list(self.zones.values())))

        # Randomly choose neighbors countries to be affected (where the disaster occurred)
        affected_zones = random.sample(list(self.zones.values()), self.max_affected_zones)
        for zone in affected_zones:
            zone.set_severity(random.randint(*self.zone_severity_limits))  # Random severity level

        # Randomly add edges between countries
        zone_keys = list(self.zones.keys())  # Get zone keys
        for i in range(len(zone_keys)):
            zone1 = self.zones[zone_keys[i]]
            neighbors_added = 0
            for j in range(i + 1, len(zone_keys)):
                zone2 = self.zones[zone_keys[j]]

                # Limit each zone to a fixed number of connections for better readability
                if neighbors_added >= self.max_edges_per_zone:
                    break

                # Randomly decide whether to add an edge
                if random.random() < 0.15:  # 15% chance of connecting any two zones
                    travel_time = random.randint(*self.zone_travel_time_limits)
                    fuel_cost = random.randint(*self.zone_fuel_cost_limits)
                    good_conditions = random.choices([True, False], weights=self.zone_good_conditions_weights, k=1)[0]  # Having good conditions is more likely
                    self.add_edge(zone1, zone2, travel_time, fuel_cost, good_conditions)
                    neighbors_added += 1

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