# https://docs.python.org/3/library/heapq.html
from heapq import heappush, heappop
# https://pypi.org/project/fibheap/
from fibheap import *
from ShortestPath import ShortestPath


class BidirectionalDijkstra(ShortestPath):

    def __init__(self, graph, s, t, priority="bin", bucket_size = 40):
        ShortestPath.__init__(self, graph, s, t, bucket_size)

        self.dist_so_far = []
        self.search_space = []
        self.search_space_size = 0
        self.nb_relax_edges = 0

        self.priority = priority  # the type of priority set data structure (str)

        self.fwd_pred = {self.s : {"dist": 0, "pred": None}}
        self.bwd_pred = {self.t : {"dist": 0, "pred": None}}

        self.midpoint = None

    def getSearchSpaceSize(self):
        return self.search_space_size

    def getNbRelaxedEdges(self):
        return self.nb_relax_edges

    def getMidpoint(self):
        return self.midpoint

    def getSearchSpaceCoords(self):
        """
        get a dictionary of all the nodes in the search space of the
        algorithm with geometric coordinates
        """
        needed = {}
        for vertex, neighbours in self.search_space[2:]:
            needed[vertex] = self.graph.getNodesCoords()[vertex]
            for arc in neighbours:
                needed[arc] = self.graph.getNodesCoords()[arc]
        return needed

    def constructShortestPath(self):
        """
        s ----- midpoint ----- t
        """
        fwd_sp = []
        v = self.midpoint
        while self.fwd_pred[v]["pred"] is not None:
            fwd_sp.append(v)
            v = self.fwd_pred[v]["pred"]
        fwd_sp.reverse()
        fwd_sp.pop() # remove duplicate midpoint

        bwd_sp = []
        v = self.midpoint
        while self.bwd_pred[v]["pred"] is not None:
            bwd_sp.append(v)
            v = self.bwd_pred[v]["pred"]

        sp = [self.s] + fwd_sp + bwd_sp + [self.t]
        return sp, self.graph.getCoords(sp)

    def processSearchResult(self):
        search_space_coords = self.getSearchSpaceCoords()
        shortest_path, sp_coords = self.constructShortestPath()
        return search_space_coords, shortest_path, sp_coords

    def findShortestPath(self):
        exist_sol = self.run()
        if not exist_sol:
            return None

        print("midpoint : ", self.midpoint)
        return self.processSearchResult()

    def getSPweight(self):
        sp, sp_coords = self.constructShortestPath()
        return self.getPathLength(sp)

    def getPriorityList(self, simple_list):
        """
        Creates a priority queue depending on the required data structure
        - list : a simple list
        - bin : a binary heap
        - fib : a fibonacci heap
        """
        if self.priority == "fib":
            fib_heap = makefheap()
            fheappush(fib_heap, simple_list[0])
            return fib_heap
        return simple_list

    def getHighestPriorityNode(self, unvisited_set):
        if self.priority == "bin":
            return heappop(unvisited_set)
        elif self.priority == "fib":
            return fheappop(unvisited_set)
        else:  # list
            # simply take the unvisited node with smallest dist to far
            # assumes the priority queue is never empty
            if len(unvisited_set) == 0:
                print("Aie (in getHighestPriorityNode of Dijkstra.py)")
            smallest = unvisited_set[0][0]  # distance from start
            id_smallest = 0
            for i, (d, v) in enumerate(unvisited_set):
                if d < smallest:
                    smallest = d
                    id_smallest = i
            return unvisited_set.pop(id_smallest)

    def pushPriorityQueue(self, unvisited_set, node):
        """
        Push new node to priority queue
        """
        if self.priority == "bin":
            heappush(unvisited_set, node)
        elif self.priority == "fib":
            fheappush(unvisited_set, node)
        else:  # list
            unvisited_set.append(node)

    def relaxVertexForward(self, v, closed_set, unvisited_set):
        """
        FORWARD
        # v = the current vertex
        Relax all arcs coming from vertex v
        """
        for arc in self.graph.getAdj(v):
            neighbour = arc.getExtremityNode()
            if neighbour in closed_set:
                continue
            self.nb_relax_edges += 1
            new_dist = self.fwd_pred[v]["dist"] + arc.getWeight()
            if neighbour not in self.fwd_pred or new_dist < self.fwd_pred[neighbour]["dist"]:
                self.fwd_pred[neighbour] = {"pred": v, "dist": new_dist}
                self.pushPriorityQueue(unvisited_set, (new_dist, neighbour))

    def relaxVertexBackward(self, v, closed_set, unvisited_set):
        """
        BACKWARD
        # v = the current vertex
        Relax all arcs coming from vertex v
        """
        for arc in self.graph.getRevAdj(v):  # REVERSE GRAPH
            neighbour = arc.getExtremityNode()
            if neighbour in closed_set:
                continue
            self.nb_relax_edges += 1
            new_dist = self.bwd_pred[v]["dist"] + arc.getWeight()
            if neighbour not in self.bwd_pred or new_dist < self.bwd_pred[neighbour]["dist"]:
                self.bwd_pred[neighbour] = {"pred": v, "dist": new_dist}
                self.pushPriorityQueue(unvisited_set, (new_dist, neighbour))

    def scan(self, unvisited_set, closed_set, direction):
        _, v = self.getHighestPriorityNode(unvisited_set)
        closed_set.add(v)
        if direction == "F":
            self.relaxVertexForward(v, closed_set, unvisited_set)
        elif direction == "B":
            self.relaxVertexBackward(v, closed_set, unvisited_set)
        return v

    def bidirectionalCheckForward(self, v):
        self.search_space.append( (self.fwd_pred[v]["pred"], [v]) )
        if v in self.bwd_pred:
            return self.bwd_pred[v]["dist"] + self.fwd_pred[v]["dist"]
        return float("inf")

    def bidirectionalCheckBackward(self, v):
        self.search_space.append( (self.bwd_pred[v]["pred"], [v]) )
        if v in self.fwd_pred:
            return self.fwd_pred[v]["dist"] + self.bwd_pred[v]["dist"]
        return float("inf")

    def run(self):
        if not self.s or not self.t:
            return False
        shortest_path_length = float("inf")
        fwd_unvisited = self.getPriorityList([(0, self.s)])
        fwd_closed_set = set()
        bwd_unvisited = self.getPriorityList([(0, self.t)])
        bwd_closed = set()

        while fwd_unvisited and bwd_unvisited:  # while not empty
            self.search_space_size += 2  # forward and backward node chosen

            # forward search
            fwd_scanned_v = self.scan(fwd_unvisited, fwd_closed_set, "F")
            fwd_path_length = self.bidirectionalCheckForward(fwd_scanned_v)
            if fwd_path_length > shortest_path_length:
                return True
            shortest_path_length = fwd_path_length
            self.midpoint = fwd_scanned_v

            # backward search
            bwd_scanned_v = self.scan(bwd_unvisited, bwd_closed, "B")
            bwd_path_length = self.bidirectionalCheckBackward(bwd_scanned_v)
            if bwd_path_length > shortest_path_length:
                return True
            shortest_path_length = bwd_path_length
            self.midpoint = bwd_scanned_v

        return False  # no valid solution has been found






