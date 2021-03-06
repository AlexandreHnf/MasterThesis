import random
import Random
from Dijkstra import Dijkstra
from Astar import Astar
from ALT import ALT
from BidirectionalDijkstra import BidirectionalDijkstra
from BidirectionalAstar import BidirectionalAstar
from BidirectionalALT import BidirectionalALT
from ALTpreprocessing import ALTpreprocessing
from ParseOSMgraph import OSMgraphParser
from Constants import *
from Timer import Timer


class Benchmark:
    def __init__(self, graph):
        self.graph = graph
        self.irange = (1, self.graph.getNbNodes())

    def selectRandomPairs(self, irange, nb):
        pairs = []
        for _ in range(nb):
            pairs.append(Random.getRandomPair(irange))

        return pairs

    def getSPalgoObject(self, graph, algo_name, s, t, priority, bucket_size, heuristic, lm_dists):
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


    def testSingleQuery(self, nb_runs, algo_name, priority, bucket_size, heuristic, lm_dists):
        # TODO check if the results are coherent
        stats = {"avg_CT": 0, "avg_SS": 0, "avg_rel": 0}

        queries_timer = Timer()
        r = 1
        while r <= nb_runs:
            s, t = Random.selectRandomPair(self.graph.getNodesIDs())
            algo = self.getSPalgoObject(self.graph, algo_name, s, t, priority, bucket_size, heuristic, lm_dists)
            timer = Timer()
            f = algo.run()
            timer.end_timer()
            if not f:
                continue
            path_len = algo.getSPweight()

            stats["avg_CT"] += timer.getTimeElapsedSec()
            stats["avg_SS"] += algo.getSearchSpaceSize()
            stats["avg_rel"] += algo.getNbRelaxedEdges()

            #print(f"s: {s} t: {t} : SP len: {round(path_len, 2)} time: {round(timing, 4)} ss: {ss} rel: {rel}")
            r += 1

        stats["avg_CT"] = round(stats["avg_CT"] / nb_runs, 6)
        stats["avg_SS"] = round(stats["avg_SS"] / nb_runs)
        stats["avg_rel"] = round(stats["avg_rel"] / nb_runs)
        queries_timer.printTimeElapsedSec("Queries")
        return stats


    def testMultipleQueries(self, nb_runs, graph, algos, lm_dists=None, prepro_time=0):
        # TODO check if the results are coherent
        stats = {algo_name : {"avg_CT": 0, "avg_SS": 0, "avg_rel": 0} for algo_name in algos}

        queries_timer = Timer()
        r = 1
        while r <= nb_runs:
            s, t = Random.selectRandomPair(self.graph.getNodesIDs())
            # print(f"run: {r}, s: {s} t: {t}")
            success = True
            for algo_name in algos:
                #print("algo : ", algo_name)
                algo = self.getSPalgoObject(graph, algo_name, s, t, PRIORITY, BUCKET_SIZE, HEURISTIC, lm_dists)
                timer = Timer()
                f = algo.run()
                timer.end_timer()
                if not f:
                    success = False
                    break
                travel_types = algo.getSPTravelTypes()
                print(travel_types)

                stats[algo_name]["avg_CT"] += timer.getTimeElapsedSec() / nb_runs
                stats[algo_name]["avg_SS"] += algo.getSearchSpaceSize() / nb_runs
                stats[algo_name]["avg_rel"] += algo.getNbRelaxedEdges() / nb_runs
            if not success:
                continue
            r += 1
        # round
        for algo_name in algos:
            stats[algo_name]["avg_CT"] = round(stats[algo_name]["avg_CT"], 6)
            stats[algo_name]["avg_SS"] = round(stats[algo_name]["avg_SS"], 2)
            stats[algo_name]["avg_rel"] = round(stats[algo_name]["avg_rel"], 2)
            if algo_name in ["ALT", "BidiALT"]:
                stats[algo_name]["lm_dists_CT"] = prepro_time
            else:
                stats[algo_name]["lm_dists_CT"] = 0

        queries_timer.printTimeElapsedSec("Queries")
        return stats


    def testPreprocessing(self, lm_selection, nb_lm):
        """
        Test ALT preprocessing on the given graph
        TODO TOTEST
        """

        alt_pre = ALTpreprocessing(self.graph, lm_selection, None, nb_lm)
        prepro_timer = Timer()
        lm_dists = alt_pre.getLmDistances()
        # landmarks = alt_pre.getLandmarks()
        prepro_timer.end_timer()
        prepro_time = prepro_timer.getTimeElapsedSec()

        return {"lm_dists": lm_dists, "Prepro_time": prepro_time}


# =========================================================================================
    # basic experiments

    def testDijkstraQueue(self):
        # TODO : not used
        algos = {}
        name = "Dijkstra_"
        for q in ["list", "bin", "fib"]:
            algos[name + q] = Dijkstra(self.graph, -1, -1, q)
        stats = self.testMultipleQueries(10, algos)
        # TODO : ne pas prendre l'average

    def testAstarHeuristic(self):
        # TODO : not used
        algos = {}
        name = "Astar_"
        for h in ["euclidean", "manhattan", "octile"]:
            algos[name + h] = Astar(self.graph, -1, -1, "bin", 40, h)
        stats = self.testMultipleQueries(10, algos)
        # TODO : ne pas prendre l'average

    def testLmSelection(self):
        # TODO : not used
        for ls in ["random", "farthest", "planar"]:
            alt_pre = ALTpreprocessing(self.graph, ls, None, 16)
            lm_dists = alt_pre.getLmDistances()
            algos = {"alt": ALT(self.graph, -1, -1, lm_dists, "bin", 40, "")}
        stats = self.testMultipleQueries(10, algos)
        # TODO : ne pas prendre l'average

    # ==================================================
    # Advanced experiments


    def testSingleModal(self):
        # TODO TOTEST
        pass

    def testMultiModalTransport(self):
        # TODO TOTEST
        pass

    def testMultiModalStation(self):
        # TODO TOTEST
        pass



def main():
    p = OSMgraphParser(GRAPH_BXL)
    graph = p.parse()

    b = Benchmark(graph)
    stats = b.testSingleQuery(10)
    print(stats)


if __name__ == "__main__":
    main()