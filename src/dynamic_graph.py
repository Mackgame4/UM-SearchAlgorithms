from classes.zone import Zone
from classes.graph import Graph
from classes.vehicle import Vehicle
import random
import geopandas as gpd

class DynamicGraph(Graph):
    def __init__(self, continent="Africa", max_edges_per_zone=3, max_affected_zones=2):
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