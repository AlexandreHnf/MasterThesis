#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Astar import Astar
from ALTpreprocessing import ALTpreprocessing


class ALT(Astar):

    def __init__(self, graph, s, t, lm_dists, priority="bin", bucket_size=40, heuristic=""):
        Astar.__init__(self, graph, s, t, priority, bucket_size, heuristic)

        self.lm_dists = lm_dists  # distance from all nodes to all landmarks

        self.h = lambda v: self.ALTHeuristic(v, self.t)

    def ALTHeuristic(self, ID1, ID2):
        max_dist = 0
        for dist1, dist2 in zip(self.lm_dists[ID1], self.lm_dists[ID2]):
            try:
                d = abs(dist1 - dist2)
                if d > max_dist:
                    max_dist = d
            except TypeError:
                pass  # some nodes couldn't reach a landmark
        return max_dist

    def findShortestPath(self):
        # s, t = self.findSourceDest(source, dest)
        # self.preprocessing()
        self.h = lambda v: self.ALTHeuristic(v, self.t)
        # here, for A*, we call dijkstra but heuristic will be used when
        # relaxing vertices

        exist_sol = self.run()
        if not exist_sol:
            return None
        return self.processSearchResult()

    def getAvgMaxHeuristicDist(self):
        avg_max_dist = 0
        for v in self.graph.getNodesIDs():
            max_dist = self.ALTHeuristic(v, self.t)
            avg_max_dist += max_dist

        return avg_max_dist / self.graph.getNbNodes()


