import threading
from Timer import Timer
import Random
from Constants import *

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
    def __init__(self, threadID, name, graph, algo_name, lm_dists, priority, bucket_size, heuristic):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.success = True
        self.timer = Timer()
        s, t = Random.selectRandomPair(graph.getNodesIDs())
        self.algo = getSPalgoObject(graph, algo_name, s, t, priority, bucket_size, heuristic, lm_dists)

    def run(self):
        self.timer.start()
        self.success = self.algo.run()
        self.timer.stop()


class MultipleQueriesThread(threading.Thread):
    def __init__(self, threadID, name, graph, algos, lm_dists):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
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


def main():
    threads = []
    # create new threads
    for i in range(2):
        threads.append(SingleQueryThread(i + 1, "Exp" + str(i + 1)))

    # start new threads
    for i in range(2):
        threads[i].start()

    # synchronize
    for i in range(2):
        threads[i].join()

    print("Exiting Main Thread")


if __name__ == "__main__":
    main()
