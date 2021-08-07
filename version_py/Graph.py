#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Utils import haversine
from Edge import Edge
from Quadtree import PointDictToQuadtree


class Graph:
    def __init__(self, nodes_coords, adj_list, bucket_size=40, name=""):
        self.nodes_coords = nodes_coords
        self.adj_list = adj_list
        self.rev_adj_list = self.setReverseGraph(self.adj_list)
        self.qtree = PointDictToQuadtree(nodes_coords, bucket_size, multiquadtree=True)
        self.name = name

    def getName(self):
        return self.name

    def getNbNodes(self):
        return len(self.nodes_coords)

    def getNodesCoords(self):
        return self.nodes_coords

    def getNodesIDs(self):
        return list(self.nodes_coords.keys())

    def getAdj(self, node):
        return self.adj_list[node]

    def getAdjList(self):
        return self.adj_list

    def getRevAdj(self, node):
        return self.rev_adj_list[node]

    def getRevAdjList(self):
        return self.rev_adj_list

    def getCoords(self, path):
        return {v: self.nodes_coords[v] for v in path}

    def getGeoCoords(self, node_id):
        if node_id > 0:
            return self.nodes_coords[node_id]

    def getQtree(self):
        return self.qtree

    def getNbEdges(self):
        nb_edges = 0
        for _, adj in self.adj_list.items():
            nb_edges += len(adj)
        return nb_edges

    def addEdge(self, start_node, edge):
        self.adj_list[start_node].append(edge)

    def addNode(self, node_id, edges, reference_node_id):
        if node_id in list(self.adj_list.keys()):
            print("node already in graph : ", node_id)
        self.adj_list[node_id] = edges
        self.nodes_coords[node_id] = self.nodes_coords[reference_node_id]

    def setReverseGraph(self, graph):
        reverse_graph = {v: [] for v in graph}
        for v in graph:
            for e in graph[v]:
                reverse_graph[e.getExtremityNode()].append(Edge(v,
                                                                e.getTravelType(),
                                                                e.getWeight(),
                                                                e.getLengthKm(),
                                                                e.getSpeed()))
        return reverse_graph

    def getReverseGraph(self):
        return self.rev_adj_list

    def getAvgDegree(self):
        avg_deg = 0
        for v, adj in self.adj_list.items():
            avg_deg += len(adj)

        return round(avg_deg / len(self.adj_list), 2)

    def getAvgDegreeTheoric(self):
        """
        For each edge, we have 2 vertices associated to it. Thus, the total degree is nb_edges*2
        """
        return round(2*self.getNbNodes()/self.getNbEdges(), 3)

    # def showGraph(self):
    #     for v, adj in self.adj_list.items():
    #         print("{0} : ".format(v), end="")
    #         for e in adj:
    #             print("--{0}, ".format(e.getExtremityNode()), end=" ")
    #         print()

    def findClosestNode(self, target, rng=.01):
        """
        Using the query_range function of the given quadtree, locate a vertex
        in the graph that is closest to the given point.

        Arguments:
        target -- (x, y) point to be matched to the graph.

        Returns:
        The ID of the vertex that is closest to the given point in the graph.
        """
        x, y = target
        close_vertices = self.qtree.query_range(x - rng, x + rng, y - rng, y + rng)
        best_vertex = None
        best_dist = float("inf")
        for point, vertices in close_vertices.items():
            dist = haversine(point[0], point[1], target[0], target[1])
            if dist < best_dist:
                best_dist = dist
                best_vertex = vertices[0]
        return best_vertex

    def findCenterNode(self):
        return self.findClosestNode(self.qtree.origin)

    def euclidean(self, id1, id2):
        """
        Returns the distance in KM between the two ID'd vertices.

        Arguments:
        id1, id2 -- IDs matching vertices in self.coords
        """
        x1, y1 = self.nodes_coords[id1]
        x2, y2 = self.nodes_coords[id2]
        return haversine(x1, y1, x2, y2)

    def manhattan(self, id1, id2):
        """
        Returns the Manhattan distance in KM between the two ID'd vertices.

        (x1, y1)
        [1]
         |
         |
         |
         |            (x2, y2)
        [3]-----------[2]
        (x1, y2)

        returns dist(1, 3) + dist(2, 3)
        """
        x1, y1 = self.nodes_coords[id1]
        x2, y2 = self.nodes_coords[id2]
        x3, y3 = x1, y2
        return haversine(x3, y3, x2, y2) + haversine(x3, y3, x1, y1)

    def octile(self, id1, id2):
        """
        Returns the octile distance in KM between the two ID'd vertices.

        (x1, y1)
        [1]
         |
         |
         |
        [3]
         | .
         |   .
         |     .
         |       .
         |         .
         |       45( .
        [ ]----------[2]

        returns dist(1, 3) + dist(2, 3)
        """
        x1, y1 = self.nodes_coords[id1]
        x2, y2 = self.nodes_coords[id2]
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        if dx > dy:
            x3 = max(x1, x2) - dy
            y3 = y1
        elif dx > dy:
            x3 = x1
            y3 = max(y1, y2) - dx
        else:
            return haversine(x1, y1, x2, y2)
        return haversine(x3, y3, x2, y2) + haversine(x3, y3, x1, y1)