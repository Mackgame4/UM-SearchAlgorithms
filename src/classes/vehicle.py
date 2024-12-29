class Vehicle:
    def __init__(self, tipo=3):
        self.tipos = {
            0: "Drone",
            1: "Helicóptero",
            2: "Caminhão",
            3: "Carro",
            4: "Moto",
            5: "Barco"
        }
        self.tipo = tipo

        # Definindo os parâmetros padrão para cada tipo de veículo
        if tipo == 0:  # Drone
            self.carga_max = 5  # kg
            self.velocidade = 60  # km/h
            self.autonomia = 150  # km
            self.consumo = 0  # drones são elétricos, consumo não aplicável
        elif tipo == 1:  # Helicóptero
            self.carga_max = 1000  # kg
            self.velocidade = 250  # km/h
            self.autonomia = 600  # km
            self.consumo = 2  # litros/km
        elif tipo == 2:  # Caminhão
            self.carga_max = 20000  # kg
            self.velocidade = 80  # km/h
            self.autonomia = 1000  # km
            self.consumo = 0.8  # litros/km
        elif tipo == 3:  # Carro
            self.carga_max = 500  # kg
            self.velocidade = 120  # km/h
            self.autonomia = 700  # km
            self.consumo = 0.5  # litros/km
        elif tipo == 4:  # Moto
            self.carga_max = 50  # kg
            self.velocidade = 100  # km/h
            self.autonomia = 300  # km
            self.consumo = 0.2  # litros/km
        elif tipo == 5:  # Barco
            self.carga_max = 5000  # kg
            self.velocidade = 40  # km/h
            self.autonomia = 500  # km
            self.consumo = 1.5  # litros/km

        # Variável para armazenar a carga atual
        self.carga_atual = 0  # kg

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

    def get_tipo_name(self):
        return self.tipos[self.tipo]

    def get_carga_max(self):
        return self.carga_max

    def get_carga_atual(self):
        return self.carga_atual

    def get_velocidade(self):
        return self.velocidade

    def get_autonomia(self):
        return self.autonomia

    def get_consumo(self):
        return self.consumo

    def set_carga_atual(self, carga):
        """Define a carga atual a ser transportada."""
        if carga > self.carga_max:
            raise ValueError(f"A carga ({carga} kg) excede a capacidade máxima do veículo ({self.carga_max} kg).")
        self.carga_atual = carga
