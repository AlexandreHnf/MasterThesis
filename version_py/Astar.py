from heapq import heappush, heappop
from Dijkstra import Dijkstra

class Astar(Dijkstra):

    def __init__(self, graph, nodes, priority="bin", bucket_size=40, heuristic=""):
        Dijkstra.__init__(self, graph, nodes, priority, bucket_size)
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

    def findShortestPath(self, s, t):
        # s, t = self.findSourceDest(source, dest)
        self.h = lambda v: self.h_fun(v, t)
        # here, for A*, we call dijkstra but heuristic will be used when
        # relaxing vertices
        search_space, pred = self.dijkstra(s, t)
        return self.processSearchResult(search_space, pred, s, t)

    def relaxVertex(self, v, t, pred, unvisited, closed_set):
        """
        # v = the current vertex, t = destination node
        Relax all arcs coming from vertex v
        """
        for neighbour, arc_weight in self.graph[v]:
            # print("neighbour : ", neighbour)
            if neighbour in closed_set:
                continue
            new_dist = pred[v]["dist"] + arc_weight
            # print("=> new dist : ", new_dist)
            # print("=> pre dist : ", pred.get(neighbour, None))
            if neighbour not in pred or new_dist < pred[neighbour]["dist"]:
                # if neighbour not in pred:
                    # print("v has been here")
                pred[neighbour] = {"pred": v, "dist": new_dist}
                estimation = new_dist + self.h(neighbour)  # heuristic estimation
                # heappush(unvisited, (estimation, neighbour) )
                self.pushPriorityQueue(unvisited, (estimation, neighbour))