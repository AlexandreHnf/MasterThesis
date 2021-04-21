from bidirectionalDijkstra import BidirectionalDijkstra

class BidirectionalAstar(BidirectionalDijkstra):

    def __init__(self, graph, rev_graph, nodes, s, t, priority="bin", bucket_size=40, heuristic=""):
        BidirectionalDijkstra.__init__(self, graph, rev_graph, nodes, s, t, priority, bucket_size)

        self.heuristic = heuristic # string : euclidean, manhattan, octile
        # heuristic function, by default, euclidean distance (haversine)
        self.h_fun = self.heuristicSelector(heuristic)
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
        self.h = lambda v, w: self.h_fun(v, w)
        # here, for A*, we call dijkstra but heuristic will be used when
        # relaxing vertices /!\ bidirectional, so we must specify v and w
        # instead of w being simply destination node t

        exist_sol = self.bidiDijkstra()
        if not exist_sol:
            return None

        print("midpoint : ", self.midpoint)
        return self.processSearchResult()

    def relaxVertexForward(self, v, closed_set, unvisited_set):
        """
        FORWARD
        # v = the current vertex
        Relax all arcs coming from vertex v
        """
        for arc in self.graph[v]:
            neighbour = arc.getExtremityNode()
            # self.nb_relax_edges += 1
            if neighbour in closed_set:
                continue
            new_dist = self.fwd_pred[v]["dist"] + arc.getWeight()
            if neighbour not in self.fwd_pred or new_dist < self.fwd_pred[neighbour]["dist"]:
                self.fwd_pred[neighbour] = {"pred": v, "dist": new_dist}
                # what changes from regular Dijkstra : heuristic estimation
                estimation = new_dist + self.h(neighbour, self.t)
                self.pushPriorityQueue(unvisited_set, (estimation, neighbour))

    def relaxVertexBackward(self, v, closed_set, unvisited_set):
        """
        BACKWARD
        # v = the current vertex
        Relax all arcs coming from vertex v
        """
        for arc in self.rev_graph[v]:  # REVERSE GRAPH
            neighbour = arc.getExtremityNode()
            # self.nb_relax_edges += 1
            if neighbour in closed_set:
                continue
            new_dist = self.bwd_pred[v]["dist"] + arc.getWeight()
            if neighbour not in self.bwd_pred or new_dist < self.bwd_pred[neighbour]["dist"]:
                self.bwd_pred[neighbour] = {"pred": v, "dist": new_dist}
                # what changes from regular Dijkstra : heuristic estimation
                estimation = new_dist + self.h(neighbour, self.s)
                self.pushPriorityQueue(unvisited_set, (estimation, neighbour))