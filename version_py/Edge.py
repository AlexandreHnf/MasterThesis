class Edge:
    def __init__(self, extremity_node, travel_type, weight, length_km, speed):
        self.travel_type = travel_type
        self.extremity_node = extremity_node
        self.weight = weight
        self.length_km = length_km
        self.speed = speed

    def getTravelType(self):
        return self.travel_type

    def getWeight(self):
        return self.weight

    def setWeight(self, weight):
        self.weight = weight

    def getLengthKm(self):
        return self.length_km

    def getSpeed(self):
        return self.speed

    def getExtremityNode(self):
        return self.extremity_node

