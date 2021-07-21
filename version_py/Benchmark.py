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


    def runAlgo(self, graph, algo_name, s, t, lm_dists, priority, bucket_size, heuristic):
        algo = self.getSPalgoObject(graph, algo_name, s, t, priority, bucket_size, heuristic, lm_dists)
        timer = Timer()
        success = algo.run()
        timer.end_timer()

        return success, timer, algo


    def testSingleQuery(self, nb_runs, algo_name, priority, bucket_size, heuristic, lm_dists):
        # TODO check if the results are coherent
        stats = {"avg_CT": 0, "avg_SS": 0, "avg_rel": 0}

        queries_timer = Timer()
        r = 1
        while r <= nb_runs:
            s, t = Random.selectRandomPair(self.graph.getNodesIDs())
            success, timer, algo = self.runAlgo(self.graph, algo_name, s, t, lm_dists, priority, bucket_size, heuristic)
            if not success:
                continue

            stats["avg_CT"] += timer.getTimeElapsedSec()
            stats["avg_SS"] += algo.getSearchSpaceSize()
            stats["avg_rel"] += algo.getNbRelaxedEdges()

            # print(f"s: {s} t: {t} : SP len: {round(path_len, 2)} time: {round(timing, 4)} ss: {ss} rel: {rel}")
            r += 1

        stats["avg_CT"] = round(stats["avg_CT"] / nb_runs, 6)
        stats["avg_SS"] = round(stats["avg_SS"] / nb_runs)
        stats["avg_rel"] = round(stats["avg_rel"] / nb_runs)
        queries_timer.printTimeElapsedSec("Queries")
        return stats


    def testMultipleQueries(self, nb_runs, graph, algos, lm_dists=None, prepro_time=0):
        # TODO check if the results are coherent
        stats = {algo_name: {"avg_CT": 0, "avg_SS": 0, "avg_rel": 0} for algo_name in algos}

        queries_timer = Timer()
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
        # TODO check if the results are coherent
        stats = {algo_name: {"avg_CT": 0, "avg_SS": 0, "avg_rel": 0, "avg_travel_types": {}} for algo_name in algos}

        queries_timer = Timer()
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
                #print(travel_types)

                stats[algo_name]["avg_CT"] += timer.getTimeElapsedSec() / nb_runs
                stats[algo_name]["avg_SS"] += algo.getSearchSpaceSize() / nb_runs
                stats[algo_name]["avg_rel"] += algo.getNbRelaxedEdges() / nb_runs
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
        lm_dists = alt_pre.getLmDistances()
        # landmarks = alt_pre.getLandmarks()
        prepro_timer.end_timer()
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
