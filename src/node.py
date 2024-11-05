class Node:
    def __init__(self, name, id=-1):
        self.id = id
        self.name = str(name)
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def set_id(self, id):
        self.id = id
    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __hash__(self):
        return hash(self.name)