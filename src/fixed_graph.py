from zone import Zone
from graph import Graph
from vehicle import Vehicle

# FixedGraph extends graph and creates a fixed graph with fixed zones and edges (defined manually)
class FixedGraph(Graph): # Inherit from Graph
    def __init__(self):
        super().__init__() # Initialize the parent Graph class
        self.example_graph() # Set up the example graph

    def example_graph(self):
        # Create nodes
        self.zones = {
            0: Zone("Botswana", 100, 2, 700, {Vehicle(3), Vehicle(2), Vehicle(1), Vehicle(0)}), # Most affected zone
            1: Zone("Namibia", 400, 1, 400, {Vehicle(3), Vehicle(2), Vehicle(0)}), # Affected zone
            2: Zone("Zimbabwe", 300, 0, 600, {Vehicle(3), Vehicle(2), Vehicle(1)}),
            3: Zone("Angola", 400, 0, 500, {Vehicle(3), Vehicle(2), Vehicle(0)}),
            4: Zone("Zambia", 500, 0, 800, {Vehicle(3), Vehicle(2)}),
            5: Zone("Tanzania", 600, 0, 900, {Vehicle(3), Vehicle(5)}),
            6: Zone("Malawi", 700, 0, 1000, {Vehicle(3), Vehicle(4)})
        }
        self.set_camp(self.zones[5]) # ONU base
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