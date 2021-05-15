from utils import haversine
from Edge import Edge
from quadtree import Quadtree, MultiQuadtree, PointDictToQuadtree

class Graph:
    def __init__(self, nodes_coords, adj_list, bucket_size=40):
        self.nodes_coords = nodes_coords
        self.adj_list = adj_list
        self.qtree = PointDictToQuadtree(nodes_coords, bucket_size, multiquadtree=True)

    def getNbEdges(self):
        nb_edges = 0
        for _, adj in self.adj_list.items():
            nb_edges += len(adj)
        return nb_edges

    def getReverseGraph(self, graph):
        reverse_graph = {v: [] for v in graph}
        for v in graph:
            for edge in graph[v]:
                reverse_graph[edge.getExtremityNode()].append(Edge(v, edge.getWeight()))
        return reverse_graph

    def getAvgDegree(self):
        # TODO
        pass

    def showGraph(self):
        for v, adj in self.adj_list.items():
            print("{0} : ".format(v), end="")
            for e in adj:
                print("--{0}, ".format(e.getExtremityNode()), end=" ")
            print()

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

    def _euclidean(self, id1, id2):
        """
        Returns the distance in KM between the two ID'd vertices.

        Arguments:
        id1, id2 -- IDs matching vertices in self.coords
        """
        x1, y1 = self.coords[id1]
        x2, y2 = self.coords[id2]
        return haversine(x1, y1, x2, y2)

    def _manhattan(self, id1, id2):
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
        x1, y1 = self.coords[id1]
        x2, y2 = self.coords[id2]
        x3, y3 = x1, y2
        return haversine(x3, y3, x2, y2) + haversine(x3, y3, x1, y1)

    def _octile(self, id1, id2):
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
        x1, y1 = self.coords[id1]
        x2, y2 = self.coords[id2]
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