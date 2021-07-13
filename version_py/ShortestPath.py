class ShortestPath(object):

    def __init__(self, graph, s, t, bucket_size=40):
        self.graph = graph
        self.s = s
        self.t = t

    def setSource(self, s):
        self.s = s

    def setDest(self, t):
        self.t = t

    def getPathLength(self, path):
        """
        Get the total length of the path in km (from first node of the path
        to the last one)
        """
        path_nodes = path
        # print(path_nodes)
        total_length = 0  # km
        for i in range(len(path_nodes)-1):
            next_edge = None
            for edge in self.graph.getAdj(path_nodes[i]):
                if edge.getExtremityNode() == path_nodes[i+1]:
                    next_edge = edge
            if next_edge is None:  # it means the path is invalid
                return None
            total_length += next_edge.getWeight()
            print(next_edge.getTravelType(), end=" ")
        return total_length

    def getPathTravelTypes(self, path):
        travel_types = {}
        path_nodes = path
        for i in range(len(path_nodes)-1):
            next_edge = None
            for edge in self.graph.getAdj(path_nodes[i]):
                if edge.getExtremityNode() == path_nodes[i+1]:
                    next_edge = edge
            if next_edge is None:  # it means the path is invalid
                return None
            travel_type = next_edge.getTravelType()
            if travel_type in travel_types:
                travel_types[travel_type] += 1
            else:
                travel_types[travel_type] = 1

        return travel_types

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

