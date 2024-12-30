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
    def get_name(self):
        return self.name
    
    def get_capacity(self):
        return self.capacity
    
    def get_range(self):
        return self.range
    
    def get_speed(self):
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

class VehicleType:
    def __init__(self, type=0):
        """
        Representa um tipo de veículo.
        :param type: Tipo de veículo
        """
        self.types = {
            0: Vehicle("Carro", 300, 400, 120),
            1: Vehicle("Moto", 100, 200, 80),
            2: Vehicle("Caminhão", 1000, 800, 80),
            3: Vehicle("Helicoptero", 500, 600, 200),
            4: Vehicle("Drone", 100, 1000, 200)
        }
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
    def get_type(self):
        return self.type

    def get_vehicle(self):
        return self.types[self.type]
    
    def get_vehicle_types(self):
        return self.types
    
    """ Setters """
    def set_type(self, type):
        self.type = type

    def set_vehicle(self, vehicle):
        self.types[self.type] = vehicle

    def set_vehicle_types(self, types):
        self.types = types