import threading
from Timer import Timer
import Random
from Constants import *
from heapq import heappush, heappop

from Dijkstra import Dijkstra
from Astar import Astar
from ALT import ALT
from BidirectionalDijkstra import BidirectionalDijkstra
from BidirectionalAstar import BidirectionalAstar
from BidirectionalALT import BidirectionalALT


def getSPalgoObject(graph, algo_name, s, t, priority, bucket_size, heuristic, lm_dists):
    """
    From the algorithm name, provide the shortest path object instance with the given
    parameters
    ex:  algos = ["Dijkstra", "A*", "ALT", "BidiDijkstra", "BidiAstar", "BidiALT"]
    """
    if algo_name == "Dijkstra":
        return Dijkstra(graph, s, t, priority, bucket_size)
    elif algo_name == "A*":
        return Astar(graph, s, t, priority, bucket_size, heuristic)
    elif algo_name == "ALT":
        return ALT(graph, s, t, lm_dists, priority, bucket_size, heuristic)
    elif algo_name == "BidiDijkstra":
        return BidirectionalDijkstra(graph, s, t, priority, bucket_size)
    elif algo_name == "BidiAstar":
        return BidirectionalAstar(graph, s, t, priority, bucket_size, heuristic)
    elif algo_name == "BidiALT":
        return BidirectionalALT(graph, s, t, lm_dists, priority, bucket_size, heuristic)


class SingleQueryThread(threading.Thread):
    def __init__(self, threadID, graph, algo_name, lm_dists, priority, bucket_size, heuristic):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.success = True
        self.timer = Timer()
        s, t = Random.selectRandomPair(graph.getNodesIDs())
        self.algo = getSPalgoObject(graph, algo_name, s, t, priority, bucket_size, heuristic, lm_dists)

    def run(self):
        self.timer.start()
        self.success = self.algo.run()
        self.timer.stop()


class MultipleQueriesThread(threading.Thread):
    def __init__(self, threadID, graph, algos, lm_dists):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.algos_success = True
        self.timer = Timer()

        self.algos = algos
        self.lm_dists = lm_dists
        self.graph = graph
        self.s, self.t = Random.selectRandomPair(graph.getNodesIDs())

        self.stat = {algo_name: {"avg_CT": 0, "avg_SS": 0, "avg_rel": 0} for algo_name in algos}

    def run(self):
        for algo_name in self.algos:
            self.timer.start()
            algo = getSPalgoObject(self.graph, algo_name, self.s, self.t,
                                   PRIORITY, BUCKET_SIZE, HEURISTIC, self.lm_dists)
            success = algo.run()
            self.timer.stop()
            self.stat[algo_name]["avg_CT"] += self.timer.getTimeElapsedSec()
            self.stat[algo_name]["avg_SS"] += algo.getSearchSpaceSize()
            self.stat[algo_name]["avg_rel"] += algo.getNbRelaxedEdges()


class MultipleQueriesMultimodalThread(threading.Thread):
    def __init__(self, threadID, graph, algos, lm_dists, prepro_time):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.algos_success = True
        self.timer = Timer()

        self.algos = algos
        self.lm_dists = lm_dists
        self.graph = graph
        self.s, self.t = Random.selectRandomPair(graph.getNodesIDs())

        self.stat = {algo_name: {"avg_CT": 0, "avg_SS": 0, "avg_rel": 0, "max_avg_lb": 0,
                                 "avg_travel_types": {}} for algo_name in algos}

    def addTravelTypesStats(self, algo_name, travel_types):
        for key in travel_types:
            if key not in self.stat[algo_name]["avg_travel_types"]:
                self.stat[algo_name]["avg_travel_types"][key] = travel_types[key]
            else:
                self.stat[algo_name]["avg_travel_types"][key] += travel_types[key]

    def run(self):
        for algo_name in self.algos:
            self.timer.start()
            algo = getSPalgoObject(self.graph, algo_name, self.s, self.t,
                                   PRIORITY, BUCKET_SIZE, HEURISTIC, self.lm_dists)
            success = algo.run()
            self.timer.stop()
            travel_types = algo.getSPTravelTypes()

            self.stat[algo_name]["avg_CT"] += self.timer.getTimeElapsedSec()
            self.stat[algo_name]["avg_SS"] += algo.getSearchSpaceSize()
            self.stat[algo_name]["avg_rel"] += algo.getNbRelaxedEdges()
            if algo_name == "ALT":
                self.stat[algo_name]["max_avg_lb"] += algo.getAvgMaxHeuristicDist()
            self.addTravelTypesStats(algo_name, travel_types)



