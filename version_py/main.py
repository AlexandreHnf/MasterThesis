from Constants import *
from parseOSMgraph import OSMgraphParser
from testSPalgos import *

import json
import csv
import sys


##############################################################################################

def processArgs():
    """
    main.py <Dijkstra, BidiDijkstra, Astar, BidiAstar> <graph file> <start> <dest>  <priority queue> <show>
    main.py <ALT/BidiALT> <priority queue> <start> <dest> <graph file>
    <show> : S or NS (show or not show)
    """
    print(sys.argv[0])

    if len(sys.argv) > 1:
        p = OSMgraphParser(sys.argv[2])
        graph = p.parse()
        rev_graph = p.getReverseGraph(graph)
        graph_coords = p.getNodes()
        p.showStats()

        if sys.argv[1] == "Dijkstra":  # 1: Dijkstra, 2: graph, 3:s, 4:t, 5: queue_type 6:show
            print(int(sys.argv[3]), int(sys.argv[4]))
            testDijkstra(graph, graph_coords, int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6])
        elif sys.argv[1] == "BidiDijkstra":  # 1: Dijkstra, 2: graph, 3:s, 4:t, 5: queue_type 6:show
            testBidiDijkstra(graph, rev_graph, graph_coords, int(sys.argv[3]), int(sys.argv[4]), sys.argv[5],
                             sys.argv[6])
        elif sys.argv[1] == "Astar":  # 1: Astar, 2: graph, 3:s, 4:t, 5: queue_type, 6:heuristic, 7:show
            testAstar(graph, graph_coords, int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6], sys.argv[7])
        elif sys.argv[1] == "BidiAstar":  # 1: BidiAstar, 2:graph, 3:s, 4:t, 5: queue_type, 6:heuristic, 7:show
            testBidiAstar(graph, rev_graph, graph_coords, int(sys.argv[3]), int(sys.argv[4]), sys.argv[5],
                          sys.argv[6], sys.argv[7])
        elif sys.argv[1] == "ALT":  # 1: ALT, 2:graph, 3:s, 4:t, 5:lm_select, 6:queue_type, 7: heuristic, 8:show
            testALT(graph, graph_coords, int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6],
                    sys.argv[7], sys.argv[8])
        elif sys.argv[1] == "BidiALT":  #1: BidiALT, 2:graph, 3:s, 4:t, 5:lm_select, 6:queue_type, 7:heuristic, 8:show
            testBidiALT(graph, rev_graph, graph_coords, int(sys.argv[3]), int(sys.argv[4]), sys.argv[5],
                        sys.argv[6], sys.argv[7], sys.argv[8])
    else:
        print("not enough arguments")
        runAllSP(7, 1335)

def runAllSP(s, t):
    p = OSMgraphParser(GRAPH_BXL_CTR_TEST)
    graph = p.parse()
    graph_coords = p.getNodes()
    p.showStats()

    testDijkstra(graph, graph_coords, s, t)
    testAstar(graph, graph_coords, s, t)
    testALT(graph, graph_coords, s, t, "planar", "bin", "euclidean", True)

    # bidirectional
    rev_graph = p.getReverseGraph(graph)
    testBidiDijkstra(graph, rev_graph, graph_coords, s, t)
    testBidiAstar(graph, rev_graph, graph_coords, s, t)
    testBidiALT(graph, rev_graph, graph_coords, s, t, "planar", "bin", "euclidean")

def testLandmark():
    p = OSMgraphParser(GRAPH_BXL_CTR_TEST)
    graph = p.parse()
    graph_coords = p.getNodes()
    # =========================================
    testLandmarks(graph, graph_coords, "random")

# ==================================================================
def main():

    runAllSP(7, 1335)
    # testLandmark()
    # =========================================
    # processArgs()



if __name__ == "__main__":
    main()
