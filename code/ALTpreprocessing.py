#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Copyright (c) 2013 Ryan Pon
# Licensed under the MIT license.
# => https://github.com/ryanpon/pathfinding-animator

# Modified by Alexandre Heneffe.

"""
Landmark computation on a graph network
    - planar landmarks selection
    - farthest landmarks selection
"""

import random
from heapq import heappush, heappop
from collections import defaultdict
from Utils import haversine, bearing
from Dijkstra import Dijkstra
from Astar import Astar

from Graph import Graph
import threading


class LandmarkDistThread(threading.Thread):
    def __init__(self, threadID, graph, landmark, lm_est):
        threading.Thread.__init__(self)

        self.threadID = threadID
        self.graph = Graph(graph.getNodesCoords(), graph.getReverseGraph())
        self.landmark = landmark

        self.lm_est = lm_est
        self.lm_dists = {}

    def run(self):
        dijkstra = Dijkstra(self.graph, self.landmark, -1)
        dists = dijkstra.getDistsSourceToNodes()
        # print("thread {0} : {1}".format(self.threadID, len(dists)))

        for i, pid in enumerate(self.graph.getNodesCoords()):
            self.lm_dists[pid] = dists[pid]


class ALTpreprocessing:
    """
    Class that contains functions to find landmarks in a graph network
    """

    def __init__(self, graph, lm_selection, origin, nb_lm):
        self.graph = graph
        self.origin = origin
        self.nb_landmarks = nb_lm
        self.landmark_selection = lm_selection
        self.landmarks = []

    def getLmDistances(self):
        if self.landmark_selection == "farthest":
            self.landmarks = self.farthestLandmarkSelection(self.nb_landmarks, self.origin)
        elif self.landmark_selection == "planar":
            self.landmarks = self.planarLandmarkSelection(self.nb_landmarks, self.origin)
        elif self.landmark_selection == "random":
            self.landmarks = self.randomLandmarkSelection(self.nb_landmarks)
        self.landmarks = list(zip([self.findClosestNode(l) for l in self.landmarks], self.landmarks))
        return self.getLandmarksDistances(self.landmarks)

    def getLandmarks(self):
        return self.landmarks

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
        best_vertex = None  # if no corresponding vertex
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
            for pid, coord in self.graph.getNodesCoords().items():
                lm_est[lm_id][pid] = haversine(x, y, coord[0], coord[1])

        # compute all distances from each node to every landmark
        lm_dists = defaultdict(list)

        threads = []
        # create new threads
        for i, landmark in enumerate(landmarks):
            my_thread = LandmarkDistThread(i + 1, self.graph, landmark[0], lm_est)
            my_thread.start()
            threads.append(my_thread)

        # synchronize
        for i, landmark in enumerate(landmarks):
            threads[i].join()

        for pid in self.graph.getNodesCoords():
            for i, landmark in enumerate(landmarks):
                lm_dists[pid].append(threads[i].lm_dists[pid])

        return lm_dists

    def divideInRegions(self, k, origin):
        regions = [[] for _ in range(k)]
        region_size = 360.0 / k  # angle
        for pid, coord in self.graph.getNodesCoords().items():
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
        origin = self.graph.getNodesCoords()[origin_id]
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
            if best_candidate:
                landmarks.append(best_candidate)
        return landmarks

    def farthestLandmarkSelection(self, k, origin):
        """
        Select the set of k vertices so that the minimum distance between a pair of selected
        vertices is maximized.
        """
        if not origin:
            origin = self.graph.getQtree().getOrigin()
        landmarks = [self.graph.getNodesCoords()[self.findClosestNode(origin)]]
        for _ in range(k):
            max_dist = float("-inf")
            best_candidate = None
            for pid, coord in self.graph.getNodesCoords().items():
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
            candidate = random.choice(list(self.graph.getNodesCoords().keys()))
            while self.graph.getNodesCoords()[candidate] in landmarks:
                candidate = random.choice(list(self.graph.getNodesCoords().keys()))
            landmarks.append(self.graph.getNodesCoords()[candidate])  # coord

        return landmarks
