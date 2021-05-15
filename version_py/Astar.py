from heapq import heappush, heappop
from Dijkstra import Dijkstra

class Astar(Dijkstra):

    def __init__(self, graph, s, t, priority="bin", bucket_size=40, heuristic=""):
        Dijkstra.__init__(self, graph, s, t, priority, bucket_size)
        self.heuristic = heuristic  # string : euclidean, manhattan, octile
        # heuristic function, by default, euclidean distance (haversine)
        self.h_fun = self.heuristicSelector(heuristic)
        # function that, given a node, gives the heuristic value with h_fun
        self.h = None

    def heuristicSelector(self, heuristic):
        h_fun = self.graph._euclidean
        if heuristic == "manhattan":
            h_fun = self.graph._manhattan
        elif heuristic == "octile":
            h_fun = self.graph._octile
        return h_fun

    def findShortestPath(self):
        self.h = lambda v: self.h_fun(v, self.t)
        # here, for A*, we call dijkstra but heuristic will be used when
        # relaxing vertices

        exist_sol = self.dijkstra()
        if not exist_sol:
            return None
        return self.processSearchResult()

    def relaxVertex(self, v):
        """
        # v = the current vertex, t = destination node
        Relax all arcs coming from vertex v
        """
        for arc in self.graph.getAdj(v):
            neighbour = arc.getExtremityNode()
            if neighbour in self.closed_set:
                continue
            self.nb_relax_edges += 1
            new_dist = self.dists_so_far[v] + arc.getWeight()
            if neighbour not in self.preds or new_dist < self.dists_so_far[neighbour]:
                self.preds[neighbour] = v
                self.dists_so_far[neighbour] = new_dist
                estimation = new_dist + self.h(neighbour)  # heuristic estimation
                self.pushPriorityQueue( (estimation, neighbour))