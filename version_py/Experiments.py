from Benchmark import *
from MultiModalGraph import *
from ParseOSMgraph import OSMgraphParser
from copy import deepcopy
import IO


def experiment1(graphs_names):
    """
    Experiment 1 : test which queue type gives fastest Dijkstra
    - List (list)
    - Binary Heap (bin)
    - Fibonacci Heap (fib)
    TODO : change nb runs to 1000 + use the 6 graphs
    """
    print("EXPERIMENT 1 : which priority queue Dijkstra")
    all_stats = {}
    for graph_name in graphs_names:
        print("GRAPH : ", graph_name)

        p = OSMgraphParser(GRAPH_FILENAMES[graph_name])
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
            print(stat)
        all_stats[graph_name]["stats"] = stats

        header = ["priority", "avg_CT", "avg_SS", "avg_rel"]
        filename = FILE_EXP1 + graph_name + "_exp1.csv"
        IO.writeDictDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, FILE_EXP1_ALL)


def experiment2(graphs_names):
    """
    Experiment 2 : test which heuristic gives fastest A*
    - Euclidean
    - Manhattan
    - Octile
    TODO : change nb runs to 1000 + use the 6 graphs
    TODO check if the results are coherent
    """
    print("EXPERIMENT 2 : which heuristic A*")
    all_stats = {}
    for graph_name in graphs_names:
        p = OSMgraphParser(GRAPH_FILENAMES[graph_name])
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
            print(stat)
        all_stats[graph_name]["stats"] = stats

        header = ["heuristic", "avg_CT", "avg_SS", "avg_rel"]
        filename = FILE_EXP2 + graph_name + "_exp2.csv"
        IO.writeDictDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, FILE_EXP2_ALL)


def experiment3(graphs_names):
    """
    Experiment 3 : test which landmark selection gives fastest ALT
    - Random
    - Farthest
    - Planar
    TODO : change nb runs to 1000 + use the 6 graphs
    TODO check if the results are coherent
    """
    print("EXPERIMENT 3 : which landmark selection ALT")
    all_stats = {}
    for graph_name in graphs_names:
        p = OSMgraphParser(GRAPH_FILENAMES[graph_name])
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
            alt_pre = ALTpreprocessing(graph, ls, None, NB_LANDMARKS)
            lm_dists = alt_pre.getLmDistances()
            pre_timer.end_timer()
            pre_timer.printTimeElapsedMin("lm dists")

            stat = b.testSingleQuery(NB_RUNS, "ALT", "bin", BUCKET_SIZE, "euclidean", lm_dists)
            stat["lm_dists_CT"] = pre_timer.getTimeElapsedSec()
            stats[ls] = stat
            print(stat)
        all_stats[graph_name]["stats"] = stats

        header = ["landmark_selection", "avg_CT", "avg_SS", "avg_rel", "lm_dists_CT"]
        filename = FILE_EXP3 + graph_name + "_exp3.csv"
        IO.writeDictDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, FILE_EXP3_ALL)


def experiment4(graphs_names):
    """
    Experiment 4 : test which nb of landmarks (k) gives fastest ALT
    => test with 1, 2, 4, 8, 16 and 21 landmarks
    difficult to have the optimal k => NP-hard problem
    TODO : change nb runs to 1000 + use the 6 graphs
    TODO check if the results are coherent with plots
    """
    print("EXPERIMENT 4 : how many landmarks ALT")
    all_stats = {}
    for graph_name in graphs_names:
        p = OSMgraphParser(GRAPH_FILENAMES[graph_name])
        graph = p.parse()

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(),
                                 "nb_edges": graph.getNbEdges(),
                                 "avg_deg": graph.getAvgDegree()}

        # Benchmark
        b = Benchmark(graph)

        stats = {1: None, 2: None, 4: None, 8: None, 16: None, 32: None}
        for nl in stats.keys():
            print(f"Number of Landmarks : {nl}, selection : {LANDMARK_SELECTION}")
            pre_timer = Timer()
            alt_pre = ALTpreprocessing(graph, LANDMARK_SELECTION, None, nl)
            lm_dists = alt_pre.getLmDistances()
            pre_timer.end_timer()
            pre_timer.printTimeElapsedMin("lm dists")

            stat = b.testSingleQuery(NB_RUNS, "ALT", "bin", BUCKET_SIZE, "euclidean", lm_dists)
            stat["lm_dists_CT"] = pre_timer.getTimeElapsedSec()
            stats[nl] = stat
            print(stat)
        all_stats[graph_name]["stats"] = stats

        header = ["nb_landmark", "avg_CT", "avg_SS", "avg_rel", "lm_dists_CT"]
        filename = FILE_EXP4 + graph_name + "_exp4.csv"
        IO.writeDictDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, FILE_EXP4_ALL)


def experiment5(graphs_names):
    """
    Experiment 5 : Single modal car network
    query benchmarks for a given graph for multiple algorithms
    TODO check if the results are coherent (with the plots)
    TODO : change nb runs to 1000 + use the 6 graphs
    """
    print("EXPERIMENT 5 : Single modal car network query benchmarks for a given graph for multiple algo")
    all_stats = {}
    for graph_name in graphs_names:
        p = OSMgraphParser(GRAPH_FILENAMES[graph_name])
        graph = p.parse()

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(),
                                 "nb_edges": graph.getNbEdges(),
                                 "avg_deg": graph.getAvgDegree()}

        # Benchmark
        b = Benchmark(graph)
        pre_timer = Timer()
        alt_pre = ALTpreprocessing(graph, LANDMARK_SELECTION, None, NB_LANDMARKS)
        lm_dists = alt_pre.getLmDistances()
        pre_timer.end_timer()
        pre_timer.printTimeElapsedMin("lm dists")

        algos = ["Dijkstra", "A*", "ALT", "BidiDijkstra", "BidiAstar", "BidiALT"]

        prepro_time = pre_timer.getTimeElapsedSec()
        stats = b.testMultipleQueries(NB_RUNS, graph, algos, lm_dists, prepro_time)
        print(stats)

        all_stats[graph_name]["stats"] = stats

        header = ["algo", "avg_CT", "avg_SS", "avg_rel", "lm_dists_CT"]
        filename = FILE_EXP5 + graph_name + "_exp5.csv"
        IO.writeDictDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, FILE_EXP5_ALL)

def experiment6(graphs_names):
    """
    Experiment 6 : Single modal car network
    Preprocessing benchmarks
    TODO check if the results are coherent (plot the qtree ?)
    TODO : change nb experiments to 1000 + use the 6 graphs
    TODO : change this experiment, with different parameters for preprocessing
    """
    print("EXPERIMENT 6 : Single modal car network, preprocessing benchmarks")
    all_stats = {}
    for graph_name in graphs_names:
        p = OSMgraphParser(GRAPH_FILENAMES[graph_name])
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
        filename = FILE_EXP6 + graph_name + "_exp6.csv"
        IO.writeSingleRowStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, FILE_EXP6_ALL)


def experiment7(graphs_names):
    """
    Experiment 7 : Multi-modal public transport network
    TODO check if the results are coherent (with plots)
    TODO : change nb runs to 1000 + use the 6 graphs
    """
    print("EXPERIMENT 7 : Multi-modal public transport network : Dijkstra & ALT")
    all_stats = {}
    for graph_name in graphs_names:
        p = OSMgraphParser(GRAPH_FILENAMES[graph_name])
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
                alt_pre = ALTpreprocessing(multi_graph, "planar", None, 16)
                lm_dists = alt_pre.getLmDistances()
                pre_timer.end_timer()
                prepro_time = pre_timer.getTimeElapsedSec()
                algos = ["Dijkstra", "ALT"]
                stat = b.testMultipleQueries(NB_RUNS, multi_graph, algos, lm_dists, prepro_time)

                stats[nb_exp] = [s, n] + list(stat["Dijkstra"].values()) + list(stat["ALT"].values())
                print("Stats : ", stats[nb_exp])

                all_stats[graph_name][nb_exp] = {"nb_edges_after": multi_graph.getNbEdges(),
                                                 "avg_degree_after": multi_graph.getAvgDegree(),
                                                  "speed_limit": s,
                                                  "nb_added_edges": n,
                                                  "Dijkstra": stat["Dijkstra"],
                                                  "ALT": stat["ALT"]}
                nb_exp += 1

        header = ["speed_limit", "nb_added_edges", "D_avg_CT", "D_avg_SS", "D_avg_rel",
                  "ALT_avg_CT", "ALT_avg_SS", "ALT_avg_rel", "lm_dists_CT"]
        filename = FILE_EXP7 + graph_name + "_exp7.csv"
        IO.writeDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, FILE_EXP7_ALL)


def experiment8(graphs_names):
    """
    Experiment 8 : Multi-modal villo-station-based network
    TODO check if the results are coherent (with graph)
    TODO : change nb runs to 1000 + use the 6 graphs
    """
    print("EXPERIMENT 8 : Multi-modal villo-station-based network : Dijkstra & ALT")
    all_stats = {}
    for graph_name in graphs_names:
        p = OSMgraphParser(GRAPH_FILENAMES[graph_name])
        graph = p.parse("foot")

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(),
                                 "nb_edges": graph.getNbEdges(),
                                 "avg_deg": graph.getAvgDegree()}

        multi_graph, villo_closests = addVilloStations(graph)

        all_stats[graph_name]["nb_nodes_after"] = multi_graph.getNbNodes()
        all_stats[graph_name]["nb_edges_after"] = multi_graph.getNbEdges()
        all_stats[graph_name]["avg_deg_after"] = multi_graph.getAvgDegree()

        # Benchmark
        b = Benchmark(multi_graph)
        pre_timer = Timer()
        alt_pre = ALTpreprocessing(multi_graph, "planar", None, 16)
        lm_dists = alt_pre.getLmDistances()
        pre_timer.end_timer()
        pre_timer.printTimeElapsedMin("lm dists")
        prepro_time = pre_timer.getTimeElapsedSec()
        algos = ["Dijkstra", "ALT"]
        stats = b.testMultipleQueries(NB_RUNS, multi_graph, algos, lm_dists, prepro_time)

        print(stats)
        header = ["algo", "avg_CT", "avg_SS", "avg_rel", "lm_dists_CT", "nb_villo_stations"]
        stats["Dijkstra"]["nb_villo_stations"] = len(villo_closests)
        stats["ALT"]["nb_villo_stations"] = len(villo_closests)

        all_stats[graph_name]["stats"] = stats
        filename = FILE_EXP8 + graph_name + "_exp8.csv"
        IO.writeDictDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, FILE_EXP8_ALL)


def experiment9(graphs_names):
    """
    Experiment 9 :
    Multi modal station-based graph with : car & villo
    Simple queries with weighted summed edge weights (2 metrics)
    TODO TOTEST
    # TODO : change nb runs to 1000 + use the 6 graphs
    """
    print("EXPERIMENT 9 : Multi-modal station-based graph with personal car and villo bike : Dijkstra & ALT")
    all_stats = {}
    for graph_name in graphs_names:
        p = OSMgraphParser(GRAPH_FILENAMES[graph_name])
        graph = p.parse("car")

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(),
                                 "nb_edges": graph.getNbEdges(),
                                 "avg_deg": graph.getAvgDegree()}

        multi_graph, villo_closests = addVilloStations(graph)
        prefs = [1,1]
        multi_graph.toWeightedSum(prefs)

        all_stats[graph_name]["nb_nodes_after"] = multi_graph.getNbNodes()
        all_stats[graph_name]["nb_edges_after"] = multi_graph.getNbEdges()
        all_stats[graph_name]["avg_deg_after"] = multi_graph.getAvgDegree()

        # Benchmark
        b = Benchmark(multi_graph)
        pre_timer = Timer()
        alt_pre = ALTpreprocessing(multi_graph, "planar", None, 16)
        lm_dists = alt_pre.getLmDistances()
        pre_timer.end_timer()
        pre_timer.printTimeElapsedMin("lm dists")
        prepro_time = pre_timer.getTimeElapsedSec()
        algos = ["Dijkstra", "ALT"]
        stats = b.testMultipleQueries(NB_RUNS, multi_graph, algos, lm_dists, prepro_time)

        print(stats)
        header = ["algo", "avg_CT", "avg_SS", "avg_rel", "lm_dists_CT", "nb_villo_stations"]
        stats["Dijkstra"]["nb_villo_stations"] = len(villo_closests)
        stats["ALT"]["nb_villo_stations"] = len(villo_closests)

        #TODO : add the stats : avg nb of bike edges & car edges in the shortest paths

        all_stats[graph_name]["stats"] = stats
        filename = FILE_EXP9 + graph_name + "_exp9.csv"
        IO.writeDictDictStatsToCsv(stats, header, filename)

    IO.dicToJson(all_stats, FILE_EXP9_ALL)


def experiment10():
    """
    Experiment 10 :
    Multi-modal villo-station-based graph :
    first preprocessing (for ALT) without preferences then query with preferences
    TODO TOTEST
    # TODO : change nb runs to 1000 + use the 6 graphs
    """
    pass


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


# =====================================================

def launchExperiment(exp):
    # TODO : put all the necessary graphs instead of just 1
    if exp == 1:
        graphs_names = [GRAPH_1_NAME]
        experiment1(graphs_names)

    elif exp == 2:
        graphs_names = [GRAPH_1_NAME]
        experiment2(graphs_names)

    elif exp == 3:
        graphs_names = [GRAPH_1_NAME]
        experiment3(graphs_names)

    elif exp == 4:
        graphs_names = [GRAPH_1_NAME]
        experiment4(graphs_names)

    elif exp == 5:
        graphs_names = [GRAPH_1_NAME]
        experiment5(graphs_names)

    elif exp == 6:
        graphs_names = [GRAPH_1_NAME]
        experiment6(graphs_names)

    elif exp == 7:
        graphs_names = [GRAPH_1_NAME]
        experiment7(graphs_names)

    elif exp == 8:
        graphs_names = [GRAPH_1_NAME]
        experiment8(graphs_names)

    elif exp == 9:
        graphs_names = [GRAPH_1_NAME]
        experiment9(graphs_names)

    elif exp == 10:
        experiment10()

    elif exp == 11:
        experiment11()

    elif exp == 12:
        experiment12()


def launchAllExperiments():
    for e in range(1, 13):
        launchExperiment(e)


def main():
    launchExperiment(EXPERIMENT)

    # launchAllExperiments()


if __name__ == "__main__":
    main()
