#!/usr/bin/env python
# -*- coding: utf-8 -*-


W = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\MasterThesis\\version_py\\"

earthRadiusKm = 6371

limit_connection_ratio = 0.5

# Graphs
GRAPH_ULB =             "1_ULB"
GRAPH_BXL =             "2_Bruxelles"
GRAPH_BXL_CAP_CTR =     "3_Bruxelles_Capitale_centre"
GRAPH_BXL_CAP =         "4_Bruxelles_Capitale"
GRAPH_BE_CTR =          "5_Belgique_centre"
GRAPH_BE =              "6_Belgique"

GRAPHS =                [GRAPH_ULB,
                         GRAPH_BXL,
                         GRAPH_BXL_CAP_CTR,
                         GRAPH_BXL_CAP,
                         GRAPH_BE_CTR,
                         GRAPH_BE]

GRAPH_VILLO =           "villo"


SPEED_FOOT =            5   # km/h
SPEED_BIKE =            20  # km/h https://cyclinguphill.com/average-speeds-cycling/
NOT_VALID_MAXSPEEDS =   not_valid = ["signals",
                                     "variable",
                                     "30; 50",
                                     "50;30",
                                     "50; 30; 50",
                                     "30;70",
                                     "FR:urban",
                                     "BE:urban"]


# Benchmarks parameters
GRAPH =                 GRAPH_BXL

PRIORITY =              "bin"
HEURISTIC =             "euclidean"
LANDMARK_SELECTION =    "planar"
NB_LANDMARKS =          16
BUCKET_SIZE =           40

SEED =                  -1
ENCODING =              'utf-8'
SHOW =                  False

GAS_PRICE_KM =          1.4  # € / L
CAR_CONSUMPTION =       7    # L / 100km

# Exp 7 - multimodal public transport
SPEEDS =                [0.1, 15, 30, 90, 1e10]
# ADDED_EDGES =           [0, 10, 50, 100, 200]
ADDED_EDGES =           [0, 10, 50, 100, 200, 600, 1000]
FOOT_PUBLIC_TRANSPORT = ["foot", "Public Transport"]
EXP7_GRAPH =            4

# EXP 8
EXP8_GRAPHS =           [1, 2, 3, 4, 5]
FOOT_VILLO =            ["foot", "toStation", "fromStation", "Villo"]
CAR_VILLO =             ["foot", "toStation", "fromStation", "car"]


TO_STATION_COST =       60
FROM_STATION_COST =     60

EXPERIMENTS =           [1]
NB_RUNS =               500

# Visualization parameters
EXPERIMENT_PLOT =       8
KEPT_GRAPHS =           [0, 1, 2, 3, 4, 5]
MARKERS =               ["s", "*", "x", "v", "^", "o", "d", "p"]
MARKER_SIZE =           20