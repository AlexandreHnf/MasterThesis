from Graph import Graph
from Random import *
from Utils import haversine
from Edge import Edge


class MultiModalGraph(Graph):
    def __init__(self, nodes_coords, adj_list, bucket_size=40):
        Graph.__init__(self, nodes_coords, adj_list, bucket_size)

    def addPublicTransportEdges(self, nb_added_edges, speed_limit):
        """
        - Embark (?)
        - Line
        - Disembark (?)
        """
        nb_added = 0
        while (nb_added < nb_added_edges):
            v1, v2 = selectRandomPair(list(self.nodes_coords.keys()))
            v1_coords = self.getGeoCoords(v1)
            v2_coords = self.getGeoCoords(v2)

            # lat 1, lon 1, lat 2, lon 2
            dist_km = haversine(v1_coords[0], v1_coords[1], v2_coords[0], v2_coords[1])
            edge_weight = 3600 * (dist_km / speed_limit)  # speed limit in km/h

            # add new edge v1 --> v2  /!\ ATTENTION : le reverse graph sera pas multimodal pour les bidirectional
            new_edge = Edge(v2, edge_weight)
            self.addEdge(v1, new_edge)

            nb_added += 1


    def toStationBased(self, stations_nodes):
        """
        Transform the uni-modal graph into a multi-modal station-based graph
        """

        # duplicate the base graph and change the duplicated edges weights
        max_id = max(self.getNodesIDs())
        print("max id in the graph : ", max_id)
        for v in self.getNodesIDs():
            bike_edges = []
            for edge in self.getAdj(v):
                # match bike speed (edge weight walk / 3)
                bike_edges.append(Edge(edge.getExtremityNode() + max_id, edge.getWeight() / 3))
            self.addNode(v+max_id, bike_edges, v)
            # TODO : update nb nodes (nodes list of Graph)

        # add links between the two layers
        for sn in stations_nodes:
            self.addEdge(sn, Edge(sn+max_id, 60))  # node to station
            self.addEdge(sn+max_id, Edge(sn, 60))  # station to node
