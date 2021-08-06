import copy
import IO

from Benchmark import *
from MultiModalGraph import *
from ParseOSMgraph import OSMgraphParser
from copy import deepcopy
from Visualization import *
from Timer import Timer




def experiment1(graphs_names):
    """
    Experiment 1 : test which queue type gives fastest Dijkstra
    - List (list)
    - Binary Heap (bin)
    - Fibonacci Heap (fib)
    """
    print("EXPERIMENT 1 : which priority queue Dijkstra")
    all_stats = {}
    for graph_name in graphs_names:
        print("GRAPH : ", graph_name)

        p = OSMgraphParser(graph_name)
        graph = p.parse()

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(),
                                 "nb_edges": graph.getNbEdges(),
                                 "avg_deg": graph.getAvgDegree()}

        # Benchmark
        b = Benchmark(graph)

        stats = {"bin": None, "fib": None, "list": None}
        for p in stats.keys():
            print("Priority : ", p)
            stat = b.testSingleQuery(NB_RUNS, "Dijkstra", p, BUCKET_SIZE, None, None)
            stats[p] = stat
            # print(stat)
        all_stats[graph_name]["stats"] = stats

        header = ["priority", "avg_CT", "avg_SS", "avg_rel"]
        filename = getFileExpPath(1, graph_name + "_exp1.csv")
        IO.writeDictDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, getFileExpPath(1, "exp1_all_stats.json"))


def experiment2(graphs_names):
    """
    Experiment 2 : test which heuristic gives fastest A*
    - Euclidean
    - Manhattan
    - Octile
    """
    print("EXPERIMENT 2 : which heuristic A*")
    all_stats = {}
    for graph_name in graphs_names:
        print("GRAPH : ", graph_name)

        p = OSMgraphParser(graph_name)
        graph = p.parse()

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(),
                                 "nb_edges": graph.getNbEdges(),
                                 "avg_deg": graph.getAvgDegree()}

        # Benchmark
        b = Benchmark(graph)

        stats = {"euclidean": None, "manhattan": None, "octile": None}
        for h in stats.keys():
            print("Heuristic : ", h)
            stat = b.testSingleQuery(NB_RUNS, "A*", "bin", BUCKET_SIZE, h, None)
            stats[h] = stat
            # print(stat)
        all_stats[graph_name]["stats"] = stats

        header = ["heuristic", "avg_CT", "avg_SS", "avg_rel"]
        filename = getFileExpPath(2, graph_name + "_exp2.csv")
        IO.writeDictDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, getFileExpPath(2, "exp2_all_stats.json"))


def experiment3(graphs_names):
    """
    Experiment 3 : test which landmark selection gives fastest ALT
    - Random
    - Farthest
    - Planar
    """
    print("EXPERIMENT 3 : which landmark selection ALT")
    all_stats = {}
    for graph_name in graphs_names:
        print("GRAPH : ", graph_name)

        p = OSMgraphParser(graph_name)
        graph = p.parse()

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(),
                                 "nb_edges": graph.getNbEdges(),
                                 "avg_deg": graph.getAvgDegree()}

        # Benchmark
        b = Benchmark(graph)

        stats = {"random": None, "farthest": None, "planar": None}
        for ls in stats.keys():
            print("Landmark selection : ", ls)
            pre_timer = Timer()
            pre_timer.start()
            alt_pre = ALTpreprocessing(graph, ls, None, NB_LANDMARKS)
            lm_dists = alt_pre.getLmDistances()
            pre_timer.stop()
            pre_timer.printTimeElapsedMin("lm dists")

            stat = b.testSingleQuery(NB_RUNS, "ALT", "bin", BUCKET_SIZE, "euclidean", lm_dists)
            stat["lm_dists_CT"] = pre_timer.getTimeElapsedSec()
            stats[ls] = stat
            # print(stat)
        all_stats[graph_name]["stats"] = stats

        header = ["landmark_selection", "avg_CT", "avg_SS", "avg_rel", "lm_dists_CT"]
        filename = getFileExpPath(3, graph_name + "_exp3.csv")
        IO.writeDictDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, getFileExpPath(3, "exp3_all_stats.json"))


def experiment4(graphs_names):
    """
    Experiment 4 : test which nb of landmarks (k) gives fastest ALT
    => test with 1, 2, 4, 8, 16 and 21 landmarks
    difficult to have the optimal k => NP-hard problem
    """
    print("EXPERIMENT 4 : how many landmarks ALT")
    all_stats = {}
    for graph_name in graphs_names:
        print("GRAPH : ", graph_name)

        p = OSMgraphParser(graph_name)
        graph = p.parse()

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(),
                                 "nb_edges": graph.getNbEdges(),
                                 "avg_deg": graph.getAvgDegree()}

        # Benchmark
        b = Benchmark(graph)

        stats = {1: None, 2: None, 4: None, 8: None, 16: None, 32: None}
        for nl in stats.keys():
            print("Number of Landmarks : {0}, selection: {1}".format(nl, LANDMARK_SELECTION))
            pre_timer = Timer()
            pre_timer.start()
            alt_pre = ALTpreprocessing(graph, LANDMARK_SELECTION, None, nl)
            lm_dists = alt_pre.getLmDistances()
            pre_timer.stop()
            pre_timer.printTimeElapsedMin("lm dists")

            stat = b.testSingleQuery(NB_RUNS, "ALT", "bin", BUCKET_SIZE, "euclidean", lm_dists)
            stat["lm_dists_CT"] = pre_timer.getTimeElapsedSec()
            stats[nl] = stat
            # print(stat)
        all_stats[graph_name]["stats"] = stats

        header = ["nb_landmark", "avg_CT", "avg_SS", "avg_rel", "lm_dists_CT"]
        filename = getFileExpPath(4, graph_name + "_exp4.csv")
        IO.writeDictDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, getFileExpPath(4, "exp4_all_stats.json"))


def experiment5(graphs_names):
    """
    Experiment 5 : Single modal car network
    query benchmarks for a given graph for multiple algorithms
    """
    print("EXPERIMENT 5 : Single modal car network query benchmarks for a given graph for multiple algo")
    all_stats = {}
    for graph_name in graphs_names:
        print("GRAPH : ", graph_name)

        p = OSMgraphParser(graph_name)
        graph = p.parse()

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(),
                                 "nb_edges": graph.getNbEdges(),
                                 "avg_deg": graph.getAvgDegree()}

        # Benchmark
        b = Benchmark(graph)
        pre_timer = Timer()
        pre_timer.start()
        alt_pre = ALTpreprocessing(graph, LANDMARK_SELECTION, None, NB_LANDMARKS)
        lm_dists = alt_pre.getLmDistances()
        pre_timer.stop()
        pre_timer.printTimeElapsedMin("lm dists")

        algos = ["Dijkstra", "A*", "ALT", "BidiDijkstra", "BidiAstar", "BidiALT"]
        print("running algos... : " + " - ".join(algos))
        prepro_time = pre_timer.getTimeElapsedSec()
        stats = b.testMultipleQueries(NB_RUNS, graph, algos, lm_dists, prepro_time)
        # print(stats)

        all_stats[graph_name]["stats"] = stats

        header = ["algo", "avg_CT", "avg_SS", "avg_rel", "lm_dists_CT"]
        filename = getFileExpPath(5, graph_name + "_exp5.csv")
        IO.writeDictDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, getFileExpPath(5, "exp5_all_stats.json"))


def experiment6(graphs_names):
    """
    Experiment 6 : Single modal car network
    Preprocessing benchmarks
    ()
    """
    print("EXPERIMENT 6 : Single modal car network, preprocessing benchmarks")
    all_stats = {}
    for graph_name in graphs_names:
        print("GRAPH : ", graph_name)

        p = OSMgraphParser(graph_name)
        graph = p.parse()

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(),
                                 "nb_edges": graph.getNbEdges(),
                                 "avg_deg": graph.getAvgDegree()}

        # Benchmark
        b = Benchmark(graph)
        stat = b.testPreprocessing(LANDMARK_SELECTION, NB_LANDMARKS)

        print(stat["Prepro_time"], " seconds")
        header = ["landmark_selection", "nb_landmarks", "prepro_CT"]
        stats = [LANDMARK_SELECTION, NB_LANDMARKS, stat["Prepro_time"]]

        all_stats[graph_name]["stats"] = stats
        filename = getFileExpPath(6, graph_name + "_exp6.csv")
        IO.writeSingleRowStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, getFileExpPath(6, "exp6_all_stats.json"))


def experiment7(graphs_names):
    """
    Experiment 7 : Multi-modal public transport network
    """
    print("EXPERIMENT 7 : Multi-modal public transport network : Dijkstra & ALT")
    all_stats = {}
    for graph_name in graphs_names:
        print("GRAPH : ", graph_name)

        p = OSMgraphParser(graph_name)
        graph = p.parse("foot")
        print("nb edges before experiments : ", graph.getNbEdges())

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(),
                                 "nb_edges": graph.getNbEdges(),
                                 "avg_deg": graph.getAvgDegree()}

        nb_added_edges = [0, 10, 50, 100, 200]  # TODO : change nb (200) to be 1.1% of the graph size
        speed_limits = [0.1, 15, 30, 90, 120, 1e10]

        stats = {}

        nb_exp = 0
        for s in speed_limits:
            for n in nb_added_edges:
                print("==> nb added edges : {0}, speed limit : {1}".format(n, s))
                nodes_coords = deepcopy(graph.getNodesCoords())
                adjlist = deepcopy(graph.getAdjList())
                multi_graph = MultiModalGraph(nodes_coords, adjlist)
                multi_graph.addPublicTransportEdges(n, s)
                print("nb edges after added lines = ", multi_graph.getNbEdges())

                # Benchmark
                b = Benchmark(multi_graph)
                pre_timer = Timer()
                pre_timer.start()
                alt_pre = ALTpreprocessing(multi_graph, "planar", None, 16)
                lm_dists = alt_pre.getLmDistances()
                pre_timer.stop()
                prepro_time = pre_timer.getTimeElapsedSec()
                algos = ["Dijkstra", "ALT"]
                stat = b.testMultipleQueriesMultiModal(NB_RUNS, multi_graph, algos, lm_dists, prepro_time)

                stats[nb_exp] = [s, n] + list(stat["Dijkstra"].values()) + list(stat["ALT"].values())
                # print("Stats : ", stats[nb_exp])

                all_stats[graph_name][nb_exp] = {"nb_edges_after": multi_graph.getNbEdges(),
                                                 "avg_degree_after": multi_graph.getAvgDegree(),
                                                 "speed_limit": s,
                                                 "nb_added_edges": n,
                                                 "Dijkstra": stat["Dijkstra"],
                                                 "ALT": stat["ALT"]}
                nb_exp += 1

        header = ["speed_limit", "nb_added_edges", "D_avg_CT", "D_avg_SS", "D_avg_rel",
                  "ALT_avg_CT", "ALT_avg_SS", "ALT_avg_rel", "lm_dists_CT"]
        filename = getFileExpPath(7, graph_name + "_exp7.csv")
        IO.writeDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, getFileExpPath(7, "exp7_all_stats.json"))


def experiment8(graphs_names, show):
    """
    Experiment 8 : Multi-modal villo-station-based network
    """
    print("EXPERIMENT 8 : Multi-modal villo-station-based network : Dijkstra & ALT")
    all_stats = {}
    for graph_name in graphs_names:
        print("GRAPH : ", graph_name)

        p = OSMgraphParser(graph_name)
        graph = p.parse("foot")

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(),
                                 "nb_edges": graph.getNbEdges(),
                                 "avg_deg": graph.getAvgDegree()}

        multi_graph, villo_closests = addVilloStations(graph, show)

        all_stats[graph_name]["nb_nodes_after"] = multi_graph.getNbNodes()
        all_stats[graph_name]["nb_edges_after"] = multi_graph.getNbEdges()
        all_stats[graph_name]["avg_deg_after"] = multi_graph.getAvgDegree()

        # Benchmark
        b = Benchmark(multi_graph)
        pre_timer = Timer()
        pre_timer.start()
        alt_pre = ALTpreprocessing(multi_graph, LANDMARK_SELECTION, None, NB_LANDMARKS)
        lm_dists = alt_pre.getLmDistances()
        pre_timer.stop()
        pre_timer.printTimeElapsedMin("lm dists")
        prepro_time = pre_timer.getTimeElapsedSec()
        algos = ["Dijkstra", "ALT"]
        stats = b.testMultipleQueriesMultiModal(NB_RUNS, multi_graph, algos, lm_dists, prepro_time)

        # print(stats)
        header = ["algo", "avg_CT", "avg_SS", "avg_rel", "lm_dists_CT", "nb_villo_stations"]
        stats["Dijkstra"]["nb_villo_stations"] = len(villo_closests)
        stats["ALT"]["nb_villo_stations"] = len(villo_closests)

        all_stats[graph_name]["stats"] = stats
        filename = getFileExpPath(8, graph_name + "_exp8.csv")
        IO.writeDictDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, getFileExpPath(8, "exp8_all_stats.json"))


def getPref(fixed_pref, x):
    if fixed_pref == 1:
        return [1, x]
    elif fixed_pref == 2:
        return [x, 1]


def experiment9(graphs_names, fixed_pref, pref_range, step):
    """
    Experiment 9 :
    Multi modal station-based graph with : car & villo
    Simple queries with weighted summed edge weights (2 metrics)
    => Preprocessing without pref (= same pref for both modalities), then query with pref
    => PROBLEM : ca va pas prendre en compte les nouveaux nodes ajoutés des stations villo !!
    => instead : faire un prepro avec les prefs identiques, mais avec les stations
    TODO : apres le preprocessing pref[1,1], faire des queries avec prefs[1,x], x=1=>X, puis prefs[x,1]
    """
    print("EXPERIMENT 9 : Multi-modal station-based graph with personal car and villo bike : Dijkstra & ALT")
    all_stats = {}
    for graph_name in graphs_names:
        print("GRAPH : ", graph_name)

        p = OSMgraphParser(graph_name)
        graph = p.parse("car")

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(),
                                 "nb_edges": graph.getNbEdges(),
                                 "avg_deg": graph.getAvgDegree()}

        base_multi_graph, villo_closests = addVilloStations(graph)
        simple_multi_graph = copy.deepcopy(base_multi_graph)
        simple_multi_graph.toWeightedSum([1, 1])

        all_stats[graph_name]["nb_nodes_after"] = simple_multi_graph.getNbNodes()
        all_stats[graph_name]["nb_edges_after"] = simple_multi_graph.getNbEdges()
        all_stats[graph_name]["avg_deg_after"] = simple_multi_graph.getAvgDegree()

        nb = 0
        all_stats[graph_name]["stats"] = {}
        stats = {}

        x = pref_range[0]
        while x >= pref_range[1]:
            # for x in range(pref_range[0], pref_range[1], step):
            prefs = getPref(fixed_pref, x)

            # preprocessing with same pref for both modalities
            pre_timer = Timer()
            pre_timer.start()
            alt_pre = ALTpreprocessing(simple_multi_graph, LANDMARK_SELECTION, None, NB_LANDMARKS)
            lm_dists = alt_pre.getLmDistances()
            pre_timer.stop()
            pre_timer.printTimeElapsedMin("lm dists")
            prepro_time = pre_timer.getTimeElapsedSec()

            multi_graph = copy.deepcopy(base_multi_graph)
            multi_graph.toWeightedSum(prefs)

            # Benchmark query with varying preferences
            b = Benchmark(multi_graph)
            algos = ["Dijkstra", "ALT"]
            stat = b.testMultipleQueriesMultiModal(NB_RUNS, multi_graph, algos, lm_dists, prepro_time)

            stats[nb] = prefs + list(stat["Dijkstra"].values()) + list(stat["ALT"].values())

            stat["Dijkstra"]["nb_villo_stations"] = len(villo_closests)
            stat["ALT"]["nb_villo_stations"] = len(villo_closests)

            all_stats[graph_name]["stats"][nb] = {"c1": prefs[0], "c2": prefs[1],
                                                  "Dijkstra": stat["Dijkstra"],
                                                  "ALT": stat["ALT"]}

            nb += 1
            x = round(x + step, 1)

        header = ["c1", "c2", "algo", "avg_CT", "avg_SS", "avg_rel",
                  "lm_dists_CT", "nb_villo_stations"]
        filename = getFileExpPath(9, graph_name + "_exp9.csv")
        # print(stats)
        IO.writeDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, getFileExpPath(9, "exp9_all_stats.json"))


def experiment10(graphs_names, fixed_pref, pref_range, step, worst_case):
    """
    Experiment 10 :
    Multi-modal villo-station-based graph :
    Preprocessing avec les pires users : le plus petit, et le plus grand
    puis query avec tout le range de preference
    => p-e séparer cette fonctioni en 2 ? Un avec le plus petit worst case et l'autre le plus grand
    """
    all_stats = {}
    for graph_name in graphs_names:
        print("GRAPH : ", graph_name)

        p = OSMgraphParser(graph_name)
        graph = p.parse("car")

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(),
                                 "nb_edges": graph.getNbEdges(),
                                 "avg_deg": graph.getAvgDegree()}

        base_multi_graph, villo_closests = addVilloStations(graph)
        simple_multi_graph = copy.deepcopy(base_multi_graph)
        simple_multi_graph.toWeightedSum(getPref(fixed_pref, pref_range[worst_case]))

        all_stats[graph_name]["nb_nodes_after"] = simple_multi_graph.getNbNodes()
        all_stats[graph_name]["nb_edges_after"] = simple_multi_graph.getNbEdges()
        all_stats[graph_name]["avg_deg_after"] = simple_multi_graph.getAvgDegree()

        nb = 0
        all_stats[graph_name]["stats"] = {}
        stats = {}

        x = pref_range[0]
        while x >= pref_range[1]:
            # for x in range(pref_range[0], pref_range[1], step):
            prefs = getPref(fixed_pref, x)

            # preprocessing with same pref for both modalities
            pre_timer = Timer()
            pre_timer.start()
            alt_pre = ALTpreprocessing(simple_multi_graph, LANDMARK_SELECTION, None, NB_LANDMARKS)
            lm_dists = alt_pre.getLmDistances()
            pre_timer.stop()
            pre_timer.printTimeElapsedMin("lm dists")
            prepro_time = pre_timer.getTimeElapsedSec()

            multi_graph = copy.deepcopy(base_multi_graph)
            multi_graph.toWeightedSum(prefs)

            # Benchmark query with varying preferences
            b = Benchmark(multi_graph)
            algos = ["Dijkstra", "ALT"]
            stat = b.testMultipleQueriesMultiModal(NB_RUNS, multi_graph, algos, lm_dists, prepro_time)

            stats[nb] = prefs + list(stat["Dijkstra"].values()) + list(stat["ALT"].values())

            stat["Dijkstra"]["nb_villo_stations"] = len(villo_closests)
            stat["ALT"]["nb_villo_stations"] = len(villo_closests)

            all_stats[graph_name]["stats"][nb] = {"c1": prefs[0], "c2": prefs[1],
                                                  "Dijkstra": stat["Dijkstra"],
                                                  "ALT": stat["ALT"]}

            nb += 1
            x = round(x + step, 1)

        header = ["c1", "c2", "algo", "avg_CT", "avg_SS", "avg_rel",
                  "lm_dists_CT", "nb_villo_stations"]
        filename = getFileExpPath(10, graph_name + "_exp10.csv")
        # print(stats)
        IO.writeDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, getFileExpPath(10, "exp10_all_stats.json"))


def experiment11():
    """
    Experiment 11 :
    Multi-modal villo-station-based graph :
    preprocessing (for ALT) WITH worst-case preferences then query with preferences
    TODO TOTEST
    # TODO : change nb runs to 1000 + use the 6 graphs
    """
    pass


def experiment12():
    """
    Experiment 12 :
    Multi-Labelling algorithm pareto optimal
    TODO TOTEST
    # TODO : change nb runs to 1000 + use the 6 graphs
    """
    print("EXPERIMENT 12 : Multi-Labelling algorithm pareto optimal multi-modal network")


# TODO : idea : vu qu'on sait que + le lower bound de d(v,t) est "tight", plus ALT performe bien,
# on peut prendre une mesure de ça: genre la différence entre le lowerbound et d(v,t) en moyenne


# =====================================================

def launchExperiment(exp):
    timer_all = Timer()
    timer_all.start()

    if exp == 1 or exp == -1:
        timer = Timer()
        # graphs_names = [GRAPH_ULB, GRAPH_BXL]
        graphs_names = GRAPHS
        timer.start()
        experiment1(graphs_names)
        timer.stop()
        timer.printTimeElapsedMin("Exp 1")
        print("==========================================================================")

    if exp == 2 or exp == -1:
        timer = Timer()
        timer.start()
        graphs_names = [GRAPH_ULB, GRAPH_BXL]
        # graphs_names = GRAPHS
        experiment2(graphs_names)
        timer.stop()
        timer.printTimeElapsedMin("Exp 2")
        print("==========================================================================")

    if exp == 3 or exp == -1:
        timer = Timer()
        timer.start()
        graphs_names = [GRAPH_ULB, GRAPH_BXL]
        # graphs_names = GRAPHS
        experiment3(graphs_names)
        timer.stop()
        timer.printTimeElapsedMin("Exp 3")
        print("==========================================================================")

    if exp == 4 or exp == -1:
        timer = Timer()
        timer.start()
        graphs_names = [GRAPH_ULB, GRAPH_BXL]
        # graphs_names = GRAPHS
        experiment4(graphs_names)
        timer.stop()
        timer.printTimeElapsedMin("Exp 4")
        print("==========================================================================")

    if exp == 5 or exp == -1:
        timer = Timer()
        timer.start()
        # graphs_names = [GRAPH_ULB, GRAPH_BXL]
        graphs_names = GRAPHS
        experiment5(graphs_names)
        timer.stop()
        timer.printTimeElapsedMin("Exp 5")
        print("==========================================================================")

    if exp == 6 or exp == -1:
        timer = Timer()
        timer.start()
        # graphs_names = [GRAPH_ULB, GRAPH_BXL]
        graphs_names = GRAPHS
        experiment6(graphs_names)
        timer.stop()
        timer.printTimeElapsedMin("Exp 6")
        print("==========================================================================")

    if exp == 7 or exp == -1:
        timer = Timer()
        timer.start()
        graphs_names = [GRAPH_ULB]
        # graphs_names = [GRAPH_BXL_CAP]
        experiment7(graphs_names)
        timer.stop()
        timer.printTimeElapsedMin("Exp 7")
        print("==========================================================================")

    if exp == 8 or exp == -1:
        timer = Timer()
        timer.start()
        # graphs_names = [GRAPH_ULB, GRAPH_BXL]
        graphs_names = [GRAPH_BXL_CAP]
        experiment8(graphs_names, show=False)
        timer.stop()
        timer.printTimeElapsedMin("Exp 8")
        print("==========================================================================")

    if exp == 9 or exp == -1:
        timer = Timer()
        timer.start()
        # graphs_names = [GRAPH_ULB]
        graphs_names = [GRAPH_BXL_CAP]
        experiment9(graphs_names, 1, [2, 0], -0.2)
        timer.stop()
        timer.printTimeElapsedMin("Exp 9")
        print("==========================================================================")

    if exp == 10 or exp == -1:
        timer = Timer()
        timer.start()
        # graphs_names = [GRAPH_ULB]
        graphs_names = [GRAPH_BXL_CAP]
        experiment10(graphs_names, 1, [2, 0], -0.2, 0)
        timer.stop()
        timer.printTimeElapsedMin("Exp 10")
        print("==========================================================================")

    timer_all.stop()
    timer_all.printTimeElapsedMin("All experiments")



def testRandomPairs():
    p = OSMgraphParser(GRAPH_ULB)
    graph = p.parse("car")

    multi_graph, villo_closests = addVilloStations(graph)
    prefs = [1, 1]
    multi_graph.toWeightedSum(prefs)

    for i in range(30):
        s, t = Random.selectRandomPair(multi_graph.getNodesIDs())
        print(s, t)


def showVilloStations(graph_name):
    p = OSMgraphParser(graph_name)
    graph = p.parse("foot")

    multi_graph, villo_closests = addVilloStations(graph, True)


def main():
    launchExperiment(EXPERIMENT)

    # launchAllExperiments()

    # testRandomPairs()

    # showVilloStations(GRAPH_BXL_CAP)


if __name__ == "__main__":
    main()
