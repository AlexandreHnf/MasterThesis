W = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\MasterThesis\\version_py\\"

# Graphs
GRAPH_ULB =             W + "Graphs\\" + "1_ULB.json"
GRAPH_BXL =             W + "Graphs\\" + "2_Bruxelles.json"
GRAPH_BXL_CAP_CTR =     W + "Graphs\\" + "3_Bruxelles_Capitale_centre.json"
GRAPH_BXL_CAP =         W + "Graphs\\" + "4_Bruxelles_Capitale.json"
GRAPH_BE_CTR =          W + "Graphs\\" + "5_Belgique_centre.json"
GRAPH_BE =              W + "Graphs\\" + "6_Belgique.json"

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

EXPERIMENT =            4
NB_RUNS =               10  # TODO : change it to 1000

# experiments stats filenames /!\ TENTATIVE => change it to be generic
FILENAME_EXP1 = W + "Benchmarks\\Exp1\\" + "2_Bruxelles_exp1.csv"
FILENAME_EXP2 = W + "Benchmarks\\Exp2\\" + "2_Bruxelles_exp2.csv"
FILENAME_EXP3 = W + "Benchmarks\\Exp3\\" + "2_Bruxelles_exp3.csv"
FILENAME_EXP4 = W + "Benchmarks\\Exp4\\" + "2_Bruxelles_exp4.csv"