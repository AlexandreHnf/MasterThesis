class Edge:
    def __init__(self, extremity_node, weight):
        self.extremity_node = extremity_node
        self.weight = weight
        self.length_km = 0

    def getWeight(self):
        return self.weight

    def setWeight(self, weight):
        self.weight = weight

    def getExtremityNode(self):
        return self.extremity_node
