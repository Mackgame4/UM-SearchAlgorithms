class Zone:
    def __init__(self, name, population=0, severity=0):
        self.name = str(name)
        self.population = population
        self.severity = severity

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