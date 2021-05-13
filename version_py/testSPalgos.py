import shortestPath
from Dijkstra import Dijkstra
from Astar import Astar
from ALT import ALT
from bidirectionalDijkstra import BidirectionalDijkstra
from bidirectionalAstar import BidirectionalAstar
from bidirectionalALT import BidirectionalALT
from ALTpreprocessing import ALTpreprocessing
from landmarkTest import *
from time import time
from quadtree import showQtree

def showResult(graph_coords, search_space, shortest_path, sp_coords, spObj, show):
    print("nb nodes search space : {0}, nodes : {1}".format(len(search_space), list(search_space.keys())))
    print("shortest_path : ", shortest_path, len(shortest_path))
    path_length = spObj.getPathLength(shortest_path)
    if path_length:
        print("valid shortest path of length : ", path_length)
    else:
        print("Invalid path !")
    print("============================")

    if show == "True" or show is True:
        print("show !!", show)
        showQtree(spObj.util.qtree, graph_coords, search_space, sp_coords, None)

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

def testDijkstra(graph, graph_coords, s, t, queue_type="bin", show=False):

    d = Dijkstra(graph, graph_coords, s, t, queue_type)
    start = time()
    search_space, shortest_path, sp_coords = d.findShortestPath()
    print("dijkstra done in : ", time() - start, " seconds.")
    showResult(graph_coords, search_space, shortest_path, sp_coords, d, show)

def testAstar(graph, graph_coords, s, t, queue_type="bin", heuristic="euclidean", show=False):

    a = Astar(graph, graph_coords, s, t, queue_type, 40, heuristic)
    start = time()
    search_space, shortest_path, sp_coords = a.findShortestPath()
    print("A* done in : ", time() - start, " seconds.")
    showResult(graph_coords, search_space, shortest_path, sp_coords, a, show)

def testALT(graph, graph_coords, s, t, lm_selection="planar", queue_type="bin", heuristic="euclidean", show=False):

    origin = 50.8460, 4.3496
    alt = ALT(graph, graph_coords, s, t, lm_selection, 16, origin, queue_type, 40, heuristic)
    prepro_start = time()
    lm = alt.preprocessing()
    print("ALT preprocessing done in : ", time() - prepro_start, " seconds.")
    start = time()
    search_space, shortest_path, sp_coords = alt.findShortestPath()
    print("ALT done in : ", time() - start, " seconds.")
    showResult(graph_coords, search_space, shortest_path, sp_coords, alt, show)

def testBidiDijkstra(graph, rev_graph, graph_coords, s, t, queue_type="bin", show=False):
    bd = BidirectionalDijkstra(graph, rev_graph, graph_coords, s, t, queue_type)
    start = time()
    search_space, shortest_path, sp_coords = bd.findShortestPath()
    print("bidirectional dijkstra done in : ", time() - start, " seconds.")
    showResult(graph_coords, search_space, shortest_path, sp_coords, bd, show)

def testBidiAstar(graph, rev_graph, graph_coords, s, t, queue_type="bin", heuristic="euclidean", show=False):
    ba = BidirectionalAstar(graph, rev_graph, graph_coords, s, t, queue_type, 40, heuristic)
    start = time()
    search_space, shortest_path, sp_coords = ba.findShortestPath()
    print("bidirectional A* done in : ", time() - start, " seconds.")
    showResult(graph_coords, search_space, shortest_path, sp_coords, ba, show)

def testBidiALT(graph, rev_graph, graph_coords, s, t, lm_selection="planar", queue_type="bin", heuristic="euclidean", show=False):
    origin = 50.8460, 4.3496
    balt = BidirectionalALT(graph, rev_graph, graph_coords, s, t, lm_selection, 16, origin, queue_type, 40, heuristic)
    prepro_start = time()
    lm = balt.preprocessing()
    print("ALT preprocessing done in : ", time() - prepro_start, " seconds.")
    start = time()
    search_space, shortest_path, sp_coords = balt.findShortestPath()
    print("Bidirectional ALT done in : ", time() - start, " seconds.")
    showResult(graph_coords, search_space, shortest_path, sp_coords, balt, show)