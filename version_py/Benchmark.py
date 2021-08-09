#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
from Thread import SingleQueryThread, MultipleQueriesThread, MultipleQueriesMultimodalThread


class Benchmark:
    def __init__(self, graph, nb_runs):
        self.graph = graph
        self.nb_runs = nb_runs
        self.irange = (1, self.graph.getNbNodes())
        self.st_pairs = Random.getRandomPairs(self.graph.getNodesIDs(), nb_runs)

    def testSingleQuery(self, algo_name, priority, bucket_size, heuristic, lm_dists):
        stats = {"avg_CT": 0, "avg_SS": 0, "avg_RS": 0}

        queries_timer = Timer()
        queries_timer.start()

        threads = []
        # create new threads
        for i in range(self.nb_runs):
            my_thread = SingleQueryThread(i + 1, self.graph, algo_name, lm_dists, priority, bucket_size, heuristic)
            my_thread.start()
            threads.append(my_thread)

        # synchronize
        for i in range(self.nb_runs):
            threads[i].join()

        for i in range(self.nb_runs):
            if threads[i].success:
                # print("thread {0} : {1}".format(threads[i].threadID, threads[i].timer.getTimeElapsedSec()))
                stats["avg_CT"] += threads[i].timer.getTimeElapsedSec()
                stats["avg_SS"] += threads[i].algo.getSearchSpaceSize()
                stats["avg_RS"] += threads[i].algo.getNbRelaxedEdges()

        # ===================================

        stats["avg_CT"] = round(stats["avg_CT"] / self.nb_runs, 6)
        stats["avg_SS"] = round(stats["avg_SS"] / self.nb_runs)
        stats["avg_RS"] = round(stats["avg_RS"] / self.nb_runs)
        queries_timer.printTimeElapsedSec("Queries")
        return stats

    def testMultipleQueries(self, graph, algos, lm_dists=None, prepro_time=0):
        stats = {algo_name: {"avg_CT": 0, "avg_SS": 0, "avg_RS": 0} for algo_name in algos}

        queries_timer = Timer()
        queries_timer.start()

        threads = []
        # create new threads
        for i in range(self.nb_runs):
            my_thread = MultipleQueriesThread(i + 1, graph, algos, lm_dists)
            my_thread.start()
            threads.append(my_thread)

        # synchronize
        for i in range(self.nb_runs):
            threads[i].join()

        for i in range(self.nb_runs):
            for algo_name in algos:
                stats[algo_name]["avg_CT"] += threads[i].stat[algo_name]["avg_CT"]
                stats[algo_name]["avg_SS"] += threads[i].stat[algo_name]["avg_SS"]
                stats[algo_name]["avg_RS"] += threads[i].stat[algo_name]["avg_RS"]

        # round
        for algo_name in algos:
            stats[algo_name]["avg_CT"] = round(stats[algo_name]["avg_CT"] / self.nb_runs, 7)
            stats[algo_name]["avg_SS"] = round(stats[algo_name]["avg_SS"] / self.nb_runs, 2)
            stats[algo_name]["avg_RS"] = round(stats[algo_name]["avg_RS"] / self.nb_runs, 2)
            if algo_name in ["ALT", "BidiALT"]:
                stats[algo_name]["lm_dists_CT"] = prepro_time
            else:
                stats[algo_name]["lm_dists_CT"] = 0

        queries_timer.printTimeElapsedSec("Queries")
        return stats

    def addTravelTypesStats(self, stats, algo_name, travel_types):
        for key in travel_types:
            if key not in stats[algo_name]["avg_travel_types"]:
                stats[algo_name]["avg_travel_types"][key] = travel_types[key]
            else:
                t = stats[algo_name]["avg_travel_types"][key]
                stats[algo_name]["avg_travel_types"][key] = round(t + travel_types[key] / self.nb_runs, 2)

    def testMultipleQueriesMultiModal(self, graph, algos, lm_dists=None, prepro_time=0):
        stats = {algo_name: {"avg_CT": 0, "avg_SS": 0, "avg_RS": 0, "max_avg_lb": 0,
                             "avg_travel_types": {}} for algo_name in algos}

        queries_timer = Timer()
        queries_timer.start()

        threads = []
        # create new threads
        for i in range(self.nb_runs):
            my_thread = MultipleQueriesMultimodalThread(i + 1, graph, algos, lm_dists, prepro_time)
            my_thread.start()
            threads.append(my_thread)

        # synchronize
        for i in range(self.nb_runs):
            threads[i].join()

        for i in range(self.nb_runs):
            for algo_name in algos:
                stats[algo_name]["avg_CT"] += threads[i].stat[algo_name]["avg_CT"]
                stats[algo_name]["avg_SS"] += threads[i].stat[algo_name]["avg_SS"]
                stats[algo_name]["avg_RS"] += threads[i].stat[algo_name]["avg_RS"]
                if algo_name == "ALT":
                    stats[algo_name]["max_avg_lb"] += threads[i].stat[algo_name]["max_avg_lb"]
                self.addTravelTypesStats(stats, algo_name, threads[i].stat[algo_name]["avg_travel_types"], self.nb_runs)

        # round
        for algo_name in algos:
            stats[algo_name]["avg_CT"] = round(stats[algo_name]["avg_CT"] / self.nb_runs, 6)
            stats[algo_name]["avg_SS"] = round(stats[algo_name]["avg_SS"] / self.nb_runs, 2)
            stats[algo_name]["avg_RS"] = round(stats[algo_name]["avg_RS"] / self.nb_runs, 2)
            if algo_name in ["ALT", "BidiALT"]:
                stats[algo_name]["max_avg_lb"] = round(stats[algo_name]["max_avg_lb"] / self.nb_runs, 2)
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