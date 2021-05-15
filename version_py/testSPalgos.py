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

def showResult(graph_coords, search_space, shortest_path, sp_coords, sp_obj, landmarks, show):
    print("Search space : ", list(search_space.keys()))
    print("shortest_path : ", shortest_path, len(shortest_path))
    print("Search space size : ", sp_obj.getSearchSpaceSize())
    print("Nb relaxed vertex : ", sp_obj.getNbRelaxedEdges())
    path_length = sp_obj.getPathLength(shortest_path)
    if path_length:
        print("valid shortest path of length : ", path_length)
    else:
        print("Invalid path !")
    print("===============================================")
    print("===============================================")

    if show == "True" or show is True:
        print("show !!", show)
        showQtree(sp_obj.graph.getQtree(), graph_coords, search_space, sp_coords, landmarks)

#=================================================================================

def testLandmarks(graph, lm_selection):

    print("nb nodes : ", len(graph.getNbNodes()))
    k=16
    origin = 50.8460, 4.3496
    alt = ALT(graph, -1, -1, lm_selection, k, origin)
    start = time()
    landmarks = alt.preprocessing()
    print(landmarks)
    print("time landmark distances : ", time() - start, " seconds.")
    showQtree(alt.util.qtree, None, None, landmarks)
    print("============================")

#=================================================================================

def testDijkstra(graph, s, t, queue_type="bin", show=False):

    d = Dijkstra(graph, s, t, queue_type)
    start = time()
    search_space, shortest_path, sp_coords = d.findShortestPath()
    print("[DIJKSTRA] done in : ", time() - start, " seconds.")
    showResult(graph.getNodes(), search_space, shortest_path, sp_coords, d, None, show)

def testAstar(graph, s, t, queue_type="bin", heuristic="euclidean", show=False):

    a = Astar(graph, s, t, queue_type, 40, heuristic)
    start = time()
    search_space, shortest_path, sp_coords = a.findShortestPath()
    print("[A*] done in : ", time() - start, " seconds.")
    showResult(graph.getNodes(), search_space, shortest_path, sp_coords, a, None, show)

def testALT(graph, s, t, lm_selection="planar", queue_type="bin", heuristic="euclidean", show=False):

    alt = ALT(graph, s, t, lm_selection, 16, None, queue_type, 40, heuristic)
    prepro_start = time()
    lm = alt.preprocessing()
    print("[ALT PREPROCESSING] done in : ", time() - prepro_start, " seconds.")
    start = time()
    search_space, shortest_path, sp_coords = alt.findShortestPath()
    print("[ALT] done in : ", time() - start, " seconds.")
    showResult(graph.getNodes(), search_space, shortest_path, sp_coords, alt, lm, show)

def testBidiDijkstra(graph, s, t, queue_type="bin", show=False):
    bd = BidirectionalDijkstra(graph, s, t, queue_type)
    start = time()
    search_space, shortest_path, sp_coords = bd.findShortestPath()
    print("[BIDI DIJKSTRA] done in : ", time() - start, " seconds.")
    showResult(graph.getNodes(), search_space, shortest_path, sp_coords, bd, None, show)

def testBidiAstar(graph, s, t, queue_type="bin", heuristic="euclidean", show=False):
    ba = BidirectionalAstar(graph, s, t, queue_type, 40, heuristic)
    start = time()
    search_space, shortest_path, sp_coords = ba.findShortestPath()
    print("[BIDI A*] done in : ", time() - start, " seconds.")
    showResult(graph.getNodes(), search_space, shortest_path, sp_coords, ba, None, show)

def testBidiALT(graph, s, t, lm_selection="planar", queue_type="bin", heuristic="euclidean", show=False):
    balt = BidirectionalALT(graph, s, t, lm_selection, 16, None, queue_type, 40, heuristic)
    prepro_start = time()
    lm = balt.preprocessing()
    print("[ALT PREPROCESSING] done in : ", time() - prepro_start, " seconds.")
    start = time()
    search_space, shortest_path, sp_coords = balt.findShortestPath()
    print("[BIDI ALT] done in : ", time() - start, " seconds.")
    showResult(graph.getNodes(), search_space, shortest_path, sp_coords, balt, lm, show)