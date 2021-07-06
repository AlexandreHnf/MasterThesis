W = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\MasterThesis\\version_py\\Graphs\\"

# Graphs
GRAPH_ULB =             W + "1_ULB.json"
GRAPH_BXL =             W + "2_Bruxelles.json"
GRAPH_BXL_CAP_CTR =     W + "3_Bruxelles_Capitale_centre.json"
GRAPH_BXL_CAP =         W + "4_Bruxelles_Capitale.json"
GRAPH_BE_CTR =          W + "5_Belgique_centre.json"
GRAPH_BE =              W + "6_Belgique.json"

GRAPH_VILLO =           W + "villo.json"
SPEED_LIMIT_FOOT =      5

# Benchmarks parameters
# TODO : faire un graph artificial (comme dans goldberg et al. when Astar meets grpah theory)
GRAPH =                 GRAPH_BXL
PRIORITY =              "bin"
HEURISTIC =             "euclidean"
LANDMARK_SELECTION =    "planar"
NB_LANDMARKS =          16
BUCKET_SIZE =           40
SEED =                  -1
ENCODING =              'utf-8'
SHOW =                  False

EXPERIMENT =            2
NB_RUNS =               10  # TODO : change it to 1000