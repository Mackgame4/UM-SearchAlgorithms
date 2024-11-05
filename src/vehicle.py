class Vehicle:
    def __init__(self, tipo=3, carga_max=0, velocidade=0, autonomia=0):
        self.carga_max = carga_max # capacidade de carga
        self.carga_atual = 0
        self.velocidade = velocidade # tempos de viagem
        self.autonomia = autonomia # distancia maxima
        self.tipos = {
            0: "Drone",
            1: "Helicoptero",
            2: "Caminhao",
            3: "Carro",
            4: "Moto",
            5: "Barco"
        }
        self.tipo = tipo
    
    def __str__(self):
        return f"{self.tipos[self.tipo]}"
    
    def __repr__(self):
        return f"{self.tipos[self.tipo]}"
    
    def __eq__(self, other):
        return self.tipo == other.tipo
    
    def __hash__(self):
        return hash(self.tipo)
    
    def get_tipo(self):
        return self.tipo
    
    def get_carga_max(self):
        return self.carga_max
    
    def get_carga_atual(self):
        return self.carga_atual
    
    def get_velocidade(self):
        return self.velocidade
    
    def get_autonomia(self):
        return self.autonomia
    
    def set_carga_max(self, carga_max):
        self.carga_max = carga_max

    def set_carga_atual(self, carga_atual):
        self.carga_atual = carga_atual

    def set_velocidade(self, velocidade):
        self.velocidade = velocidade

    def set_autonomia(self, autonomia):
        self.autonomia = autonomia

    def set_tipo(self, tipo):
        self.tipo = tipo

    def get_tipos(self):
        return self.tipos