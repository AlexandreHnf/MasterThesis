import json
from utils import *
from Edge import Edge
from Constants import *
import random
from Dijkstra import Dijkstra

class OSMgraphParser:
    def __init__(self, filename):
        self.graph_filename = filename
        self.nodes_coordinates = {}  # key = node ID, value = (lat, lon)
        self.original_nb_nodes = 0
        self.original_nb_edges = 0
        self.tot_nb_nodes = 0
        self.tot_nb_edges = 0
        self.nb_edges_no_speed = 0
        self.nb_self_loops = 0  # loop edges (edge coming from a node v and going to the same node
        self.connection_ratio = 0
        self.nb_two_way_edges = 0
        self.nb_duplicate_edges = 0

    def isDuplicateEdge(self, adjList, v, w, weight):
        """
        if a duplicate edge exists, we keep the smallest weight edge
        """
        for edge in adjList[v]:  # all edges adjacent to v

            if edge.getExtremityNode() == w:  # same extremities (nodes)
                if weight < edge.getWeight():
                    edge.setWeight(weight)
                self.nb_duplicate_edges += 1
                return True
        return False

    def createEdge(self, feature, adjList, v, w, weight):
        """
        Given 2 nodes and a new edge weight, creates a new edge
        [v] --- weight --- [w] and add it to the adjacency list
        """
        if not self.isDuplicateEdge(adjList, v, w, weight):
            adjList[v].append(Edge(w, weight))  # new edge forward

            oneway_tag = feature["properties"]["tags"].get("oneway", None)
            if oneway_tag is None or oneway_tag == "no":  # if backward edge must exist
                if not self.isDuplicateEdge(adjList, w, v, weight):
                    adjList[w].append(Edge(v, weight))  # new edge backward
                    self.nb_two_way_edges += 1

    def estimateSpeedLimit(self, highway_tag):
        """
        If an edge in the OSM graph does not come with a speed limit tag, then
        we have to estimate it depending on the road type
        """
        self.nb_edges_no_speed += 1
        if highway_tag in ["primary", "primary_link", "secondary", "secondary_link", "tertiary", "tertiary_link", "residential"]:
            return 50  # 50 km/h => do not take into account 30 km/h roads
        elif highway_tag in ["trunk", "trunk_link", "motorway", "motorway_link"]:
            return 120  # high speed roads
        else:
            print("Highway tag not specified !")
            return None

    def getSpeedLimit(self, feature, travel_type):
        """
        Given a travel type : car or foot, return the maxspeed or an estimation of it
        if no maxspeed is provided
        """
        if travel_type == "foot":
            return SPEED_LIMIT_FOOT
        elif travel_type == "car":
            maxspeed = feature["properties"]["tags"].get("maxspeed", None)
            if maxspeed:  # not None
                return maxspeed
            else:
                return self.estimateSpeedLimit(feature["properties"]["tags"]["highway"])


    def getVilloNodes(self):
        """
        Get the geographic coordinates (lat, lon) of all "villo" stations
        in Brussels
        """
        stations_coordinates = []  # value = (lat, lon)
        features = self.getJsonData(GRAPH_VILLO)["features"]
        for f in features:
            stations_coordinates.append((f["geometry"]["coordinates"][1], f["geometry"]["coordinates"][0]))
        return stations_coordinates

    def getJsonData(self, filename):
        """
        parse json file and return all data in json format
        """
        # read file
        with open(filename, 'r', encoding=ENCODING) as myfile:
            data = myfile.read()
        return json.loads(data)

    def getNodesCoordinates(self, features, adjlist):
        for f in features:
            if f["geometry"]["type"] == "Point":
                self.original_nb_nodes += 1
                # (lat, lon)
                point = [f["geometry"]["coordinates"][1], f["geometry"]["coordinates"][0]]
                self.nodes_coordinates[f["id"]] = point
                adjlist[f["id"]] = []

    def getNodes(self):
        return self.nodes_coordinates

    def computeEdgeWeight(self, feature):
        """
        Given an edge, composed of 6 coordinates, compute its length in km
        => successive additions of euclidean distances between pairs of intermediate
        geographic coordinates (lat, lon)
        """
        length_km = 0
        prev = False
        prevLat, prevLon = 0, 0
        for coord in feature["geometry"]["coordinates"]:
            lat = coord[1]
            lon = coord[0]
            if prev:
                length_km += haversine(prevLat, prevLon, lat, lon)  # euclidean distance
            prevLat = lat
            prevLon = lon
            prev = True
        return length_km

    def getNbEdges(self, graph):
        """
        TODO : mettre cette fonction autre part (graph Utils par exemple)
        """
        nb_edges = 0
        for v in graph:
            nb_edges += len(v)
        return nb_edges

    def getReverseGraph(self, graph):
        reverse_graph = [[] for _ in range(len(graph))]
        for s in range(len(graph)):
            for edge in graph[s]:
                reverse_graph[edge.getExtremityNode()].append(Edge(s, edge.getWeight()))
        return reverse_graph

    def getStronglyConnectedGraph(self, graph, s):
        connected_graph = []
        forward = Dijkstra(graph) # TODO : change



        return connected_graph


    def getConnectedGraph(self, adjlist):
        """
        remove non connected nodes so that the graph is
        strongly connected
        """
        connected_graph = []
        while self.connection_ratio < 0.5:
            s = random.randint(0, len(adjlist))  # random starting node
            connected_graph = self.getStronglyConnectedGraph(adjlist, s)
            self.connection_ratio = len(connected_graph) / len(adjlist)
        self.tot_nb_nodes = len(connected_graph)
        self.tot_nb_edges = self.getNbEdges(connected_graph)

        return connected_graph

    def parse(self, travel_type="car"):
        """
        parse a OSM graph and return a graph : adjacency list
        adjlist : index = node v's ID - 1, value = list of Edges adjacent to node v
        travel type : either car (using road max speed) or foot (5 km/h)

            child, elderly: 1 à 3 km/h
            adult: 4 à 6 km/h => 5km/h in average
            runner: 12 à 15 km/h

        """

        features = self.getJsonData(self.graph_filename)["features"]
        adjlist = {}  # key = ID, value = list of adjacent Edge (object)
        self.getNodesCoordinates(features, adjlist)

        for f in features:
            if f["geometry"]["type"] == "LineString":  # if edges
                self.original_nb_edges += 1
                srcID = f["src"]
                tgtID = f["tgt"]
                if srcID == tgtID:  # self loop
                    self.nb_self_loops += 1
                    continue

                speed_limit = self.getSpeedLimit(f, travel_type)
                length_km = self.computeEdgeWeight(f)
                edge_weight = length_km
                # edge_weight = 3600 * (length_km / speed_limit)  # travel time in seconds

                self.createEdge(f, adjlist, srcID, tgtID, edge_weight)

        # return self.getConnectedGraph(adjlist)
        return adjlist

    def getAvgDegree(self, graph):
        """
        Get the average node degree of the graph
        TODO : mettre ca ailleurs (graph utils)
        """

    def showStats(self):
        """
        Show all stats related to the parsing of the OSM graph data
        """
        print("======= Stats graph OSM ======== ")
        print("Raw graph : {0} nodes, {1} edges".format(self.original_nb_nodes, self.original_nb_nodes))
        print("nb two way edges : {0} = {1} % ".format(self.nb_two_way_edges, 100*(self.nb_two_way_edges / self.original_nb_edges)))
        print("nb duplicate edges : {0} = {1} %".format(self.nb_duplicate_edges, 100*(self.nb_duplicate_edges/self.original_nb_edges)))
        print("nb self loop edges : {0} = {1} %".format(self.nb_self_loops, 100*(self.nb_self_loops/self.original_nb_edges)))
        print("nb edges with no speed limit defined : {0} = {1} %".format(self.nb_edges_no_speed, 100*(self.nb_edges_no_speed/self.original_nb_edges)))
        print("Final graph : {0} nodes, {1} edges".format(self.tot_nb_nodes, self.tot_nb_edges))
        print("Connected graph connection ratio : {0} % of vertices left".format(100*self.connection_ratio))

    def showGraph(self, graph):
        """
        TODO : mettre ca ailleurs (graph utils)
        """
        for v, adj in graph.items():
            print("{0} : ".format(v), end="")
            for e in adj:
                print("--{0}, ".format(e.getExtremityNode()), end=" ")
            print()


def main():
    # graph = {"id": [Edge, Edge, ...], ...}
    # nodes = {"id": [lat, lon], ...}
    p = OSMgraphParser(GRAPH_BXL_CTR_TEST)
    adjlist = p.parse()
    p.showStats()
    p.showGraph(adjlist)

if __name__ == "__main__":
    main()