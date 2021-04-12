from GraphDijkstra import * 
from Utils import *  
from Node import * 
from Dijkstra import * 
import time 
import json

def parse(filename):
    p = [] # new nodes 

    G = GraphDijkstra()
    nb_edges = 0

    # try:
    with open(filename) as my_file:
        
        lines = my_file.readlines()
        for line in lines:
            l = line.strip().split()
            if l[0] == "v":
                G.createNode(int(l[1])-1, float(l[2]), float(l[3])) # ID - 1 to start with 0
            elif l[0] == "e":
                n1, n2 = int(l[2])-1, int(l[3])-1
                G.getNode(n1).addAdjacentNode(G.getNode(n2))
                # also add the inverse edge since it's a undirected graph
                G.getNode(n2).addAdjacentNode(G.getNode(n1))
                nb_edges += 1
                dist = distanceEarth(G.getNode(n1).lat, G.getNode(n1).lon, G.getNode(n2).lat, G.getNode(n2).lon)
                # print("e {0} - {1} dist = {2}".format(n1, n2, dist))

    G.setNbEdges(nb_edges)
    # G.show()
    return G

    # except:
    #     print("Problem when reading a file : ", filename )

def writeSolToJson(shortest_path):
    to_write = {
        "type": "FeatureCollection",
        "features": []
    }
    for node in shortest_path:
        coordinates = [node.getLatitude(), node.getLongitude()]
        to_write["features"].append({"type":"Feature", "geometry":{"type": "Point", "coordinates": coordinates}, "properties":{"id":node.getID()}})
    
    # print(json.dumps(to_write, indent = 4, sort_keys=True))
    with open('D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\MasterThesis\\py\\test.json', 'w') as json_file:
        json.dump(to_write, json_file)

def timing(start_time):
    end = time.time() - start_time
    nb_minutes = end // 60
    nb_seconds = end - (nb_minutes * 60)
    print("Time spent : {0} min {1} sec. Total : {2} sec".format(nb_minutes, nb_seconds, end))

def testSimpleGraph():
    filename_testgraph = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\MasterThesis\\py\\testgraph.txt"
    G = parse(filename_testgraph)

    D = Dijkstra(2,4, G)

    begin = time.time()
    D.runDijkstra()
    timing(begin)

def testBxlSquare():
    filename_bxl_square = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\MasterThesis\\py\\testgraph2.txt"
    G = parse(filename_bxl_square)
    G.showStats()

    D = Dijkstra(0, 1334, G)
    # for i in range(G.getNbNodes()):
    #     print("G.getNode({0}).getID() : {1}".format(i, G.getNode(i).getID()))

    begin = time.time()
    D.runDijkstra()
    timing(begin)

    writeSolToJson(D.getShortestPath())

def main():

    # test Dijkstra on simple example graph 
    # testSimpleGraph()
    
    # test Dijkstra on bxl square
    testBxlSquare()

if __name__ == "__main__":
    main()