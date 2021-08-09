#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import random
from Constants import *


def setSeed():
    seed = SEED
    if seed == -1:
        seed = time.time()
    random.seed(seed)
    print("SEED : ", seed)


def getRandomPair(irange):
    x, y = irange
    a = random.randint(x, y)
    b = random.randint(x, y)
    while a == b:
        a = random.randint(x, y)
        b = random.randint(x, y)

    return a, b


def selectRandomPair(nodes):
    a = random.choice(nodes)
    b = random.choice(nodes)
    while a == b:
        a = random.choice(nodes)
        b = random.choice(nodes)
    return a, b


def getRandomPairs(nodes, nb_runs):
    pairs = []
    for _ in range(nb_runs):
        s, t = selectRandomPair(nodes)
        pairs.append((s, t))
