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
from Thread import SingleQueryThread


class Benchmark:
    def __init__(self, graph):
        self.graph = graph
        self.irange = (1, self.graph.getNbNodes())


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


    def runAlgo(self, graph, algo_name, s, t, lm_dists, priority, bucket_size, heuristic):
        algo = self.getSPalgoObject(graph, algo_name, s, t, priority, bucket_size, heuristic, lm_dists)
        timer = Timer()
        timer.start()
        success = algo.run()
        timer.stop()

        return success, timer, algo


    def testSingleQuery(self, nb_runs, algo_name, priority, bucket_size, heuristic, lm_dists):
        stats = {"avg_CT": 0, "avg_SS": 0, "avg_rel": 0}

        queries_timer = Timer()
        queries_timer.start()

        threads = []
        # create new threads
        for i in range(nb_runs):
            my_thread = SingleQueryThread(i + 1, "Exp1", self.graph, algo_name, lm_dists, priority, bucket_size, heuristic)
            my_thread.start()
            threads.append(my_thread)

        # synchronize
        for i in range(nb_runs):
            threads[i].join()

        for i in range(nb_runs):
            if threads[i].success:
                # print("thread {0} : {1}".format(threads[i].threadID, threads[i].timer.getTimeElapsedSec()))
                stats["avg_CT"] += threads[i].timer.getTimeElapsedSec()
                stats["avg_SS"] += threads[i].algo.getSearchSpaceSize()
                stats["avg_rel"] += threads[i].algo.getNbRelaxedEdges()

        # ===================================

        stats["avg_CT"] = round(stats["avg_CT"] / nb_runs, 6)
        stats["avg_SS"] = round(stats["avg_SS"] / nb_runs)
        stats["avg_rel"] = round(stats["avg_rel"] / nb_runs)
        queries_timer.printTimeElapsedSec("Queries")
        return stats


    def testMultipleQueries(self, nb_runs, graph, algos, lm_dists=None, prepro_time=0):
        stats = {algo_name: {"avg_CT": 0, "avg_SS": 0, "avg_rel": 0} for algo_name in algos}

        queries_timer = Timer()
        queries_timer.start()
        r = 1
        while r <= nb_runs:
            s, t = Random.selectRandomPair(self.graph.getNodesIDs())
            # print(f"run: {r}, s: {s} t: {t}")
            algos_success = True
            for algo_name in algos:
                success, timer, algo = self.runAlgo(graph, algo_name, s, t, lm_dists, PRIORITY, BUCKET_SIZE, HEURISTIC)
                if not success:
                    algos_success = False
                    break

                stats[algo_name]["avg_CT"] += timer.getTimeElapsedSec() / nb_runs
                stats[algo_name]["avg_SS"] += algo.getSearchSpaceSize() / nb_runs
                stats[algo_name]["avg_rel"] += algo.getNbRelaxedEdges() / nb_runs
            if not algos_success:
                continue
            r += 1
        # round
        for algo_name in algos:
            stats[algo_name]["avg_CT"] = round(stats[algo_name]["avg_CT"], 7)
            stats[algo_name]["avg_SS"] = round(stats[algo_name]["avg_SS"], 2)
            stats[algo_name]["avg_rel"] = round(stats[algo_name]["avg_rel"], 2)
            if algo_name in ["ALT", "BidiALT"]:
                stats[algo_name]["lm_dists_CT"] = prepro_time
            else:
                stats[algo_name]["lm_dists_CT"] = 0

        queries_timer.printTimeElapsedSec("Queries")
        return stats


    def addTravelTypesStats(self, stats, algo_name, travel_types, nb_runs):
        for key in travel_types:
            if key not in stats[algo_name]["avg_travel_types"]:
                stats[algo_name]["avg_travel_types"][key] = travel_types[key]
            else:
                t = stats[algo_name]["avg_travel_types"][key]
                stats[algo_name]["avg_travel_types"][key] = round(t + travel_types[key] / nb_runs, 2)


    def testMultipleQueriesMultiModal(self, nb_runs, graph, algos, lm_dists=None, prepro_time=0):
        stats = {algo_name: {"avg_CT": 0, "avg_SS": 0, "avg_rel": 0, "max_avg_lb": 0,
                             "avg_travel_types": {}} for algo_name in algos}

        queries_timer = Timer()
        queries_timer.start()
        r = 1
        while r <= nb_runs:
            s, t = Random.selectRandomPair(self.graph.getNodesIDs())
            algos_success = True
            for algo_name in algos:
                success, timer, algo = self.runAlgo(graph, algo_name, s, t, lm_dists, PRIORITY, BUCKET_SIZE, HEURISTIC)
                if not success:
                    algos_success = False
                    break
                travel_types = algo.getSPTravelTypes()

                stats[algo_name]["avg_CT"] += timer.getTimeElapsedSec() / nb_runs
                stats[algo_name]["avg_SS"] += algo.getSearchSpaceSize() / nb_runs
                stats[algo_name]["avg_rel"] += algo.getNbRelaxedEdges() / nb_runs
                if algo_name == "ALT":
                    stats[algo_name]["max_avg_lb"] += algo.getAvgMaxHeuristicDist() / nb_runs
                self.addTravelTypesStats(stats, algo_name, travel_types, nb_runs)

            if not algos_success:
                continue
            r += 1
        # round
        for algo_name in algos:
            stats[algo_name]["avg_CT"] = round(stats[algo_name]["avg_CT"], 6)
            stats[algo_name]["avg_SS"] = round(stats[algo_name]["avg_SS"], 2)
            stats[algo_name]["avg_rel"] = round(stats[algo_name]["avg_rel"], 2)
            if algo_name in ["ALT", "BidiALT"]:
                stats[algo_name]["max_avg_lb"] = round(stats[algo_name]["max_avg_lb"], 2)
                stats[algo_name]["lm_dists_CT"] = prepro_time
            else:
                stats[algo_name]["lm_dists_CT"] = 0

        queries_timer.printTimeElapsedSec("Queries")
        return stats


    def testPreprocessing(self, lm_selection, nb_lm):
        """
        Test ALT preprocessing on the given graph
        """

        alt_pre = ALTpreprocessing(self.graph, lm_selection, None, nb_lm)
        prepro_timer = Timer()
        prepro_timer.start()
        lm_dists = alt_pre.getLmDistances()
        # landmarks = alt_pre.getLandmarks()
        prepro_timer.stop()
        prepro_time = prepro_timer.getTimeElapsedSec()

        return {"lm_dists": lm_dists, "Prepro_time": prepro_time}


    # ==================================================


def main():
    p = OSMgraphParser(GRAPH_BXL)
    graph = p.parse()

    b = Benchmark(graph)
    stats = b.testSingleQuery(10)
    print(stats)


if __name__ == "__main__":
    main()
