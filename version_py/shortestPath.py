from heapq import heappush, heappop
from utils import haversine
from graphUtils import GraphUtil

class ShortestPath(object):

    def __init__(self, graph, nodes, bucket_size=40):
        self.graph = graph
        self.nodes_coords = nodes
        self.util = GraphUtil(nodes, bucket_size)

    def findSourceDest(self, source, dest):
        s = self.util.findClosestNode(self.nodes_coords[source])
        t = self.util.findClosestNode(self.nodes_coords[dest])
        return s, t

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

    def processSearchResult(self, search_space, pred, source, dest):
        if search_space == {} and pred == []:
            return None
        search_space_coords = self.getSearchSpaceCoords(search_space)
        shortest_path = self.constructShortestPath(pred, source, dest)
        return search_space_coords, shortest_path

    def getSearchSpaceCoords(self, search_space):
        """
        get a dictionary of all the nodes in the search space of the
        algorithm with geometric coordinates
        """
        needed = {}
        coords = self.util.coords
        for vertex, neighbours in search_space:
            needed[vertex] = coords[vertex]
            for arc in neighbours:
                needed[arc] = coords[arc]
        return needed

    def findShortestPath(self, source, dest):
        """
        Implemented by inherited objects
        """
        pass

    def constructShortestPath(self, pred, source, dest):
        """
        Given a pred (predecessor) list created by the shortest path algorithm, and the
        destination node's ID, returns the shortest path containing all these
        nodes. => will give the actual shortest path computed by the algorithm.
        """
        sp = []
        v = dest
        while pred[v]["pred"]:  # is not None
            sp.append(v)
            v = pred[v]["pred"]
        sp.append(source)
        sp.reverse()  # to have the path from source to dest and not t to s
        return {v: self.util.coords[v] for v in sp}

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