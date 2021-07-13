from Constants import *
from ParseOSMgraph import OSMgraphParser
from ShortestPathExperiments import *
from Experiments import *

import sys


# TODO : add launchExperiments of "Experiments.py" to main
# TODO : deal with paths of Windows + Uubuntu when using argv

##############################################################################################

def processArgs():
    """
    main.py <Dijkstra, BidiDijkstra, Astar, BidiAstar> <graph file> <start> <dest>  <priority queue> <show>
    main.py <ALT/BidiALT> <priority queue> <start> <dest> <graph file>
    <show> : S or NS (show or not show)

    /!\ graph file in ubuntu path : ex: Graphs/2_Bruxelles.json
    """
    print(sys.argv[0])
    algos = ["Dijkstra", "BidiDijkstra", "Astar", "BidiAstar", "ALT", "BidiALT", "MMDijkstra"]

    if len(sys.argv) > 1:

        a = sys.argv

        if sys.argv[1] in algos:
            p = OSMgraphParser(sys.argv[2])
            graph = p.parse()
            p.showStats()

            if a[1] == "Dijkstra":  # 1: Dijkstra, 2: graph, 3:s, 4:t, 5: queue_type 6:show
                print(int(a[3]), int(a[4]))
                testDijkstra(graph, int(a[3]), int(a[4]), a[5], a[6])
            elif a[1] == "BidiDijkstra":  # 1:Dijkstra, 2:graph, 3:s, 4:t, 5:queue_type 6:show
                testBidiDijkstra(graph, int(a[3]), int(a[4]), a[5], a[6])
            elif a[1] == "Astar":  # 1:Astar, 2:graph, 3:s, 4:t, 5: queue_type, 6:heuristic, 7:show
                testAstar(graph, int(a[3]), int(a[4]), a[5], a[6], a[7])
            elif a[1] == "BidiAstar":  # 1: BidiAstar, 2:graph, 3:s, 4:t, 5: queue_type, 6:heuristic, 7:show
                testBidiAstar(graph, int(a[3]), int(a[4]), a[5], a[6], a[7])
            elif a[1] == "ALT":  # 1: ALT, 2:graph, 3:s, 4:t, 5:lm_select, 6:queue_type, 7:heuristic, 8:show
                testALT(graph, int(a[3]), int(a[4]), a[5], a[6], a[7], a[8])
            elif a[1] == "BidiALT":  # 1: BidiALT, 2:graph, 3:s, 4:t, 5:lm_select, 6:queue_type, 7:heuristic, 8:show
                testBidiALT(graph, int(a[3]), int(a[4]), a[5], a[6], a[7], a[8])
            elif a[1] == "MMDijkstra":  # 1: Dijkstra, 2: graph, 3:s, 4:t, 5: queue_type 6:show
                testMMDijkstra(graph, int(a[3]), int(a[4]), a[5], a[6])

        else:
            if a[1] == "runAllExperiments":
                launchAllExperiments()
            elif a[1] == "runExperiment":
                launchExperiment(a[2])  # 1: runExperiment, 2: experiment nb

    else:
        print("not enough arguments")
        runAllSP(7, 1335)


def runAllSP(s, t):
    p = OSMgraphParser(GRAPH_BXL)
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
    p = OSMgraphParser(GRAPH_BXL)
    graph = p.parse()
    # =========================================
    testLandmarks(graph, "random")


# ==================================================================
def main():
    # runAllSP(7, 1335)
    # testLandmark()
    # =========================================
    #processArgs()

    # =========================================
    p = OSMgraphParser(GRAPH_BXL)
    graph = p.parse()
    testMMDijkstra(graph, 7, 1335, "bin", False)


if __name__ == "__main__":
    main()
