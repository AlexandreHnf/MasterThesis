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