from GraphDijkstra import * 
from Utils import *  
from Node import * 
from Dijkstra import * 

def parse(filename):
    p = [] # new nodes 

    G = GraphDijkstra()

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
                dist = distanceEarth(G.getNode(n1).lat, G.getNode(n1).lon, G.getNode(n2).lat, G.getNode(n2).lon)
                print("e {0} - {1} dist = {2}".format(n1, n2, dist))

    G.show()
    return G

    # except:
    #     print("Problem when reading a file : ", filename )

def main():
    filename_testgraph = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\MasterThesis\\py\\testgraph.txt"
    G = parse(filename_testgraph)

    D = Dijkstra(2,4, G)
    D.runDijkstra()
    

if __name__ == "__main__":
    main()