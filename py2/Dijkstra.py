from heapq import heappush, heappop
from shortestPath import ShortestPath

class Dijkstra(ShortestPath):

    def __init__(self, graph, nodes_coords):
        ShortestPath.__init__(self, graph, nodes_coords)

    def findShortestPath(self, source, dest):
        s, t = self.findSourceDest(source, dest)
        path, pred = self.dijkstra(s, t)
        return self.processSearchResult(path, pred, t)

    def dijkstra(self, s, t):
        """
        Find the shortest path from s to t.
        Result = a sequence of nodes belonging to the shortest path
        """
        if not s or not t:
            return {}, []
        sequence = []
        pred = {s : {"dist": 0, "pred": None}}
        closed_set = set()
        unvisited = [(0, s)] # datastructure : heap, fibonacci heap, or simple list
        while unvisited:
            _, v = heappop(unvisited)
            sequence.append( (pred[v]["pred"], [v]) )
            if v in closed_set:
                continue
            elif v == t:
                return sequence[1:], pred
            closed_set.add(v)
            self.relaxVertex(v, t, pred, unvisited, closed_set)
        return None # if no valid path has been found (some node inaccessible before t

    def relaxVertex(self, v, t, pred, unvisited, closed_set):
        """
        # v = the current vertex, t = destination node
        Relax all arcs coming from vertex v
        """
        for neighbour, arc_weight in self.graph[v]:
            if neighbour in closed_set:
                continue
            new_dist = pred[v]["dist"] + arc_weight
            if neighbour not in pred or new_dist < pred[neighbour]["dist"]:
                pred[neighbour] = {"pred": v, "dist": new_dist}
                heappush(unvisited, (new_dist, neighbour) )