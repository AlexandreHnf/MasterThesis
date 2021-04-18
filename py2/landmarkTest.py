# Copyright (c) 2013 Ryan Pon
# Licensed under the MIT license.

"""
Landmark computation on a graph network
    - planar landmarks selection
    - farthest landmarks selection
"""

import json
from heapq import heappush, heappop
from quadtree import point_dict_to_quadtree, showQtree
from collections import defaultdict
from utils import haversine, bearing
from time import time

W = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\Datasets_graphs\\"

def find_closest_node(target, quadtree, rng=.01):
    x, y = target
    close_nodes = quadtree.query_range(x - rng, x + rng, y - rng, y + rng)
    best_node = None
    best_dist = float("inf")
    for point, nodes in close_nodes.items():
        dist = haversine(point[0], point[1], target[0], target[1])
        if dist < best_dist:
            best_dist = dist
            best_node = nodes
    if best_node:
        return best_node[0]
    else:
        return None


def exact_dist(source, dest, graph, coords):
    dest_x, dest_y = coords[dest]
    pred_list = {source: 0}
    closed_set = set()
    unseen = [(0, source)]  # keeps a set and heap structure
    while unseen:
        _, vert = heappop(unseen)
        if vert in closed_set:
            # needed because we dont have a heap with decrease-key
            continue
        elif vert == dest:
            return pred_list[vert]
        closed_set.add(vert)
        for arc, arc_len in graph[vert]:
            if arc not in closed_set:
                new_dist = (pred_list[vert] + arc_len)
                if arc not in pred_list or new_dist < pred_list[arc]:
                    pred_list[arc] = new_dist
                    x, y = coords[arc]
                    heappush(unseen, (new_dist + haversine(x, y, dest_x, dest_y), arc))
    return None  # no valid path found


def lm_exact_dist(source, dest, graph, coords, lm_dists):
    """ Speed up by using already calculated euclidean distance. """
    lm_dists = lm_dists[dest]
    pred_list = {source: 0}
    closed_set = set()
    unseen = [(0, source)]  # keeps a set and heap structure
    while unseen:
        _, vert = heappop(unseen)
        if vert in closed_set:
            # needed because we dont have a heap with decrease-key
            continue
        elif vert == dest:
            return pred_list[vert]
        closed_set.add(vert)
        for arc, arc_len in graph[vert]:
            if arc not in closed_set:
                new_dist = (pred_list[vert] + arc_len)
                if arc not in pred_list or new_dist < pred_list[arc]:
                    pred_list[arc] = new_dist
                    heappush(unseen, (new_dist + lm_dists[arc], arc))
    return None  # no valid path found


def landmark_distances(landmarks, graph, graph_coords):
    lm_est = {}
    for lm_id, lm_coord in landmarks:
        lm_est[lm_id] = {}
        x, y = lm_coord
        for pid, coord in graph_coords.items():
            lm_est[lm_id][pid] = haversine(x, y, coord[0], coord[1])
    lm_dists = defaultdict(list)
    l = len(graph_coords)
    for i, pid in enumerate(graph_coords):
        # print(i, '/', l, ':', pid)
        for landmark, _ in landmarks:
            try:
                d = lm_exact_dist(pid, landmark, graph, graph_coords, lm_est)
            except KeyError:
                d = None
            lm_dists[pid].append(d)
    return lm_dists


def planar_landmark_selection(k, origin, coords, graph, qtree):
    origin_id = find_closest_node(origin, qtree)
    origin = coords[origin_id]
    sectors = section_plane(k, origin, coords)
    landmarks = []
    for sector in sectors:
        max_dist = float("-inf")
        best_candidate = None
        for pid, coord in sector:
            cur_dist = haversine(origin[0], origin[1], coord[0], coord[1])
            if cur_dist > max_dist and exact_dist(pid, origin_id, graph, coords):
                max_dist = cur_dist
                best_candidate = coord
        landmarks.append(best_candidate)
    return landmarks


def section_plane(k, origin, coords):
    sectors = [[] for _ in range(k)]
    sector_size = 360.0 / k
    for pid, coord in coords.items():
        b = bearing(origin[0], origin[1], coord[0], coord[1], True)
        s = int(b / sector_size)
        sectors[s].append((pid, coord))
    return sectors


def farthest_landmark_selection(k, origin, coords):
    landmarks = [origin]
    for _ in range(k):
        max_dist = float("-inf")
        best_candidate = None
        for pid, coord in coords.items():
            cur_dist = 0
            for lm in landmarks:
                cur_dist += haversine(lm[0], lm[1], coord[0], coord[1])
            if cur_dist > max_dist and not coord in landmarks:
                max_dist = cur_dist
                best_candidate = coord
        landmarks.append(best_candidate)
        if len(landmarks) > k:
            landmarks.pop(0)
    return landmarks

# ======================================================

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

def testSFgraph():
    filename_sf = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\code ALT from other\\pathfinding-animator\\routing\\graph_data\\sf.j"
    filename_sf_coords = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\code ALT from other\\pathfinding-animator\\routing\\graph_data\\sf_coords.j"
    graph, graph_coords = load_graph(filename_sf, filename_sf_coords)
    return graph, graph_coords

def testBxlSquare():
    bxl_square_graph_nodes = W + "small_graph\\test_bxl_square_nodes.json"
    bxl_square_graph_adj = W + "small_graph\\test_bxl_square_adj.json"
    graph, graph_coords = load_graph(bxl_square_graph_adj, bxl_square_graph_nodes)
    graph = computeBaseDistances(graph, graph_coords)
    #print(graph)
    return graph, graph_coords

def main():

    # graph, graph_coords = testSFgraph()

    graph, graph_coords = testBxlSquare()

    print("nb nodes : ", len(graph_coords))
    # origin = 37.772614, -122.423798

    qtree = point_dict_to_quadtree(graph_coords, 40, multiquadtree=True)
    rect = qtree.query_range(4.33, 4.34, 50.845, 50.850)
    # print(rect)

    k = 16
    origin = 50.8460, 4.3496

    # farthest landmark selection
    # landmarks = farthest_landmark_selection(k, origin, graph_coords)

    # planar landmark selection
    landmarks = planar_landmark_selection(k, origin, graph_coords, graph, qtree)

    landmarks = list(zip([find_closest_node(l, qtree) for l in landmarks], landmarks))
    print("landmarks : ", landmarks)

    showQtree(qtree, graph_coords, None, None, landmarks)

    # compute all shortest paths from any node to each landmark
    # start = time()
    # lm_dists = landmark_distances(landmarks, graph, graph_coords)
    # print("time landmark distances : ", time() - start, " seconds.")
    # with open(W + 'small_graph\\test_bxl_square_Flm_dists.json', 'w') as fp:
    #     fp.write(json.dumps(lm_dists))

if __name__ == '__main__':
    main()