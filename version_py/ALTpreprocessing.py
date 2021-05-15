# Copyright (c) 2013 Ryan Pon
# Licensed under the MIT license.
# => https://github.com/ryanpon/pathfinding-animator

# Modified by Alexandre Heneffe.

"""
Landmark computation on a graph network
    - planar landmarks selection
    - farthest landmarks selection
"""

import json
import random
from heapq import heappush, heappop
from collections import defaultdict
from utils import haversine, bearing
from Dijkstra import Dijkstra
from Astar import Astar

class ALTpreprocessing:
    """
    Class that contains functions to find landmarks in a graph network
    """

    def __init__(self, graph):
        self.graph = graph

    def findClosestNode(self, target, rng=.01):
        """
        Given geographic coordinates, find the closest node in the graph corresponding
        to that coordinates using the quadtree query_range function.
        rng = search range size

        Arguments:
        target -- (x, y) point to be matched to the graph.

        Returns:
        The ID of the vertex that is closest to the given point in the graph.
        """
        x, y = target
        close_vertices = self.graph.getQtree().query_range(x - rng, x + rng, y - rng, y + rng)
        best_vertex = None # if no corresponding vertex
        best_dist = float("inf")
        for point, vertices in close_vertices.items():
            dist = haversine(point[0], point[1], target[0], target[1])
            if dist < best_dist:
                best_dist = dist
                best_vertex = vertices[0]
        if best_vertex:
            return best_vertex
        else:
            return None

    def existShortestPath(self, s, t):
        """
        Check whether there exists a shortest path from s to t
        """
        d = Dijkstra(self.graph, s, t)
        return d.existShortestPath()

    def lmExactDist(self, v, landmark, lm_est):
        """
        => mini A* algorithm to compute shortest path between a node v and a landmark
        Speedup by using precomputed euclidean distances between nodes and landmarks
        """
        lm_dists = lm_est[landmark]
        pred = {v: 0}  # source = v
        closed_set = set()
        unseen = [(0, v)]
        while unseen:
            _, w = heappop(unseen)
            if w in closed_set:
                continue
            elif w == landmark:
                return pred[w]
            closed_set.add(w)
            for arc in self.graph.getAdj(w):
                neighbour = arc.getExtremityNode()
                if neighbour not in closed_set:
                    new_dist = (pred[w] + arc.getWeight())
                    if neighbour not in pred or new_dist < pred[neighbour]:
                        pred[neighbour] = new_dist
                        est = new_dist + lm_dists[neighbour]
                        heappush(unseen, (new_dist + est, neighbour))
        return None # if no vvalid path found

    def getLandmarksDistances(self, landmarks):
        """
        compute the shortest path from all nodes in the graph to all landmarks using
        A* => heuristic = euclidean distance between node and landmark
        """
        # landmark heuristic estimation (speedup)
        lm_est = {}
        for lm_id, lm_coord in landmarks:
            lm_est[lm_id] = {}
            x, y = lm_coord
            for pid, coord in self.graph.getNodes().items():
                lm_est[lm_id][pid] = haversine(x, y, coord[0], coord[1])

        # compute all distances from each node to every landmark
        lm_dists = defaultdict(list)
        for i, pid in enumerate(self.graph.getNodes()):
            for landmark, _ in landmarks:
                try:
                    d = self.lmExactDist(pid, landmark, lm_est)
                except KeyError:
                    d = None
                lm_dists[pid].append(d)

        return lm_dists

    def divideInRegions(self, k, origin):
        regions = [[] for _ in range(k)]
        region_size = 360.0 / k # angle
        for pid, coord in self.graph.getNodes().items():
            b = bearing(origin[0], origin[1], coord[0], coord[1], True)
            s = int(b / region_size)
            regions[s].append((pid, coord))
        return regions

    def planarLandmarkSelection(self, k, origin):
        """
        Find k landmarks using the "planar landmark selection" method :
        divide the graph plane in k regions and for each region based on a central
        point, find a landmark that is the farthest from center in each region
        """
        if not origin:
            origin = self.graph.getQtree().getOrigin()
        origin_id = self.findClosestNode(origin)
        origin = self.graph.getNodes()[origin_id]
        regions = self.divideInRegions(k, origin)
        landmarks = []
        for region in regions:
            max_dist = float("-inf")
            best_candidate = None
            for pid, coord in region:
                cur_dist = haversine(origin[0], origin[1], coord[0], coord[1])
                if cur_dist > max_dist and self.existShortestPath(pid, origin_id):
                    max_dist = cur_dist
                    best_candidate = coord
            landmarks.append(best_candidate)
        return landmarks

    def farthestLandmarkSelection(self, k, origin):
        """
        Select the set of k vertices so that the minimum distance between a pair of selected
        vertices is maximized.
        """
        if not origin:
            origin = self.graph.getQtree().getOrigin()
        landmarks = [self.graph.getNodes()[self.findClosestNode(origin)]]
        print(landmarks)
        for _ in range(k):
            max_dist = float("-inf")
            best_candidate = None
            for pid, coord in self.graph.getNodes().items():
                cur_dist = 0
                for lm in landmarks:
                    cur_dist += haversine(lm[0], lm[1], coord[0], coord[1])
                if cur_dist > max_dist and not coord in landmarks:
                    max_dist = cur_dist
                    best_candidate = coord
            landmarks.append(best_candidate)
            if len(landmarks) > k:
                landmarks.pop(0)
        return landmarks

    def randomLandmarkSelection(self, k):
        """
        Pick k landmarks randomly
        """
        landmarks = []
        for _ in range(k):
            candidate = random.choice(list(self.graph.getNodes().keys()))
            while self.graph.getNodes()[candidate] in landmarks:
                candidate = random.choice(list(self.graph.getNodes().keys()))
            landmarks.append(self.graph.getNodes()[candidate])  # coord

        return landmarks