#!/usr/bin/env python
# -*- coding: utf-8 -*-


W = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\MasterThesis\\version_py\\"

earthRadiusKm = 6371

limit_connection_ratio = 0.5

# ================================
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
SPEED_BIKE =            25  # km/h https://cyclinguphill.com/average-speeds-cycling/
NOT_VALID_MAXSPEEDS =   not_valid = ["signals",
                                     "variable",
                                     "30; 50",
                                     "50;30",
                                     "50; 30; 50",
                                     "30;70",
                                     "FR:urban",
                                     "BE:urban"]


# ================================
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

# ================================
# Exp 7 - multimodal public transport
SPEEDS =                [0.1, 15, 30, 90, 1e10]
SPEEDS_LABELS =         {0.1: "0.1 km/h (~0)",
                         15: "15 km/h (bus/tram)",
                         30: "30 km/h (metro)",
                         90: "90 km/h (train)",
                         1e10: "1e10 km/h (~inf.)"}
ADDED_EDGES =           [0, 10, 50, 100, 200, 600, 1000]
FOOT_PUBLIC_TRANSPORT = ["foot", "Public Transport"]
EXP7_GRAPH =            4

# ================================
# EXP 8
EXP8_GRAPHS =           [1, 2, 3, 4, 5]
FOOT_VILLO =            ["foot", "toStation", "fromStation", "Villo"]
CAR_VILLO =             ["Villo", "toStation", "fromStation", "car"]

TO_STATION_COST =       60
FROM_STATION_COST =     60

# ================================
# EXP 9 & 10
C1 = 0
C2 = 1
PREF_RANGE =            [2, 0]
PREF_STEP =             -0.2
EXP9_GRAPHS =           [1, 2, 3]
EXP9_CATEGORIES =       {"1_ULB": "1 ULB",
                         "2_Bruxelles": "2 Bxl",
                         "3_Bruxelles_Capitale_centre": "3 Bxl Cap ctr",
                        }

PRICE_VILLO =           0       # 0 €

GAS_PRICE_KM =          1.4  # € / L
CAR_CONSUMPTION =       7    # L / 100km

EXP10_GRAPH =           3
EXP10_CATEGORIES =      {"00": "F:c1, E:low",
                         "01": "F:c1, E:high",
                         "02": "F:c1, E:middle",
                         "10": "F:c2, E:low",
                         "11": "F:c2, E:high",
                         "12": "F:c2, E:middle"}


# ================================
EXPERIMENTS =           [10]
NB_RUNS =               200

# ================================
# Visualization parameters
EXPERIMENT_PLOT =       8
KEPT_GRAPHS =           [0, 1, 2]
MARKERS =               ["s", "*", "x", "v", "^", "o", "d", "p"]
MARKER_SIZE =           20