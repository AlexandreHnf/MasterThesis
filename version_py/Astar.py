from heapq import heappush, heappop
from Dijkstra import Dijkstra

class Astar(Dijkstra):

    def __init__(self, graph, nodes, s, t, priority="bin", bucket_size=40, heuristic=""):
        Dijkstra.__init__(self, graph, nodes, s, t, priority, bucket_size)
        self.heuristic = heuristic  # string : euclidean, manhattan, octile
        self.h_fun = self.heuristicSelector(heuristic)  # heuristic function, by default, euclidean distance (haversine)
        # function that, given a node, gives the heuristic value with h_fun
        self.h = None

    def heuristicSelector(self, heuristic):
        h_fun = self.util._euclidean
        if heuristic == "manhattan":
            h_fun = self.util._manhattan
        elif heuristic == "octile":
            h_fun = self.util._octile
        return h_fun

    def findShortestPath(self):
        # s, t = self.findSourceDest(source, dest)
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
        for arc in self.graph[v]:
            neighbour = arc.getExtremityNode()
            if neighbour in self.closed_set:
                continue
            new_dist = self.pred[v]["dist"] + arc.getWeight()
            if neighbour not in self.pred or new_dist < self.pred[neighbour]["dist"]:
                self.pred[neighbour] = {"pred": v, "dist": new_dist}
                estimation = new_dist + self.h(neighbour)  # heuristic estimation
                # heappush(unvisited, (estimation, neighbour) )
                self.pushPriorityQueue( (estimation, neighbour))