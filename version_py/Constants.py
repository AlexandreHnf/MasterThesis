W = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\MasterThesis\\version_py\\"

# Graphs
GRAPH_1_NAME =          "1_ULB"
GRAPH_2_NAME =          "2_Bruxelles"
GRAPH_3_NAME =          "3_Bruxelles_Capitale_centre"
GRAPH_4_NAME =          "4_Bruxelles_Capitale"
GRAPH_5_NAME =          "5_Belgique_centre"
GRAPH_6_NAME =          "6_Belgique"

GRAPH_ULB =             W + "Graphs\\" + GRAPH_1_NAME + ".json"
GRAPH_BXL =             W + "Graphs\\" + GRAPH_2_NAME + ".json"
GRAPH_BXL_CAP_CTR =     W + "Graphs\\" + GRAPH_3_NAME + ".json"
GRAPH_BXL_CAP =         W + "Graphs\\" + GRAPH_4_NAME + ".json"
GRAPH_BE_CTR =          W + "Graphs\\" + GRAPH_5_NAME + ".json"
GRAPH_BE =              W + "Graphs\\" + GRAPH_6_NAME + ".json"

GRAPH_FILENAMES =      {GRAPH_1_NAME : GRAPH_ULB,
                        GRAPH_2_NAME : GRAPH_BXL,
                        GRAPH_3_NAME : GRAPH_BXL_CAP_CTR,
                        GRAPH_4_NAME : GRAPH_BXL_CAP,
                        GRAPH_5_NAME : GRAPH_BE_CTR,
                        GRAPH_6_NAME : GRAPH_BE}

GRAPH_VILLO =           W + "Graphs\\" + "villo.json"
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

EXPERIMENT =            3
NB_RUNS =               10  # TODO : change it to 1000

# experiments stats filenames /!\ TENTATIVE => change it to be generic

FILE_EXP1 =         W + "Benchmarks\\Exp1\\"
FILE_EXP2 =         W + "Benchmarks\\Exp2\\"
FILE_EXP3 =         W + "Benchmarks\\Exp3\\"
FILE_EXP4 =         W + "Benchmarks\\Exp4\\"
FILE_EXP5 =         W + "Benchmarks\\Exp5\\"
FILE_EXP6 =         W + "Benchmarks\\Exp6\\"
FILE_EXP7 =         W + "Benchmarks\\Exp7\\"
FILE_EXP8 =         W + "Benchmarks\\Exp8\\"
