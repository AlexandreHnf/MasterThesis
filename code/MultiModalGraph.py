#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Graph import Graph
from Random import *
from Utils import haversine, getCarGasPrice
from Edge import Edge
from UserAdaptedEdge import UserAdaptedEdge
from Quadtree import *
from ParseOSMgraph import OSMgraphParser
from copy import deepcopy
from Timer import Timer


class MultiModalGraph(Graph):
    def __init__(self, nodes_coords, adj_list, bucket_size=40):
        Graph.__init__(self, nodes_coords, adj_list, bucket_size)

    def addPublicTransportEdges(self, nb_added_edges, speed_limit):
        """
        choose x pairs of nodes and add new edges = public transport lines
        """
        nb_added = 0
        while nb_added < nb_added_edges:
            v1, v2 = selectRandomPair(list(self.nodes_coords.keys()))
            v1_coords = self.getGeoCoords(v1)
            v2_coords = self.getGeoCoords(v2)

            # lat 1, lon 1, lat 2, lon 2
            dist_km = haversine(v1_coords[0], v1_coords[1], v2_coords[0], v2_coords[1])
            edge_weight = 3600 * (dist_km / speed_limit)  # speed limit in km/h

            # add new edge v1 --> v2
            new_edge = Edge(v2, "Public Transport", edge_weight, dist_km, speed_limit)
            self.addEdge(v1, new_edge)

            nb_added += 1

        # re-create the reverse graph (becomes multimodal)
        self.rev_adj_list = self.createReverseGraph(self.adj_list)

    def toStationBased(self, stations_nodes):
        """
        Transform the uni-modal graph into a multi-modal station-based graph
        """

        # duplicate the base graph and change the duplicated edges weights
        max_id = max(self.getNodesIDs())
        for v in self.getNodesIDs():
            bike_edges = []
            for edge in self.getAdj(v):
                # match bike speed
                bike_edges.append(Edge(edge.getExtremityNode() + max_id,
                                       "Villo",
                                       3600 * (edge.getLengthKm() / SPEED_BIKE),
                                       edge.getLengthKm(),
                                       SPEED_BIKE))
            self.addNode(v + max_id, bike_edges, v)

        # add links between the two layers
        for sn in stations_nodes:
            # node to station
            self.addEdge(sn, Edge(sn + max_id, "toStation", TO_STATION_COST, None, None))
            # station to node
            self.addEdge(sn + max_id, Edge(sn, "fromStation", FROM_STATION_COST, None, None))

        # re-create the reverse graph (becomes multimodal)
        self.rev_adj_list = self.createReverseGraph(self.adj_list)

    def getWeightedSum(self, edge, prefs):
        """
        weighted sum = c1.x1 + c2.x2
        c1, c2 = preferences
        x1, x2 = metrics : travel time and gas price
        """
        if edge.getTravelType() == "car":
            ws = prefs[0] * edge.getWeight() + prefs[1] * getCarGasPrice(edge.getLengthKm())
            # print("car : {0} . {1} + {2} . {3} = {4}".
            #       format(prefs[0], edge.getWeight(), prefs[1], getCarGasPrice(edge.getLengthKm()), ws))
            return ws

        elif edge.getTravelType() == "toStation":
            # get the non-null preference
            ws = (prefs[0]+prefs[1]) * edge.getWeight()
            return ws

        elif edge.getTravelType() == "fromStation":
            ws = (prefs[0]+prefs[1]) * edge.getWeight()
            return ws

        else :  # bike or foot
            ws = prefs[0] * edge.getWeight() + prefs[1] * PRICE_VILLO
            # print("{0} : {1} . {2} + {3} . {4} = {5}".
            #       format(edge.getTravelType(), prefs[0], edge.getWeight(), prefs[1], 0, ws))
            return ws

    def toWeightedSum(self, prefs):
        for v in self.getNodesIDs():
            for edge in self.getAdj(v):
                weighted_sum = self.getWeightedSum(edge, prefs)
                # print(edge.getTravelType(), edge.getWeight())
                edge.setWeight(weighted_sum)

    def toUserAdapted(self, prefs):
        for v in self.getNodesIDs():
            e = self.getAdj(v)
            for i in range(len(e)):
                e[i] = UserAdaptedEdge(e[i].getExtremityNode(),
                                       e[i].getTravelType(),
                                       e[i].getWeight(),
                                       e[i].getLengthKm(),
                                       e[i].getSpeed(), prefs)

        self.rev_adj_list = self.createReverseGraph(self.adj_list)


# =====================================================================

def addVilloStations(graph, show=False):
    timer = Timer()
    timer.start()
    villo_coords = OSMgraphParser.getVilloNodes()

    if show:
        showVilloStations(graph.getQtree(), graph.getNodesCoords(), villo_coords, False)
        print("show villo")

    # get Villo stations nodes in the graph
    villo_closests = []
    for coord in villo_coords:
        closest = graph.findClosestNode(coord)
        if closest:
            villo_closests.append(closest)
    print("Nb villo stations retrieved : ", len(villo_closests))

    # transform the graph into a multi-modal foot-villo graph
    nodes_coords = deepcopy(graph.getNodesCoords())
    adjlist = deepcopy(graph.getAdjList())
    multi_graph = MultiModalGraph(nodes_coords, adjlist)
    if show:
        print("villo closests : ", villo_closests)
    print("BEFORE : {0} nodes, {1} edges".format(graph.getNbNodes(), graph.getNbEdges()))
    multi_graph.toStationBased(villo_closests)
    print("AFTER : {0} nodes, {1} edges".format(multi_graph.getNbNodes(), multi_graph.getNbEdges()))
    timer.printTimeElapsedMin("single to station-based construction")

    return multi_graph, villo_closests