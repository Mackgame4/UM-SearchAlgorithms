class Zone:
    def __init__(self, name, population=0, severity=0, ttl=0, permitted_vehicles={}):
        self.name = str(name)
        self.population = population
        self.severity = severity
        self.ttl = ttl # Time to live (janela de tempo critica)
        self.permitted_vehicles = permitted_vehicles # Dicionário de veículos que podem aceder a esta zona

    def is_vehicle_permitted(self, vehicle, good_conditions):
        vehicle_name = vehicle.get_tipo_name()
        # Verificar se as condições são hostis
        if not good_conditions:
            vehicles_allowed_in_hostile_conditions = {"Helicoptero", "Camiao", "Barco"}
            return vehicle_name in vehicles_allowed_in_hostile_conditions

        # Caso contrário, verificar a permissão padrão da zona
        return self.permitted_vehicles.get(vehicle_name, False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def set_name(self, name):
        self.name = name

    def set_population(self, population):
        self.population = population

    def set_severity(self, severity):
        self.severity = severity

    def get_name(self):
        return self.name

    def get_population(self):
        return self.population

    def get_severity(self):
        return self.severity

    def get_ttl(self):
        return self.ttl

    def set_ttl(self, ttl):
        self.ttl = ttl

    def get_permitted_vehicles(self):
        return self.permitted_vehicles

    def set_permitted_vehicles(self, permitted_vehicles):
        self.permitted_vehicles = permitted_vehicles

