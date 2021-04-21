# https://docs.python.org/3/library/heapq.html
from heapq import heappush, heappop
# https://pypi.org/project/fibheap/
from fibheap import *
from shortestPath import ShortestPath


class Dijkstra(ShortestPath):

    def __init__(self, graph, nodes, s, t, priority="bin", bucket_size=40):
        ShortestPath.__init__(self, graph, nodes, s, t, bucket_size)

        self.search_space = []
        self.search_space_size = 0
        self.nb_relax_edges = 0
        self.dists_so_far = {self.s: 0}  # shortest distance so far from source node
        self.preds = {self.s: None}
        # self.pred = {self.s: {"dist": 0, "pred": None}}  # TODO : maybe split in two lists
        self.closed_set = set()
        self.priority = priority  # the type of priority set data structure (str)
        self.unvisited = self.getPriorityList()

    def getDistSoFar(self):
        return self.dists_so_far

    def getSearchSpace(self):
        return self.search_space

    def getSearchSpaceSize(self):
        return self.search_space_size

    def getNbRelaxedEdges(self):
        return self.nb_relax_edges

    def getPredecessors(self):
        return self.preds

    def getSearchSpaceCoords(self):
        """
        get a dictionary of all the nodes in the search space of the
        algorithm with geometric coordinates
        """
        needed = {}
        coords = self.util.coords
        for vertex, neighbours in self.search_space[1:]:
            needed[vertex] = coords[vertex]
            for arc in neighbours:
                needed[arc] = coords[arc]
        return needed

    def constructShortestPath(self):
        """
        Given a pred (predecessor) list created by the shortest path algorithm, and the
        destination node's ID, returns the shortest path containing all these
        nodes. => will give the actual shortest path computed by the algorithm.
        """
        sp = []
        v = self.t
        while self.preds[v]:  # is not None
            sp.append(v)
            v = self.preds[v]
        sp.append(self.s)  # source
        sp.reverse()  # to have the path from source to dest and not t to s
        return {v: self.util.coords[v] for v in sp}

    def processSearchResult(self):
        search_space_coords = self.getSearchSpaceCoords()
        shortest_path = self.constructShortestPath()
        return search_space_coords, shortest_path

    def findShortestPath(self):
        exist_sol = self.dijkstra()
        if not exist_sol:
            return None
        return self.processSearchResult()

    def getDistsSourceToNodes(self):
        """
        Compute Dijkstra from a node s to all other nodes in the graph
        returns the set of shortest distances to those nodes
        """
        self.dijkstra()
        return

    def existShortestPath(self):
        """
        Check whether there exists a shortest path from s to t
        """
        # s, t = self.findSourceDest(source, dest)
        return self.dijkstra()

    def getPriorityList(self):
        """
        Creates a priority queue depending on the required data structure
        - list : a simple list
        - bin : a binary heap
        - fib : a fibonacci heap
        """
        simple_list = [(0, self.s)]
        if self.priority == "fib":
            fib_heap = makefheap()
            fheappush(fib_heap, simple_list[0])
            return fib_heap
        return simple_list

    def getHighestPriorityNode(self):
        if self.priority == "bin":
            return heappop(self.unvisited)
        elif self.priority == "fib":
            return fheappop(self.unvisited)
        else:  # list
            # simply take the unvisited node with smallest dist to far
            # assumes the priority queue is never empty
            if len(self.unvisited) == 0:
                print("Aie (in getHighestPriorityNode of Dijkstra.py)")
            smallest = self.unvisited[0][0]  # distance from start
            id_smallest = 0
            for i, (d, v) in enumerate(self.unvisited):
                if d < smallest:
                    smallest = d
                    id_smallest = i
            return self.unvisited.pop(id_smallest)

    def pushPriorityQueue(self, node):
        """
        Push new node to priority queue
        """
        if self.priority == "bin":
            heappush(self.unvisited, node)
        elif self.priority == "fib":
            fheappush(self.unvisited, node)
        else:  # list
            self.unvisited.append(node)


    def dijkstra(self):
        """
        Find the shortest path from s to t.
        Result = a sequence of nodes belonging to the shortest path
        """
        if not self.s or not self.t:
            return False
        while self.unvisited:  # not empty
            self.search_space_size += 1
            _, v = self.getHighestPriorityNode()
            self.search_space.append( (self.preds[v], [v]) )
            if v in self.closed_set:
                continue
            elif v == self.t:
                return True
            self.closed_set.add(v)
            self.relaxVertex(v)
        return False  # if no valid path has been found (some node inaccessible before t

    def relaxVertex(self, v):
        """
        # v = the current vertex
        Relax all arcs coming from vertex v
        """
        for arc in self.graph[v]:
            neighbour = arc.getExtremityNode()
            self.nb_relax_edges += 1
            if neighbour in self.closed_set:
                continue
            new_dist = self.dists_so_far[v] + arc.getWeight()
            if neighbour not in self.preds or new_dist < self.dists_so_far[neighbour]:
                self.preds[neighbour] = v
                self.dists_so_far[neighbour] = new_dist
                self.pushPriorityQueue( (new_dist, neighbour) )