import shortestPath
from Dijkstra import Dijkstra
from Astar import Astar
from ALT import ALT
from ALTpreprocessing import ALTpreprocessing
import json
import csv
from landmarkTest import *
from time import time
from quadtree import showQtree

W = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\Datasets_graphs\\"

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

def testDijkstra(graph, graph_coords):

    d = Dijkstra(graph, graph_coords)
    start = time()
    search_space, shortest_path = d.findShortestPath("7", "1335")
    print("dijkstra done in : ", time() - start, " seconds.")
    path_length = d.getPathLength(search_space)
    print("nb nodes : {0}, path length : {1} : {2}".format(len(search_space), path_length, list(search_space.keys())))
    print("shortest_path search space : ", shortest_path, len(shortest_path))
    print("vald path ? ", d.isValidPath(search_space))
    print("============================")

def testAstar(graph, graph_coords):

    a = Astar(graph, graph_coords)
    start = time()
    search_space, shortest_path = a.findShortestPath("7", "1335")
    print("A* done in : ", time() - start, " seconds.")
    path_length = a.getPathLength(search_space)
    print("nb nodes search space: {0}, path length : {1} : {2}".format(len(search_space), path_length, list(search_space.keys())))
    print("shortest_path : ", shortest_path, len(shortest_path))
    print("vald path ? ", a.isValidPath(search_space))
    print("============================")

def testALT(graph, graph_coords):

    origin = 50.8460, 4.3496
    alt = ALT(graph, graph_coords, "planar", 16, origin)
    prepro_start = time()
    lm = alt.preprocessing()
    print("ALT preprocessing done in : ", time() - prepro_start, " seconds.")
    start = time()
    search_space, shortest_path = alt.findShortestPath("7", "1335")
    print("ALT done in : ", time() - start, " seconds.")
    path_length = alt.getPathLength(search_space)
    print("nb nodes search space: {0}, path length : {1} : {2}".format(len(search_space), path_length, list(search_space.keys())))
    print("shortest_path : ", shortest_path, len(shortest_path))
    print("vald path ? ", alt.isValidPath(search_space))
    print("============================")

    showQtree(alt.util.qtree, graph_coords, search_space, shortest_path, lm)


def main():
    bxl_square_graph_nodes = W + "small_graph\\test_bxl_square_nodes.json"
    bxl_square_graph_adj = W + "small_graph\\test_bxl_square_adj.json"
    graph, graph_coords = load_graph(bxl_square_graph_adj, bxl_square_graph_nodes)
    graph = computeBaseDistances(graph, graph_coords)

    # =========================================
    # testLandmarks1(graph, graph_coords)
    # testLandmarks2(graph, graph_coords)

    testDijkstra(graph, graph_coords)
    testAstar(graph, graph_coords)
    testALT(graph, graph_coords)


if __name__ == "__main__":
    main()