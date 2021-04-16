from heapq import heappush, heappop
from utils import haversine
from graphUtils import GraphUtil

class ShortestPath(object):

    def __init__(self, graph, nodes_coords):
        self.graph = graph
        self.nodes_coords = nodes_coords
        self.util = GraphUtil(nodes_coords)

    def findSourceDest(self, source, dest):
        s = self.util.findClosestNode(self.nodes_coords[source])
        t = self.util.findClosestNode(self.nodes_coords[dest])
        return s, t

    def processSearchResult(self, path, pred, dest):
        if path == {} and pred == []:
            return None
        path_coords = self.getPathCoords(path)
        shortest_path = self.constructShortestPath(pred, dest)
        return path, path_coords, shortest_path

    def getPathCoords(self, path):
        """
        get a dictionary of all the nodes in the shortest path found
        along with their coordinates
        """
        needed = {}
        coords = self.util.coords
        for vertex, neighbours in path:
            needed[vertex] = coords[vertex]
            for arc in neighbours:
                needed[arc] = coords[arc]
        return needed

    def findShortestPath(self, source, dest):
        """
        Implemented by inherited objects
        """
        pass

    def constructShortestPath(self, pred, dest):
        """
        Given a pred (predecessor) list created by the shortest path algorithm, and the
        destination node's ID, returns the shortest path containing all these
        nodes. => will give the actual shortest path computed by the algorithm.
        """
        path = []
        v = dest
        while pred[v]["pred"]:  # is not None
            path.append(v)
            v = pred[v]["pred"]
        path.reverse()  # to have the path from source to dest and not t to s
        return [self.util.coords[v] for v in path]

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