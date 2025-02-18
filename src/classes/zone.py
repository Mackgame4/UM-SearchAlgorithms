class Zone:
    def __init__(self, name: str, population: int=0, severity: int=0, ttl: int=0, camp: bool=False):
        """
        Representa uma zona.
        :param name: Nome da zona.
        :param population: População da zona.
        :param severity: Severidade da zona.
        :param ttl: Tempo de vida da zona (janela de tempo critica).
        :param camp: Zona de acampamento.
        """
        self.name = str(name) # Ensure name is a string
        self.population = population
        self.severity = severity
        self.ttl = ttl # Time to live (janela de tempo critica)
        self.camp = camp

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other: "Zone"):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    """ Getters """
    def get_name(self) -> str:
        return self.name
    
    def get_population(self) -> int:
        return self.population
    
    def get_severity(self) -> int:
        return self.severity
    
    def get_ttl(self) -> int:
        return self.ttl
    
    def is_camp(self) -> bool:
        return self.camp
    
    """ Setters """
    def set_name(self, name):
        self.name = name

    def set_population(self, population):
        self.population = population

    def set_severity(self, severity):
        self.severity = severity

    def set_ttl(self, ttl):
        self.ttl = ttl

    def set_camp(self, camp):
        self.camp = camp