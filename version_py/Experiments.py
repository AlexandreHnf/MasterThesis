from Benchmark import *
from MultiModalGraph import *
from ParseOSMgraph import OSMgraphParser
from copy import deepcopy
from Quadtree import showVilloStations
import Writer

def experiment1():
    """
    Experiment 1 : test which queue type gives fastest Dijkstra
    - List (list)
    - Binary Heap (bin)
    - Fibonacci Heap (fib)
    # TODO : change nb runs to 1000 + use the 6 graphs
    """
    print("EXPERIMENT 1 : which priority queue Dijkstra")
    p = OSMgraphParser(GRAPH)
    graph = p.parse()

    b = Benchmark(graph)

    all_stats = {"bin": None, "fib": None, "list": None}
    for p in all_stats.keys():
        print("Priority : ", p)
        stats = b.testSingleQuery(NB_RUNS, "Dijkstra", p, BUCKET_SIZE, None, None)
        all_stats[p] = stats
        print(stats)

    header = ["priority", "avg_CT", "avg_SS", "avg_rel"]
    Writer.writeExp1StatsToCsv(all_stats, header, FILENAME_EXP1)


def experiment2():
    """
    Experiment 2 : test which heuristic gives fastest A*
    - Euclidean
    - Manhattan
    - Octile
    # TODO : change nb runs to 1000 + use the 6 graphs
    """
    # TODO check if the results are coherent
    print("EXPERIMENT 2 : which heuristic A*")
    p = OSMgraphParser(GRAPH)
    graph = p.parse()

    b = Benchmark(graph)

    all_stats = {"euclidean": None, "manhattan": None, "octile": None}
    for h in all_stats.keys():
        print("Heuristic : ", h)
        stats = b.testSingleQuery(NB_RUNS, "A*", "bin", BUCKET_SIZE, h, None)
        all_stats[h] = stats
        print(stats)

    header = ["heuristic", "avg_CT", "avg_SS", "avg_rel"]
    Writer.writeExp1StatsToCsv(all_stats, header, FILENAME_EXP2)

def experiment3():
    """
    Experiment 3 : test which landmark selection gives fastest ALT
    - Random
    - Farthest
    - Planar
    # TODO : change nb runs to 1000 + use the 6 graphs
    """
    # TODO check if the results are coherent
    print("EXPERIMENT 3 : which landmark selection ALT")
    p = OSMgraphParser(GRAPH)
    graph = p.parse()

    b = Benchmark(graph)

    all_stats = {"random": None, "farthest": None, "planar": None}
    for ls in all_stats.keys():
        print("Landmark selection : ", ls)
        pre_timer = Timer()
        alt_pre = ALTpreprocessing(graph, ls, None, NB_LANDMARKS)
        lm_dists = alt_pre.getLmDistances()
        pre_timer.end_timer()
        pre_timer.printTimeElapsedMin("lm dists")

        stats = b.testSingleQuery(NB_RUNS, "ALT", "bin", BUCKET_SIZE, "euclidean", lm_dists)
        stats["lm_dists_CT"] = pre_timer.getTimeElapsedSec()
        all_stats[ls] = stats
        print(stats)

    header = ["landmark_selection", "avg_CT", "avg_SS", "avg_rel", "lm_dists_CT"]
    Writer.writeExp1StatsToCsv(all_stats, header, FILENAME_EXP3)


def experiment4():
    """
    Experiment 4 : test which nb of landmarks (k) gives fastest ALT
    # TODO : change nb runs to 1000 + use the 6 graphs
    """
    pass
    # maybe to difficult => NP-hard problem
    # TODO check if the results are coherent with plots
    print("EXPERIMENT 4 : how many landmarks ALT")
    # test with 1, 2, 4, 8, 16 and 21 landmarks
    p = OSMgraphParser(GRAPH)
    graph = p.parse()

    b = Benchmark(graph)

    nb_landmarks = [1, 2, 4, 8, 16, 32]
    all_stats = {1: None, 2: None, 4: None, 8: None, 16: None, 32: None}
    for nl in all_stats.keys():
        print("Number of Landmarks : ", nl)
        pre_timer = Timer()
        alt_pre = ALTpreprocessing(graph, LANDMARK_SELECTION, None, nl)
        lm_dists = alt_pre.getLmDistances()
        pre_timer.end_timer()
        pre_timer.printTimeElapsedMin("lm dists")

        stats = b.testSingleQuery(NB_RUNS, "ALT", "bin", BUCKET_SIZE, "euclidean", lm_dists)
        stats["lm_dists_CT"] = pre_timer.getTimeElapsedSec()
        all_stats[nl] = stats
        print(stats)

    header = ["nb_landmark", "avg_CT", "avg_SS", "avg_rel", "lm_dists_CT"]
    Writer.writeExp1StatsToCsv(all_stats, header, FILENAME_EXP4)

def experiment5():
    """
    Experiment 5 : Single modal car network
    query benchmarks for a given graph for multiple algorithms
    TODO check if the results are coherent (with the plots)
    # TODO : change nb runs to 1000 + use the 6 graphs
    """
    print("EXPERIMENT 5 : Single modal car network query benchmarks for a given graph for multiple algo")
    p = OSMgraphParser(GRAPH)
    graph = p.parse()

    b = Benchmark(graph)

    alt_pre = ALTpreprocessing(graph, LANDMARK_SELECTION, None, NB_LANDMARKS)
    lm_dists = alt_pre.getLmDistances()
    print("ready (preprocessing done)")

    algos = ["Dijkstra", "A*", "ALT", "BidiDijkstra", "BidiAstar", "BidiALT"]

    stats = b.testMultipleQueries(NB_RUNS, graph, algos, lm_dists)
    # TODO : write to file
    print(stats)


def experiment6():
    """
    Experiment 6 : Single modal car network
    Preprocessing benchmarks
    TODO check if the results are coherent (plot the qtree ?)
    # TODO : change nb experiments to 1000 + use the 6 graphs
    """
    print("EXPERIMENT 6 : Single modal car network, preprocessing benchmarks")
    p = OSMgraphParser(GRAPH)
    graph = p.parse()

    b = Benchmark(graph)
    stats = b.testPreprocessing(LANDMARK_SELECTION, NB_LANDMARKS)

    print(stats["Prepro_time"], " seconds")
    # TODO : write to file


def experiment7():
    """
    Experiment 7 : Multi-modal public transport network
    TODO check if the results are coherent (with plots)
    # TODO : change nb runs to 1000 + use the 6 graphs
    """
    print("EXPERIMENT 7 : Multi-modal public transport network : Dijkstra & ALT")
    p = OSMgraphParser(GRAPH)
    graph = p.parse("foot")
    print("nb edges before experiments : ", graph.getNbEdges())

    nb_added_edges = [0, 10, 50, 100, 200]  # TODO : change nb (200) to be 1.1% of the graph size
    speed_limits = [0.1, 15, 30, 90, 120, 1e10]

    for s in speed_limits:
        for n in nb_added_edges:
            print("==> nb added edges : {0}, speed limit : {1}".format(n, s))
            nodes_coords = deepcopy(graph.getNodesCoords())
            adjlist = deepcopy(graph.getAdjList())
            multi_graph = MultiModalGraph(nodes_coords, adjlist)
            multi_graph.addPublicTransportEdges(n, s)
            print("nb edges after added lines = ", multi_graph.getNbEdges())

            b = Benchmark(multi_graph)
            alt_pre = ALTpreprocessing(multi_graph, "planar", None, 16)
            lm_dists = alt_pre.getLmDistances()
            algos = {"Dijkstra": Dijkstra(multi_graph, -1, -1, "bin"), "ALT": ALT(multi_graph, -1, -1, lm_dists, "bin")}
            stats = b.testMultipleQueries(NB_RUNS, multi_graph, algos, lm_dists)

            print("Stats : ", stats)


def experiment8():
    """
    Experiment 8 : Multi-modal station-based network
    TODO TOTEST
    # TODO : change nb runs to 1000 + use the 6 graphs
    """
    print("EXPERIMENT 8 : Multi-modal station-based network : Dijkstra & ALT")
    p = OSMgraphParser(GRAPH)
    graph = p.parse("foot")

    villo_coords = OSMgraphParser.getVilloNodes()
    # print(villo_coords)

    showVilloStations(graph.getQtree(), graph.getNodesCoords(), villo_coords, False)

    # get Villo stations nodes in the graph
    villo_closests = []
    for coord in villo_coords:
        closest = graph.findClosestNode(coord)
        if closest:
            villo_closests.append(closest)

    # transform the graph into a multi-modal foot-villo graph
    nodes_coords = deepcopy(graph.getNodesCoords())
    adjlist = deepcopy(graph.getAdjList())
    multi_graph = MultiModalGraph(nodes_coords, adjlist)
    print(villo_closests)
    print("BEFORE : {0} nodes, {1} edges".format(graph.getNbNodes(), graph.getNbEdges()))
    multi_graph.toStationBased(villo_closests)
    print("AFTER : {0} nodes, {1} edges".format(multi_graph.getNbNodes(), multi_graph.getNbEdges()))

    b = Benchmark(multi_graph)
    pre_timer = Timer()
    alt_pre = ALTpreprocessing(multi_graph, "planar", None, 16)
    lm_dists = alt_pre.getLmDistances()
    pre_timer.end_timer()
    pre_timer.printTimeElapsedMin("lm dists")  #TODO : save this time in the csv
    algos = {"Dijkstra": Dijkstra(multi_graph, -1, -1, "bin"), "ALT": ALT(multi_graph, -1, -1, lm_dists, "bin")}
    stats = b.testMultipleQueries(NB_RUNS, multi_graph, algos, lm_dists)

    print(stats)


def experiment9():
    """
    Experiment 9 :
    Multi modal with : personal car and personal bike ? => pb of coherence mmmh
    TODO TOTEST
    # TODO : change nb runs to 1000 + use the 6 graphs
    """
    print("EXPERIMENT 9 : Multi-modal with personal car and personal bike : Dijkstra & ALT")
    pass


def experiment10():
    """
    Experiment 10 :
    Multi-Labelling algorithm pareto optimal
    TODO TOTEST
    # TODO : change nb runs to 1000 + use the 6 graphs
    """
    print("EXPERIMENT 10 : Multi-Labelling algorithm pareto optimal multi-modal network")


# =====================================================

def launchExperiment():
    if EXPERIMENT == 1:
        experiment1()
    elif EXPERIMENT == 2:
        experiment2()
    elif EXPERIMENT == 3:
        experiment3()
    elif EXPERIMENT == 4:
        experiment4()
    elif EXPERIMENT == 5:
        experiment5()
    elif EXPERIMENT == 6:
        experiment6()
    elif EXPERIMENT == 7:
        experiment7()
    elif EXPERIMENT == 8:
        experiment8()
    elif EXPERIMENT == 9:
        experiment9()
    elif EXPERIMENT == 10:
        experiment10()

def main():
    launchExperiment()
    #TODO : faire une fonction qui lance tous les experiments a la suite


if __name__ == "__main__":
    main()
