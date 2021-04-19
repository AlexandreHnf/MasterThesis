# https://docs.python.org/3/library/heapq.html
from heapq import heappush, heappop
# https://pypi.org/project/fibheap/
from fibheap import *
from shortestPath import ShortestPath


class Dijkstra(ShortestPath):

    def __init__(self, graph, nodes, priority="bin", bucket_size=40):
        ShortestPath.__init__(self, graph, nodes, bucket_size)
        self.priority = priority  # the type of priority set data structure (str)

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

    def getPriorityList(self, s):
        """
        Creates a priority queue depending on the required data structure
        - list : a simple list
        - bin : a binary heap
        - fib : a fibonacci heap
        """
        simple_list = [(0, s)]
        if self.priority == "fib":
            fib_heap = makefheap()
            fheappush(fib_heap, simple_list[0])
            return fib_heap
        return simple_list

    def getHighestPriorityNode(self, priority_queue):
        if self.priority == "bin":
            return heappop(priority_queue)
        elif self.priority == "fib":
            return fheappop(priority_queue)
        else:  # list
            # simply take the unvisited node with smallest dist to far
            # assumes the priority queue is never empty
            if len(priority_queue) == 0:
                print("Aie")
            smallest = priority_queue[0][0]  # distance from start
            id_smallest = 0
            for i, (d, v) in enumerate(priority_queue):
                if d < smallest:
                    smallest = d
                    id_smallest = i
            return priority_queue.pop(id_smallest)

    def pushPriorityQueue(self, priority_queue, node):
        """
        Push new node to priority queue
        """
        if self.priority == "bin":
            heappush(priority_queue, node)
        elif self.priority == "fib":
            fheappush(priority_queue, node)
        else:  # list
            priority_queue.append(node)


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
        unvisited = self.getPriorityList(s)
        while unvisited:
            _, v = self.getHighestPriorityNode(unvisited)
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
            if neighbour in closed_set:
                continue
            new_dist = pred[v]["dist"] + arc_weight
            if neighbour not in pred or new_dist < pred[neighbour]["dist"]:
                pred[neighbour] = {"pred": v, "dist": new_dist}
                self.pushPriorityQueue(unvisited, (new_dist, neighbour) )