from GraphDijkstra import * 
from Node import * 
from Utils import * 
import sys

class Dijkstra:
    def __init__(self, s, t, G):
        self.s = s
        self.t = t 
        self.G = G 

    def adjacentRemainingNodes(self, node):
        remaining_adjacents = [] # list of nodes
        for i in range(node.getNbAdjacents()):
            if (not node.getAdjacentNode(i).getMark()):
                remaining_adjacents.append(node.getAdjacentNode(i))

        return remaining_adjacents

    def extractMinimum(self):
        size = self.G.getNbNodes()
        if (size == 0): return None 
        smallest_position = 0
        smallest = None
        for i in range(size):
            if (not self.G.getNode(i).getMark()):
                print(self.G.getNode(i))
                current = self.G.getNode(i)
                if (smallest == None or current.getDistFromStart() < smallest.getDistFromStart()):
                    print("smallest !")
                    smallest = current 
                    smallest_position = i 

        # self.G.getNode(smallest_position).mark(True)
        print("smallest: ", smallest)
        return smallest

    def distance(self, node1, node2):
        res = 0
        for i in range(node1.getNbAdjacents()):
            # if it is indeed its neighbour
            if (node2.getID() == node1.getAdjacentNode(i).getID()):
                res = distanceEarth(node1.getLatitude(), node1.getLongitude(), node2.getLatitude(), node2.getLongitude())
        return res 

    def printShortestRouteTo(self):
        previous = self.G.getNode(self.t)
        shortest_path = [] 
        # print("Distance from start : ", previous.getDistFromStart())
        dist_from_start = previous.getDistFromStart()
        while (previous != None):
            # print(previous.getID(), end=" ")
            shortest_path.insert(0, previous.getID())
            previous = previous.getPrevious()
        print("shortest path from {0} to {1} : {2} \n => dist = {3}".format(self.s, self.t, shortest_path, dist_from_start) )

    def runDijkstra(self):
        # INIT
        for i in range(self.G.getNbNodes()):
            self.G.getNode(i).setDistFromStart(sys.maxsize) # infinity
            self.G.getNode(i).mark(False)
            self.G.getNode(i).setPrevious(None)

        current = self.G.getNode(self.s)
        current.setDistFromStart(0)
        it = 0

        while (current.getID() != self.t):
            print("========== it = ", it)
            current.show()
            adjacent_nodes = self.adjacentRemainingNodes(current)
            print("nb adjacents : ", len(adjacent_nodes))

            for i in range(len(adjacent_nodes)):
                adjacent = adjacent_nodes[i]
                dist = self.distance(current, adjacent) + current.getDistFromStart()

                if (dist < adjacent.getDistFromStart()):
                    print("ok")
                    adjacent.setDistFromStart(dist)
                    adjacent.setPrevious(current)
                    print("node {0} : new dist : {1}".format(adjacent.getID(), dist))

            self.G.visited(current.getID()) # visited
            print(self.G.getNode(0).getMark(), current.getID())
            current = self.extractMinimum()
            it += 1
            if (it > 10) : break

        self.printShortestRouteTo() 

    