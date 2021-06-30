from Benchmark import *
from MultiModalGraph import *
from ParseOSMgraph import OSMgraphParser
from copy import deepcopy
from Quadtree import showVilloStations

def experiment1():
    """
    Experiment 1 : test which queue type gives fastest Dijkstra
    - List
    - Binary Heap
    - Fibonacci Heap
    """
    pass
    # TODO TOTEST


def experiment2():
    """
    Experiment 2 : test which heuristic gives fastest A*
    - Euclidean
    - Manhattan
    - Octile
    """
    pass
    # TODO TOTEST


def experiment3():
    """
    Experiment 3 : test which landmark selection gives fastest ALT
    - Random
    - Farthest
    - Planar
    """
    pass
    # TODO TOTEST


def experiment4():
    """
    Experiment 4 : test which nb of landmarks (k) gives fastest ALT
    """
    pass
    # TODO TOTEST


def experiment5():
    """
    Experiment 5 : Single modal car network
    query benchmarks for a given graph
    TODO check if the results are coherent (with the plots)
    """
    p = OSMgraphParser(GRAPH)
    graph = p.parse()

    b = Benchmark(graph)

    alt_pre = ALTpreprocessing(graph, LANDMARK_SELECTION, None, NB_LANDMARKS)
    lm_dists = alt_pre.getLmDistances()
    print("ready (preprocessing done)")

    algos = ["Dijkstra", "A*", "ALT", "BidiDijkstra", "BidiAstar", "BidiALT"]

    stats = b.testMultipleQueries(10, graph, algos, lm_dists)
    # TODO : write to file
    print(stats)


def experiment6():
    """
    Experiment 6 : Single modal car network
    Preprocessing benchmarks
    TODO check if the results are coherent (plot the qtree ?)
    """
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
    """
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
            stats = b.testMultipleQueries(10, multi_graph, algos, lm_dists)

            print("Stats : ", stats)

def experiment8():
    """
    Experiment 8 : Multi-modal station-based network
    TODO TOTEST
    """
    p = OSMgraphParser(GRAPH)
    graph = p.parse("foot")

    villo_coords = OSMgraphParser.getVilloNodes()
    #print(villo_coords)

    showVilloStations(graph.getQtree(), graph.getNodesCoords(), villo_coords, True)

    # get Villo stations nodes in the graph
    villo_closests = []
    for coord in villo_coords:
        villo_closests.append(graph.findClosestNode(coord))

    # transform the graph into a multi-modal foot-villo graph
    nodes_coords = deepcopy(graph.getNodesCoords())
    adjlist = deepcopy(graph.getAdjList())
    multi_graph = MultiModalGraph(nodes_coords, adjlist)
    print(villo_closests)
    multi_graph.toStationBased(villo_closests)

    b = Benchmark(multi_graph)
    alt_pre = ALTpreprocessing(multi_graph, "planar", None, 16)
    lm_dists = alt_pre.getLmDistances()
    algos = {"Dijkstra": Dijkstra(multi_graph, -1, -1, "bin"), "ALT": ALT(multi_graph, -1, -1, lm_dists, "bin")}
    stats = b.testMultipleQueries(10, algos, lm_dists)


def experiment9():
    """
    Experiment 9 :
    Multi modal with : personal car and personal bike ? => pb of coherence mmmh
    TODO TOTEST
    """
    pass


def experiment10():
    """
    Experiment 10 :
    Multi-Labelling algorithm pareto optimal
    TODO TOTEST
    """


# =====================================================



def main():
    #experiment5()

    #experiment6()

    # experiment7()

    experiment8()

if __name__ == "__main__":
    main()
