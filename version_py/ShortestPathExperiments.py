#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Dijkstra import Dijkstra
from Astar import Astar
from ALT import ALT
from BidirectionalDijkstra import BidirectionalDijkstra
from BidirectionalAstar import BidirectionalAstar
from BidirectionalALT import BidirectionalALT
from ALTpreprocessing import ALTpreprocessing
from MultiModalGraph import *
from time import time
from Quadtree import showQtree
from Timer import Timer


def showResult(graph_coords, search_space, shortest_path, sp_coords, sp_obj, landmarks, show):
    # TODO put it in a "SHOW" class along with the matplotlib plots
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


# =================================================================================

def testLandmarks(graph, lm_selection):
    print("nb nodes : ", graph.getNbNodes())
    k = 16
    origin = 50.8460, 4.3496
    alt_pre = ALTpreprocessing(graph, lm_selection, origin, k)
    start = time()
    lm_dists = alt_pre.getLmDistances()
    landmarks = alt_pre.getLandmarks()
    print(landmarks)
    print("time landmark distances : ", time() - start, " seconds.")
    alt = ALT(graph, -1, -1, lm_dists)
    showQtree(graph.getQtree(), graph.getNodesCoords(), None, None, landmarks)
    print("============================")


# =================================================================================

def testDijkstra(graph, s, t, queue_type="bin", show=False):
    d = Dijkstra(graph, s, t, queue_type)
    timer = Timer()
    if t == -1:
        timer.start()
        dists = d.getDistsSourceToNodes()
        print("nb nodes visited : ", len(dists))
        timer.printTimeElapsedSec("[DIJKSTRA] single source")
    else:
        timer.start()
        search_space, shortest_path, sp_coords = d.findShortestPath()
        timer.printTimeElapsedSec("[DIJKSTRA]")

        showResult(graph.getNodesCoords(), search_space, shortest_path, sp_coords, d, None, show)


def testAstar(graph, s, t, queue_type="bin", heuristic="euclidean", show=False):
    a = Astar(graph, s, t, queue_type, 40, heuristic)
    timer = Timer()
    timer.start()
    search_space, shortest_path, sp_coords = a.findShortestPath()
    timer.printTimeElapsedSec("[A*]")
    showResult(graph.getNodesCoords(), search_space, shortest_path, sp_coords, a, None, show)


def testALT(graph, s, t, lm_selection="planar", queue_type="bin", heuristic="euclidean", show=False):

    alt_pre = ALTpreprocessing(graph, lm_selection, None, 16)
    prepro_timer = Timer()
    prepro_timer.start()
    lm_dists = alt_pre.getLmDistances()
    landmarks = alt_pre.getLandmarks()
    prepro_timer.printTimeElapsedSec("[ALT PREPROCESSING]")

    alt = ALT(graph, s, t, lm_dists, queue_type, 40, heuristic)
    timer = Timer()
    timer.start()
    search_space, shortest_path, sp_coords = alt.findShortestPath()
    timer.printTimeElapsedSec("[ALT]")
    showResult(graph.getNodesCoords(), search_space, shortest_path, sp_coords, alt, landmarks, show)

    max_avg_dist = alt.getAvgMaxHeuristicDist()
    print("max avg distance ALT : ", max_avg_dist)

def testBidiDijkstra(graph, s, t, queue_type="bin", show=False):
    bd = BidirectionalDijkstra(graph, s, t, queue_type)
    timer = Timer()
    timer.start()
    search_space, shortest_path, sp_coords = bd.findShortestPath()
    timer.printTimeElapsedSec("[BIDI DIJKSTRA]")
    showResult(graph.getNodesCoords(), search_space, shortest_path, sp_coords, bd, None, show)


def testBidiAstar(graph, s, t, queue_type="bin", heuristic="euclidean", show=False):
    ba = BidirectionalAstar(graph, s, t, queue_type, 40, heuristic)
    timer = Timer()
    timer.start()
    search_space, shortest_path, sp_coords = ba.findShortestPath()
    timer.printTimeElapsedSec("[BIDI A*]")
    showResult(graph.getNodesCoords(), search_space, shortest_path, sp_coords, ba, None, show)


def testBidiALT(graph, s, t, lm_selection="planar", queue_type="bin", heuristic="euclidean", show=False):
    balt_pre = ALTpreprocessing(graph, lm_selection, None, 16)
    prepro_timer = Timer()
    prepro_timer.start()
    lm_dists = balt_pre.getLmDistances()
    landmarks = balt_pre.getLandmarks()
    prepro_timer.printTimeElapsedSec("[BIDI ALT PREPROCESSING]")

    balt = BidirectionalALT(graph, s, t, lm_dists, queue_type, 40, heuristic)
    timer = Timer()
    timer.start()
    search_space, shortest_path, sp_coords = balt.findShortestPath()
    timer.printTimeElapsedSec("[BIDI ALT]")
    showResult(graph.getNodesCoords(), search_space, shortest_path, sp_coords, balt, landmarks, show)


def testMMDijkstra(graph, s, t, queue_type="bin", show=False):
    multi_graph, villo_closests = addVilloStations(graph)
    prefs = [1, 1]
    multi_graph.toWeightedSum(prefs)

    d = Dijkstra(multi_graph, s, t, queue_type)
    timer = Timer()
    timer.start()
    search_space, shortest_path, sp_coords = d.findShortestPath()
    timer.printTimeElapsedSec("[DIJKSTRA]")
    showResult(multi_graph.getNodesCoords(), search_space, shortest_path, sp_coords, d, None, show)