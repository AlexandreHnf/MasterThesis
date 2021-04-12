from Node import *

class GraphDijkstra:

    def __init__(self):
        self.nb_nodes = 0
        self.nodes = {} #dic
        self.nb_edges = 0

    # def initNodes(self):
    #     self.nodes = [None for _ in range(self.nb_nodes)]

    def setNbEdges(self, nb_e):
        self.nb_edges = nb_e

    def createNode(self, ID, lat, lon):
        new_node = Node(ID, lat, lon)
        # self.nodes.append(new_node)
        self.nodes[ID] = new_node

    def getNbNodes(self):
        return len(self.nodes)

    def setNbNodes(self, nb_n):
        self.nb_nodes = nb_n

    def getNode(self, i):
        return self.nodes[i]

    def visited(self, i):
        self.nodes[i].mark(True)

    def showStats(self):
        print("- Nb nodes : ", len(self.nodes))
        print("- Nb edges : ", self.nb_edges)

    def show(self):
        print("Graph : ")
        for node in self.nodes:
            # print("Node {0}, adj : ".format(node.getID()))
            # for j in range(node.getNbAdjacents()):
            #     print(node.getAdjacentNode(j).getID(), end= ", ")
            # print()
            # print("marked ", node.getMark())
            print(nodes[node])