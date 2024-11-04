class Zona:
    def __init__(self):
        self.populacao = 0
        self.gravidade = 0 # prioridade?
        self.cond_metereologicas = 0 # acessibilidade?
        self.cond_geograficas = 0 # acessibilidade?

    """
    def __str__(self):
        out = ""
        for key in self.m_graph.keys():
            out = out + "node" + str(key) + ": " + str(self.m_graph[key]) + "\n"
            return out
    """