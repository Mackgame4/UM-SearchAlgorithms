class Vehicle:
    def __init__(self, name: str, capacity: int=0, range: int=0, speed: int=1):
        """
        Representa um veículo.
        :param name: Nome ou tipo do veículo
        :param capacity: Capacidade máxima do veículo em kg
        :param range: Autonomia do veículo em quilômetros
        :param speed: Velocidade do veículo em km/h
        """
        self.name = name
        self.capacity = capacity
        self.range = range
        self.speed = speed

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def __eq__(self, other: "Vehicle"):
        return self.name == other.name
   
    def __hash__(self):
        return hash(self.name)
    
    """ Getters """
    def get_name(self) -> str:
        return self.name
    
    def get_capacity(self) -> int:
        return self.capacity
    
    def get_range(self) -> int:
        return self.range
    
    def get_speed(self) -> int:
        return self.speed
    
    """ Setters """
    def set_name(self, name):
        self.name = name

    def set_capacity(self, capacity):
        self.capacity = capacity

    def set_range(self, range):
        self.range = range

    def set_speed(self, speed):
        self.speed = speed

VEHICLE_TYPES: dict[int, Vehicle] = {
    0: Vehicle("Carro", 300, 400, 120),
    1: Vehicle("Moto", 100, 200, 80),
    2: Vehicle("Camião", 1000, 49, 80),
    3: Vehicle("Helicóptero", 500, 600, 200),
    4: Vehicle("Drone", 600, 1000, 200)
}

def get_fastest_capable_vehicle(capacity: int) -> Vehicle:
    # get the fastest vehicle that can carry the given capacity
    vehicleList = list(VEHICLE_TYPES.values())
    vehicleList.sort(key=lambda x: x.get_speed(), reverse=True)
    for vehicle in vehicleList:
        if vehicle.get_capacity() >= capacity:
            return vehicle
    return None

class VehicleType:
    def __init__(self, type: int=0):
        """
        Representa um tipo de veículo.
        :param type: Tipo de veículo
        """
        self.types = VEHICLE_TYPES
        self.type = type
        
    def __str__(self):
        return self.types[self.type].get_name()
    
    def __repr__(self):
        return self.types[self.type].get_name()
    
    def __eq__(self, other: "VehicleType"):
        return self.types[self.type] == other.types[self.type]
    
    def __hash__(self):
        return hash(self.types[self.type])
    
    """ Getters """
    def get_type(self) -> int:
        return self.type

    def get_vehicle(self) -> Vehicle:
        return self.types[self.type]
    
    def get_vehicle_types(self) -> dict[int, Vehicle]:
        return self.types
    
    def get_possible_vehicles(self) -> list[Vehicle]:
        return self.types.values()

    """ Setters """
    def set_type(self, type):
        self.type = type

    def set_vehicle(self, vehicle):
        self.types[self.type] = vehicle

    def set_vehicle_types(self, types):
        self.types = types

    def set_possible_vehicles(self, vehicles):
        self.types = vehicles