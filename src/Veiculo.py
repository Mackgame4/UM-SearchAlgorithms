class Veiculo:
    def __init__(self):
        self.carga_max = 0 # capacidade de carga?
        self.carga_atual = 0
        self.velocidade = 0 # tempos de viagem?
        self.autonomia = 0 # distancia maxima?
        self.tipo = {
            0: "Drone",
            1: "Helicoptero",
            2: "Barco",
            3: "Caminhao",
            4: "Carro",
            5: "Moto"
        }

    """
    def __str__(self):
        out = ""
        for key in self.m_graph.keys():
            out = out + "node" + str(key) + ": " + str(self.m_graph[key]) + "\n"
            return out
    """