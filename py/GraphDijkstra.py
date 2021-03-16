from Node import *

class GraphDijkstra:

    def __init__(self):
        self.nodes = []

    def createNode(self, ID, lat, lon):
        new_node = Node(ID, lat, lon)
        self.nodes.append(new_node)

    def getNbNodes(self):
        return len(self.nodes)

    def getNode(self, i):
        return self.nodes[i]

    def visited(self, i):
        self.nodes[i].mark(True)

    def show(self):
        print("Graph : ")
        for node in self.nodes:
            # print("Node {0}, adj : ".format(node.getID()))
            # for j in range(node.getNbAdjacents()):
            #     print(node.getAdjacentNode(j).getID(), end= ", ")
            # print()
            # print("marked ", node.getMark())
            print(node)