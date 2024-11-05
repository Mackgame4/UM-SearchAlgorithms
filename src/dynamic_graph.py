from zone import Zone
from graph import Graph
import random
import geopandas as gpd

# DynamicGraph extends graph and creates a random graph with random zones and edges
class DynamicGraph(Graph):
    def __init__(self):
        super().__init__()
        self.create_random_graph()

    def create_random_graph(self):
        # Load all African countries
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        africa = world[world['continent'] == 'Africa']
        
        # Initialize zones with each African country
        self.zones = {}
        for index, row in africa.iterrows():
            self.zones[index] = Zone(row['name'], random.randint(100, 1000), random.randint(0, 2))
        
        # Randomly choose one country as the camp
        self.set_camp(random.choice(list(self.zones.values())))

        # Randomly add edges between countries
        zone_keys = list(self.zones.keys())  # Get all keys in the zones dictionary
        max_edges_per_zone = 3  # Limit the number of edges per zone to avoid a fully connected graph
        
        for i in range(len(zone_keys)):
            zone1 = self.zones[zone_keys[i]]
            neighbors_added = 0
            for j in range(i + 1, len(zone_keys)):
                zone2 = self.zones[zone_keys[j]]
                
                # Limit each zone to a fixed number of connections for better readability
                if neighbors_added >= max_edges_per_zone:
                    break
                
                # Randomly decide whether to add an edge
                if random.random() < 0.15:  # 15% chance of connecting any two zones
                    travel_time = random.randint(50, 500)
                    fuel_cost = random.randint(5, 20)
                    good_conditions = random.choice([True, False])
                    self.add_edge(zone1, zone2, travel_time, fuel_cost, good_conditions)
                    neighbors_added += 1