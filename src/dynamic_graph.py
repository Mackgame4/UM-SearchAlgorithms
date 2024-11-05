from zone import Zone
from graph import Graph
import random
import geopandas as gpd

# DynamicGraph extends graph and creates a random graph with random zones and edges
class DynamicGraph(Graph):
    def __init__(self, continent="Africa", max_edges_per_zone=3, max_affected_zones=2):
        super().__init__()
        self.continent = continent
        self.max_edges_per_zone = max_edges_per_zone
        self.max_affected_zones = max_affected_zones

        self.example_graph()

    def example_graph(self):
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        continent = world[world['continent'] == self.continent]

        # Initialize zones with each country
        self.zones = {}
        for index, row in continent.iterrows():
            self.zones[index] = Zone(row['name'], row['pop_est'], 0) # Just add the zone, no severity
        
        # Randomly choose one country as the camp
        self.set_camp(random.choice(list(self.zones.values())))

        # Randomly choose neighbors contries to be affected (where the disaster occured)
        affected_zones = random.sample(list(self.zones.values()), self.max_affected_zones)
        for zone in affected_zones:
            zone.set_severity(random.randint(1, 4)) # Random severity level

        # Randomly add edges between countries
        zone_keys = list(self.zones.keys()) # Get zone keys
        for i in range(len(zone_keys)):
            zone1 = self.zones[zone_keys[i]]
            neighbors_added = 0
            for j in range(i + 1, len(zone_keys)):
                zone2 = self.zones[zone_keys[j]]
                
                # Limit each zone to a fixed number of connections for better readability
                if neighbors_added >= self.max_edges_per_zone:
                    break
                
                # Randomly decide whether to add an edge
                if random.random() < 0.15: # 15% chance of connecting any two zones
                    travel_time = random.randint(30, 200)
                    fuel_cost = random.randint(5, 20)
                    good_conditions = random.choices([True, False], weights=[0.85, 0.15], k=1)[0] # Having good conditions is more likely
                    self.add_edge(zone1, zone2, travel_time, fuel_cost, good_conditions)
                    neighbors_added += 1