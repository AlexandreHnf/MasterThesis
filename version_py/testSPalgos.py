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

def showResult(graph_coords, search_space, shortest_path, sp_coords, sp_obj, show):
    print("Search space : ", list(search_space.keys()))
    print("shortest_path : ", shortest_path, len(shortest_path))
    print("Search space size : ", sp_obj.getSearchSpaceSize())
    print("Nb relaxed vertex : ", sp_obj.getNbRelaxedEdges())
    path_length = sp_obj.getPathLength(shortest_path)
    if path_length:
        print("valid shortest path of length : ", path_length)
    else:
        print("Invalid path !")
    print("============================")

    if show == "True" or show is True:
        print("show !!", show)
        showQtree(sp_obj.util.qtree, graph_coords, search_space, sp_coords, None)

#=================================================================================

def testLandmarks(graph, graph_coords, lm_selection):

    print("nb nodes : ", len(graph_coords))
    k=16
    origin = 50.8460, 4.3496
    alt = ALT(graph, graph_coords, -1, -1, lm_selection, k, origin)
    start = time()
    landmarks = alt.preprocessing()
    print(landmarks)
    print("time landmark distances : ", time() - start, " seconds.")
    showQtree(alt.util.qtree, graph_coords, None, None, landmarks)
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
    print(lm)
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