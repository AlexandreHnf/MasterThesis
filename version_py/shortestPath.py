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


    def getPathLength(self, path):
        """
        Get the total length of the path in km (from first node of the path
        to the last one)
        """
        path_nodes = list(path.keys())
        total_length = 0  # km
        for i in range(len(path_nodes)-1):
            next_edge = None
            for edge in self.graph[path_nodes[i]]:
                if edge.getExtremityNode() == path_nodes[i+1]:
                    next_edge = edge
            if next_edge is None:  # it means the path is invalid
                return None
            total_length += next_edge.getWeight()
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

    def findShortestPath(self):
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