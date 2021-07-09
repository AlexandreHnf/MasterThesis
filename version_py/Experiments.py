from Benchmark import *
from MultiModalGraph import *
from ParseOSMgraph import OSMgraphParser
from copy import deepcopy
from Quadtree import showVilloStations
import Writer


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

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(), "nb_edges": graph.getNbEdges()}

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
        Writer.writeDictDictStatsToCsv(stats, header, filename)

    Writer.dicToJson(all_stats, FILE_EXP1_ALL)


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

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(), "nb_edges": graph.getNbEdges()}

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
        Writer.writeDictDictStatsToCsv(stats, header, filename)

    Writer.dicToJson(all_stats, FILE_EXP2_ALL)


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

        all_stats[graph_name] = {"nb_nodes": graph.getNbNodes(), "nb_edges": graph.getNbEdges()}

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
        Writer.writeDictDictStatsToCsv(stats, header, filename)

    Writer.dicToJson(all_stats, FILE_EXP3_ALL)


def experiment4(graphs_names):
    """
    Experiment 4 : test which nb of landmarks (k) gives fastest ALT
    => test with 1, 2, 4, 8, 16 and 21 landmarks
    difficult to have the optimal k => NP-hard problem
    TODO : change nb runs to 1000 + use the 6 graphs
    TODO check if the results are coherent with plots
    """
    print("EXPERIMENT 4 : how many landmarks ALT")
    for graph_name in graphs_names:
        p = OSMgraphParser(GRAPH_FILENAMES[graph_name])
        graph = p.parse()

        b = Benchmark(graph)

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
        filename = FILE_EXP4 + graph_name + "_exp4.csv"
        Writer.writeDictDictStatsToCsv(all_stats, header, filename)


def experiment5(graphs_names):
    """
    Experiment 5 : Single modal car network
    query benchmarks for a given graph for multiple algorithms
    TODO check if the results are coherent (with the plots)
    TODO : change nb runs to 1000 + use the 6 graphs
    """
    print("EXPERIMENT 5 : Single modal car network query benchmarks for a given graph for multiple algo")
    for graph_name in graphs_names:
        p = OSMgraphParser(GRAPH_FILENAMES[graph_name])
        graph = p.parse()

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

        header = ["algo", "avg_CT", "avg_SS", "avg_rel", "lm_dists_CT"]
        filename = FILE_EXP5 + graph_name + "_exp5.csv"
        Writer.writeDictDictStatsToCsv(stats, header, filename)


def experiment6(graphs_names):
    """
    Experiment 6 : Single modal car network
    Preprocessing benchmarks
    TODO check if the results are coherent (plot the qtree ?)
    TODO : change nb experiments to 1000 + use the 6 graphs
    TODO : change this experiment, with different parameters for preprocessing
    """
    print("EXPERIMENT 6 : Single modal car network, preprocessing benchmarks")
    for graph_name in graphs_names:
        p = OSMgraphParser(GRAPH_FILENAMES[graph_name])
        graph = p.parse()

        b = Benchmark(graph)
        stats = b.testPreprocessing(LANDMARK_SELECTION, NB_LANDMARKS)

        print(stats["Prepro_time"], " seconds")
        header = ["landmark_selection", "nb_landmarks", "prepro_CT"]
        all_stats = [LANDMARK_SELECTION, NB_LANDMARKS, stats["Prepro_time"]]
        filename = FILE_EXP6 + graph_name + "_exp6.csv"
        Writer.writeSingleRowStatsToCsv(all_stats, header, filename)


def experiment7(graphs_names):
    """
    Experiment 7 : Multi-modal public transport network
    TODO check if the results are coherent (with plots)
    # TODO : change nb runs to 1000 + use the 6 graphs
    TODO : add the stats : nb_edges after added lines
    """
    print("EXPERIMENT 7 : Multi-modal public transport network : Dijkstra & ALT")
    for graph_name in graphs_names:
        p = OSMgraphParser(GRAPH_FILENAMES[graph_name])
        graph = p.parse("foot")
        print("nb edges before experiments : ", graph.getNbEdges())

        nb_added_edges = [0, 10, 50, 100, 200]  # TODO : change nb (200) to be 1.1% of the graph size
        speed_limits = [0.1, 15, 30, 90, 120, 1e10]

        all_stats = {}

        nb_exp = 0
        for s in speed_limits:
            for n in nb_added_edges:
                print("==> nb added edges : {0}, speed limit : {1}".format(n, s))
                nodes_coords = deepcopy(graph.getNodesCoords())
                adjlist = deepcopy(graph.getAdjList())
                multi_graph = MultiModalGraph(nodes_coords, adjlist)
                multi_graph.addPublicTransportEdges(n, s)
                print("nb edges after added lines = ", multi_graph.getNbEdges())

                b = Benchmark(multi_graph)
                pre_timer = Timer()
                alt_pre = ALTpreprocessing(multi_graph, "planar", None, 16)
                lm_dists = alt_pre.getLmDistances()
                pre_timer.end_timer()
                prepro_time = pre_timer.getTimeElapsedSec()
                algos = ["Dijkstra", "ALT"]
                stats = b.testMultipleQueries(NB_RUNS, multi_graph, algos, lm_dists, prepro_time)

                all_stats[nb_exp] = [s, n] + list(stats["Dijkstra"].values()) + list(stats["ALT"].values())
                print("Stats : ", all_stats[nb_exp])
                nb_exp += 1

        header = ["speed_limit", "nb_added_edges", "D_avg_CT", "D_avg_SS", "D_avg_rel",
                  "ALT_avg_CT", "ALT_avg_SS", "ALT_avg_rel", "lm_dists_CT"]
        filename = FILE_EXP7 + graph_name + "_exp7.csv"
        Writer.writeDictStatsToCsv(all_stats, header, filename)


def experiment8(graphs_names):
    """
    Experiment 8 : Multi-modal station-based network
    TODO TOTEST
    # TODO : change nb runs to 1000 + use the 6 graphs
    """
    print("EXPERIMENT 8 : Multi-modal station-based network : Dijkstra & ALT")
    for graph_name in graphs_names:
        p = OSMgraphParser(GRAPH_FILENAMES[graph_name])
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
        print("villo closests : ", villo_closests)
        print("BEFORE : {0} nodes, {1} edges".format(graph.getNbNodes(), graph.getNbEdges()))
        multi_graph.toStationBased(villo_closests)
        print("AFTER : {0} nodes, {1} edges".format(multi_graph.getNbNodes(), multi_graph.getNbEdges()))

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
        filename = FILE_EXP8 + graph_name + "_exp8.csv"
        Writer.writeDictDictStatsToCsv(stats, header, filename)


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
        experiment9()

    elif exp == 10:
        experiment10()


def launchAllExperiments():
    for e in range(1, 11):
        launchExperiment(e)


def main():
    launchExperiment(EXPERIMENT)

    # launchAllExperiments()


if __name__ == "__main__":
    main()
