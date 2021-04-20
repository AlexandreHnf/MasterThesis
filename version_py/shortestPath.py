from heapq import heappush, heappop
from utils import haversine
from graphUtils import GraphUtil

class ShortestPath(object):

    def __init__(self, graph, nodes, s, t, bucket_size=40):
        self.graph = graph
        # self.nodes_coords = nodes
        self.util = GraphUtil(nodes, bucket_size)
        self.s = s
        self.t = t

    def isAdjacent(self, id2, id1_adjacents):
        for adj in id1_adjacents:
            if id2 == adj[0]:
                return True
        return False

    def isValidPath(self, path):
        ids = list(path.keys())
        for i in range(len(ids)-1):
            # print("{0}, {1} ({2})".format(ids[i], ids[i+1], self.graph[ids[i]]))
            if not self.isAdjacent(ids[i+1], self.graph[ids[i]]):
                return False
        return True

    def getPathLength(self, path):
        """
        Get the total length of the path in km (from first node of the path
        to the last one)
        """
        c = list(path.values()) # coordinates
        total_length = 0  # in km
        for i in range(1, len(c)):
            total_length += haversine(c[i][0], c[i][1], c[i-1][0], c[i-1][1])
        return total_length

    def processSearchResult(self):
        """
        Implemented by inherited objects
        """

    def getSearchSpaceCoords(self):
        """
        get a dictionary of all the nodes in the search space of the
        algorithm with geometric coordinates

        Implemented by inherited objects
        """

    def findShortestPath(self, source, dest):
        """
        Implemented by inherited objects
        """
        pass

    def getPriorityList(self):
        """
        Implemented by inherited objects
        """

    def constructShortestPath(self):
        """
        Given a pred (predecessor) list created by the shortest path algorithm, and the
        destination node's ID, returns the shortest path containing all these
        nodes. => will give the actual shortest path computed by the algorithm.

        implemented by inherited objects
        """