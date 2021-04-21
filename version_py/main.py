import shortestPath
from Dijkstra import Dijkstra
from Astar import Astar
from ALT import ALT
from bidirectionalDijkstra import BidirectionalDijkstra
from bidirectionalAstar import BidirectionalAstar
from ALTpreprocessing import ALTpreprocessing
import json
import csv
from landmarkTest import *
from time import time
from quadtree import showQtree
from Constants import *
from parseOSMgraph import OSMgraphParser

def load_graph(filename_adj, filename_nodes):

    with open(filename_adj, 'r') as fp:
        graph = json.loads(fp.read())
    with open(filename_nodes, 'r') as fp:
        graph_coords = json.loads(fp.read())
    return graph, graph_coords


def computeBaseDistances(graph, nodes):
    """
    Compute distances between all nodes with an edge in between
    returns the same adjacency lists but with distances
    distance = haversine distance between 2 geographic coordinates
    """
    for pid, adjacents in graph.items():
        adjs = []
        for a in adjacents:
            dist = haversine(nodes[pid][0], nodes[pid][1], nodes[str(a)][0], nodes[str(a)][1])
            adjs.append((str(a), dist))
        graph[pid] = adjs
    return graph

#=================================================================================

def testLandmarks1(graph, graph_coords):
    # print(graph)

    print("nb nodes : ", len(graph_coords))
    qtree = point_dict_to_quadtree(graph_coords, multiquadtree=True)
    k = 16
    origin = 50.8460, 4.3496

    # farthest landmark selection
    # landmarks = farthest_landmark_selection(k, origin, graph_coords)

    # planar landmark selection
    landmarks = planar_landmark_selection(k, origin, graph_coords, graph, qtree)

    landmarks = list(zip([find_closest_node(l, qtree) for l in landmarks], landmarks))
    print("landmarks : ", landmarks)

    showQtree(qtree, graph_coords, landmarks)

    # compute all shortest paths from any node to each landmark
    start = time()
    lm_dists = landmark_distances(landmarks, graph, graph_coords)
    print("time landmark distances : ", time() - start, " seconds.")
    print("============================")

def testLandmarks2(graph, graph_coords):

    print("nb nodes : ", len(graph_coords))
    k=16
    origin = 50.8460, 4.3496
    alt = ALT(graph, graph_coords, "planar", k, origin)
    start = time()
    landmarks = alt.preprocessing()
    print("time landmark distances : ", time() - start, " seconds.")
    showQtree(alt.util.qtree, graph_coords, landmarks)
    print("============================")

def testDijkstra(graph, graph_coords, s, t, show=False):

    d = Dijkstra(graph, graph_coords, s, t, "bin")
    start = time()
    search_space, shortest_path = d.findShortestPath()
    print("dijkstra done in : ", time() - start, " seconds.")
    print("nb nodes search space : {0}, nodes : {1}".format(len(search_space), list(search_space.keys())))
    print("shortest_path : ", list(shortest_path.keys()), len(shortest_path))
    path_length = d.getPathLength(shortest_path)
    if path_length:
        print("valid shortest path of length : ", path_length)
    else:
        print("Invalid path !")
    print("============================")

    if show:
        showQtree(d.util.qtree, graph_coords, search_space, shortest_path, None)

def testAstar(graph, graph_coords, s, t, show=False):

    a = Astar(graph, graph_coords, s, t, "bin")
    start = time()
    search_space, shortest_path = a.findShortestPath()
    print("A* done in : ", time() - start, " seconds.")
    print("nb nodes search space : {0}, nodes : {1}".format(len(search_space), list(search_space.keys())))
    print("shortest_path : ", list(shortest_path.keys()), len(shortest_path))
    path_length = a.getPathLength(shortest_path)
    if path_length:
        print("valid shortest path of length : ", path_length)
    else:
        print("Invalid path !")
    print("============================")

    if show:
        showQtree(a.util.qtree, graph_coords, search_space, shortest_path, None)

def testALT(graph, graph_coords, s, t, show=False):

    origin = 50.8460, 4.3496
    alt = ALT(graph, graph_coords, s, t, "planar", 16, origin, "bin")
    prepro_start = time()
    lm = alt.preprocessing()
    print("ALT preprocessing done in : ", time() - prepro_start, " seconds.")
    start = time()
    search_space, shortest_path = alt.findShortestPath()
    print("ALT done in : ", time() - start, " seconds.")
    print("nb nodes search space : {0}, nodes : {1}".format(len(search_space), list(search_space.keys())))
    print("shortest_path : ", list(shortest_path.keys()), len(shortest_path))
    path_length = alt.getPathLength(shortest_path)
    if path_length:
        print("valid shortest path of length : ", path_length)
    else:
        print("Invalid path !")
    print("============================")

    if show:
        showQtree(alt.util.qtree, graph_coords, search_space, shortest_path, lm)

def testBidiDijkstra(graph, rev_graph, graph_coords, s, t, show=False):
    bd = BidirectionalDijkstra(graph, rev_graph, graph_coords, s, t, "bin")
    start = time()
    search_space, shortest_path = bd.findShortestPath()
    print("bidirectional dijkstra done in : ", time() - start, " seconds.")
    print("nb nodes search space : {0}, nodes : {1}".format(len(search_space), list(search_space.keys())))
    print("shortest_path : ", list(shortest_path.keys()), len(shortest_path))
    path_length = bd.getPathLength(shortest_path)
    if path_length:
        print("valid shortest path of length : ", path_length)
    else:
        print("Invalid path !")
    print("============================")

    if show:
        showQtree(bd.util.qtree, graph_coords, search_space, shortest_path, None)

def testBidiAstar(graph, rev_graph, graph_coords, s, t, show=False):
    ba = BidirectionalAstar(graph, rev_graph, graph_coords, s, t, "bin")
    start = time()
    search_space, shortest_path = ba.findShortestPath()
    print("bidirectional A* done in : ", time() - start, " seconds.")
    print("nb nodes search space : {0}, nodes : {1}".format(len(search_space), list(search_space.keys())))
    print("shortest_path : ", list(shortest_path.keys()), len(shortest_path))
    path_length = ba.getPathLength(shortest_path)
    if path_length:
        print("valid shortest path of length : ", path_length)
    else:
        print("Invalid path !")
    print("============================")

    if show:
        showQtree(ba.util.qtree, graph_coords, search_space, shortest_path, None)

def main():
    # bxl_square_graph_nodes = GRAPH_BXL_CTR_TEST_N
    # bxl_square_graph_adj = GRAPH_BXL_CTR_TEST_A
    # graph, graph_coords = load_graph(bxl_square_graph_adj, bxl_square_graph_nodes)
    # graph = computeBaseDistances(graph, graph_coords)
    p = OSMgraphParser(GRAPH_BXL_CTR_TEST)
    graph = p.parse()
    graph_coords = p.getNodes()

    # =========================================
    # testLandmarks1(graph, graph_coords)
    # testLandmarks2(graph, graph_coords)

    s = 7
    t = 1335
    testDijkstra(graph, graph_coords, s, t)
    # testAstar(graph, graph_coords, s, t)
    # testALT(graph, graph_coords, s, t)

    rev_graph = p.getReverseGraph(graph)
    testBidiDijkstra(graph, rev_graph, graph_coords, s, t, False)
    testBidiAstar(graph, rev_graph, graph_coords, s, t, True)


if __name__ == "__main__":
    main()