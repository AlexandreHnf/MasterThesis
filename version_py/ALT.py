from heapq import heappush, heappop
from Astar import Astar
from ALTpreprocessing import ALTpreprocessing

class ALT(Astar):

    def __init__(self, graph, s, t, lm_selection, nb_lm, origin, priority="bin", bucket_size=40, heuristic=""):
        Astar.__init__(self, graph, s, t, priority, bucket_size, heuristic)

        self.landmark_selection = lm_selection  # (str) landmark selection strategy
        self.nb_landmarks = nb_lm
        self.origin = origin
        self.lm_dists = None  # distance from all nodes to all landmarks

    def preprocessing(self):
        p = ALTpreprocessing(self.graph)
        landmarks = []
        if self.landmark_selection == "farthest":
            landmarks = p.farthestLandmarkSelection(self.nb_landmarks, self.origin)
        elif self.landmark_selection == "planar":
            landmarks = p.planarLandmarkSelection(self.nb_landmarks, self.origin)
        elif self.landmark_selection == "random":
            landmarks = p.randomLandmarkSelection(self.nb_landmarks)
        landmarks = list(zip([p.findClosestNode(l) for l in landmarks], landmarks))
        self.lm_dists = p.getLandmarksDistances(landmarks)

        return landmarks  # temporaire

    def ALTHeuristic(self, ID1, ID2):
        max_dist = 0
        for dist1, dist2 in zip(self.lm_dists[ID1], self.lm_dists[ID2]):
            try:
                d = abs(dist1 - dist2)
                if d > max_dist:
                    max_dist = d
            except TypeError:
                pass  # some nodes couldn't reach a landmark
        # print(max_dist)
        return max_dist

    def findShortestPath(self):
        # s, t = self.findSourceDest(source, dest)
        # self.preprocessing()
        self.h = lambda v: self.ALTHeuristic(v, self.t)
        # here, for A*, we call dijkstra but heuristic will be used when
        # relaxing vertices

        exist_sol = self.dijkstra()
        if not exist_sol:
            return None
        return self.processSearchResult()
