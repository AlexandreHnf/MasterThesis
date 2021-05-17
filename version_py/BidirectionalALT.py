from BidirectionalAstar import BidirectionalAstar
from ALTpreprocessing import ALTpreprocessing


class BidirectionalALT(BidirectionalAstar):

    def __init__(self, graph, s, t, lm_dists, priority="bin", bucket_size=40, heuristic=""):
        BidirectionalAstar.__init__(self, graph, s, t, priority, bucket_size, heuristic)

        self.lm_dists = lm_dists  # distance from all nodes to all landmarks

        self.h = lambda v, w: self.ALTHeuristic(v, w)

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
        self.h = lambda v, w: self.ALTHeuristic(v, w)
        # here, for A*, we call dijkstra but heuristic will be used when
        # relaxing vertices

        exist_sol = self.run()
        if not exist_sol:
            return None
        return self.processSearchResult()
