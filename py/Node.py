class Node:
    def __init__(self, ID, lat, lon):
        self.ID = ID
        self.lat = lat
        self.lon = lon 
        self.previous = None # of type Node 
        self.dist_from_start = 0
        self.marked = False 
        self.adjacents = []

    def setDistFromStart(self, d):
        self.dist_from_start = d
    
    def addAdjacentNode(self, v):
        if (v not in self.adjacents):
            self.adjacents.append(v)
    
    def setPrevious(self, p):
        self.previous = p 

    def getPrevious(self):
        return self.previous 

    def getID(self):
        return self.ID 

    def getLatitude(self):
        return self.lat 

    def getLongitude(self):
        return self.lon 

    def getDistFromStart(self):
        return self.dist_from_start

    def mark(self, m):
        self.marked = m

    def getMark(self):
        return self.marked
    
    def getAdjacentNode(self, i):
        return self.adjacents[i]

    def getNbAdjacents(self):
        return len(self.adjacents)

    def show(self):
        print("node {0}, marked = {1}".format(self.ID, self.marked))

    def __repr__(self):
        a = [node.getID() for node in self.adjacents]
        return "Node {0}, adj : {1}, marked : {2})".format(self.ID, a, self.marked)