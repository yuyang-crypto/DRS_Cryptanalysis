import random
from numpy import zeros, int64, float64
from numpy.linalg import lstsq
import sys
import ctypes
import _ctypes
import matplotlib.pyplot as plt
from math import sqrt
from copy import copy
import os


def RandomSign():
    return random.randint(0, 1) * 2 - 1

def RandomSample(n, D, k):
    """Generate x_1 + ... + x_{k} < D where x_i > 0."""
    Domain = range(1, D)
    random.shuffle(Domain)
    Xlist = Domain[: k]
    Xlist.sort()
    Tuple = []
    Tuple += [Xlist[0]]
    for i in range(1, k):
        Tuple += [(Xlist[i] - Xlist[i - 1]) * RandomSign()]
    Tuple += [0] * (n - k)
    random.shuffle(Tuple)
    return Tuple

# for n in [32, 64, 128, 256, 512]:
for n in [16]:
    D = n
    # if not os.path.exists('./sk'):
    #     os.makedirs('./sk')
    fin = open("#nonzero/" + str(n))
    idx = 0
    for line in fin:
        if line == "":
            break
        data = line.split()
        fout = open("./" + str(n) + "_" + str(idx), "w")
        for d in data:
            k = int(d)
            Tuple = RandomSample(n, D, k)
            for t in Tuple:
                fout.write(str(t) + " ")
            fout.write("\n")
        idx += 1
