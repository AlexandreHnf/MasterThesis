# Copyright (c) 2013 Ryan Pon
# Licensed under the MIT license.
# => https://github.com/ryanpon/pathfinding-animator

"""
Landmark computation on a graph network
    - planar landmarks selection
    - farthest landmarks selection
"""

import json
from heapq import heappush, heappop
from quadtree import point_dict_to_quadtree, showQtree
from collections import defaultdict
from utils import haversine, bearing
from Dijkstra import Dijkstra
from Astar import Astar

class ALTpreprocessing:
    """
    Class that contains functions to find landmarks in a graph network
    """

    def __init__(self, graph, nodes_coords, qtree=None):
        self.graph = graph
        self.nodes_coords = nodes_coords
        self.qtree = qtree

    def initQuadTree(self, bucket_size):
        self.qtree = point_dict_to_quadtree(self.nodes_coords, bucket_size, multiquadtree=True)

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
        close_vertices = self.qtree.query_range(x - rng, x + rng, y - rng, y + rng)
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
        d = Dijkstra(self.graph, self.nodes_coords)
        return d.existShortestPath(s, t)

    def getLandmarksDistances(self, landmarks):
        """
        compute the shortest path from all nodes in the graph to all landmarks using
        A* => heuristic = euclidean distance between node and landmark
        """
        lm_dists = defaultdict(list)
        l = len(self.nodes_coords)
        for i, pid in enumerate(self.nodes_coords):
            # print(i, '/', l, ':', pid)
            for landmark, _ in landmarks:
                try:
                    astar = Astar(self.graph, self.nodes_coords)
                    d = astar.findShortestPath(pid, landmark)
                except KeyError:
                    d = None
                lm_dists[pid].append(d)
        return lm_dists

    def planarLandmarkSelection(self, k, origin):
        """
        Find k landmarks using the "planar landmark selection" method :
        divide the graph plane in k regions and for each region based on a central
        point, find a landmark that is the farthest from center in each region
        """
        origin_id = self.findClosestNode(origin)
        origin = self.nodes_coords[origin_id]
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


    def divideInRegions(self, k, origin):
        regions = [[] for _ in range(k)]
        region_size = 360.0 / k # angle
        for pid, coord in self.nodes_coords.items():
            b = bearing(origin[0], origin[1], coord[0], coord[1], True)
            s = int(b / region_size)
            regions[s].append((pid, coord))
        return regions

    def farthestLandmarkSelection(self, k, origin):
        landmarks = [origin] # TODO change to findClosestNode
        for _ in range(k):
            max_dist = float("-inf")
            best_candidate = None
            for pid, coord in self.nodes_coords.items():
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