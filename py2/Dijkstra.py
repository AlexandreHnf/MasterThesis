from heapq import heappush, heappop
from shortestPath import ShortestPath

class Dijkstra(ShortestPath):

    def __init__(self, graph, nodes_coords, bucket_size=40):
        ShortestPath.__init__(self, graph, nodes_coords, bucket_size)

    def findShortestPath(self, source, dest):
        s, t = self.findSourceDest(source, dest)
        search_space, pred = self.dijkstra(s, t)
        return self.processSearchResult(search_space, pred, s, t)

    def existShortestPath(self, source, dest):
        """
        Check whether there exists a shortest path from s to t
        """
        # s, t = self.findSourceDest(source, dest)
        path, pred = self.dijkstra(source, dest)
        return not (path == {} and pred == [])

    def dijkstra(self, s, t):
        """
        Find the shortest path from s to t.
        Result = a sequence of nodes belonging to the shortest path
        """
        if not s or not t:
            return {}, []
        search_space = []
        pred = {s : {"dist": 0, "pred": None}}
        closed_set = set()
        unvisited = [(0, s)]  # TODO : datastructure : heap, fibonacci heap, or simple list
        while unvisited:
            _, v = heappop(unvisited)
            # print("current : {0}, dist to t : {1}".format(v, pred[v]["dist"]))
            search_space.append( (pred[v]["pred"], [v]) )
            if v in closed_set:
                continue
            elif v == t:
                return search_space[1:], pred
            closed_set.add(v)
            self.relaxVertex(v, t, pred, unvisited, closed_set)
        return {}, []  # if no valid path has been found (some node inaccessible before t

    def relaxVertex(self, v, t, pred, unvisited, closed_set):
        """
        # v = the current vertex, t = destination node
        Relax all arcs coming from vertex v
        """
        for neighbour, arc_weight in self.graph[v]:
            # print("neighbour : ", neighbour)
            if neighbour in closed_set:
                continue
            new_dist = pred[v]["dist"] + arc_weight
            # print("=> new dist : ", new_dist)
            # print("=> pre dist : ", pred.get(neighbour, None))
            if neighbour not in pred or new_dist < pred[neighbour]["dist"]:
                # if neighbour not in pred:
                    # print("v has been here")
                pred[neighbour] = {"pred": v, "dist": new_dist}
                heappush(unvisited, (new_dist, neighbour) )