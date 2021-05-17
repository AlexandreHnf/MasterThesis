from Constants import *
from ParseOSMgraph import OSMgraphParser
from ShortestPathExperiments import *

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
        p.showStats()

        a = sys.argv

        if a[1] == "Dijkstra":  # 1: Dijkstra, 2: graph, 3:s, 4:t, 5: queue_type 6:show
            print(int(a[3]), int(a[4]))
            testDijkstra(graph, int(a[3]), int(a[4]), a[5], a[6])
        elif a[1] == "BidiDijkstra":  # 1: Dijkstra, 2: graph, 3:s, 4:t, 5: queue_type 6:show
            testBidiDijkstra(graph, int(a[3]), int(a[4]), a[5], a[6])
        elif a[1] == "Astar":  # 1: Astar, 2: graph, 3:s, 4:t, 5: queue_type, 6:heuristic, 7:show
            testAstar(graph, int(a[3]), int(a[4]), a[5], a[6], a[7])
        elif a[1] == "BidiAstar":  # 1: BidiAstar, 2:graph, 3:s, 4:t, 5: queue_type, 6:heuristic, 7:show
            testBidiAstar(graph, int(a[3]), int(a[4]), a[5], a[6], a[7])
        elif a[1] == "ALT":  # 1: ALT, 2:graph, 3:s, 4:t, 5:lm_select, 6:queue_type, 7: heuristic, 8:show
            testALT(graph, int(a[3]), int(a[4]), a[5], a[6], a[7], a[8])
        elif a[1] == "BidiALT":  # 1: BidiALT, 2:graph, 3:s, 4:t, 5:lm_select, 6:queue_type, 7:heuristic, 8:show
            testBidiALT(graph, int(a[3]), int(a[4]), a[5], a[6], a[7], a[8])
    else:
        print("not enough arguments")
        runAllSP(7, 1335)


def runAllSP(s, t):
    p = OSMgraphParser(GRAPH_BXL_CTR_TEST)
    graph = p.parse()
    p.showStats()

    testDijkstra(graph, s, t)
    testAstar(graph, s, t)
    testALT(graph, s, t, "planar", "bin", "euclidean", True)

    # bidirectional
    testBidiDijkstra(graph, s, t)
    testBidiAstar(graph, s, t)
    testBidiALT(graph, s, t, "planar", "bin", "euclidean")


def testLandmark():
    p = OSMgraphParser(GRAPH_BXL_CTR_TEST)
    graph = p.parse()
    # =========================================
    testLandmarks(graph, "random")


# ==================================================================
def main():
    runAllSP(7, 1335)
    # testLandmark()
    # =========================================
    # processArgs()


if __name__ == "__main__":
    main()
