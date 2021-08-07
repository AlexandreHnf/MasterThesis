#!/usr/bin/env python
# -*- coding: utf-8 -*-


from BidirectionalDijkstra import BidirectionalDijkstra


class BidirectionalAstar(BidirectionalDijkstra):

    def __init__(self, graph, s, t, priority="bin", bucket_size=40, heuristic=""):
        BidirectionalDijkstra.__init__(self, graph, s, t, priority, bucket_size)

        self.heuristic = heuristic # string : euclidean, manhattan, octile
        # heuristic function, by default, euclidean distance (haversine)
        self.h_fun = self.heuristicSelector(heuristic)
        # function that, given a node, gives the heuristic value with h_fun
        # here, for A*, we call dijkstra but heuristic will be used when
        # relaxing vertices /!\ bidirectional, so we must specify v and w
        # instead of w being simply destination node t
        self.h = lambda v, w: self.h_fun(v, w)

    def heuristicSelector(self, heuristic):
        h_fun = self.graph.euclidean
        if heuristic == "manhattan":
            h_fun = self.graph.manhattan
        elif heuristic == "octile":
            h_fun = self.graph.octile
        return h_fun

    def findShortestPath(self):
        self.h = lambda v, w: self.h_fun(v, w)
        # here, for A*, we call dijkstra but heuristic will be used when
        # relaxing vertices /!\ bidirectional, so we must specify v and w
        # instead of w being simply destination node t

        exist_sol = self.run()
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
        for arc in self.graph.getAdj(v):
            neighbour = arc.getExtremityNode()
            if neighbour in closed_set:
                continue
            self.nb_relax_edges += 1
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
        for arc in self.graph.getRevAdj(v):  # REVERSE GRAPH
            neighbour = arc.getExtremityNode()
            if neighbour in closed_set:
                continue
            self.nb_relax_edges += 1
            new_dist = self.bwd_pred[v]["dist"] + arc.getWeight()
            if neighbour not in self.bwd_pred or new_dist < self.bwd_pred[neighbour]["dist"]:
                self.bwd_pred[neighbour] = {"pred": v, "dist": new_dist}
                # what changes from regular Dijkstra : heuristic estimation
                estimation = new_dist + self.h(neighbour, self.s)
                self.pushPriorityQueue(unvisited_set, (estimation, neighbour))