"""training model."""

import random
from numpy import zeros, int64, float64, concatenate, array
from numpy.linalg import lstsq
import sys
import ctypes
import _ctypes
import matplotlib.pyplot as plt
from math import sqrt
from copy import copy
import gc
import os

# System params

n = 912
D = n
b = 28
Nb = 16
N1 = 432

# Global attack param

block_count = 2
blocks = []
renormalize_lstsq = False  # True


if os.path.exists('./model') == False:
    os.makedirs('./model')

for i in range(block_count):
    a = max(1, i * n / block_count)
    b = (i + 1) * n / block_count
    blocks += [range(a, b)]

for block in blocks:
    b = []
    A = []

    for j in block:
        print j,
        with open("training/j%d.dat" % j, "r") as file:
            for line in file:
                D = eval(line)
                b += [D["s"]]
                A += [D["leak"]]

    print
    b = array(b)
    print b.shape
    A = array(A)
    print A.shape

    x = lstsq(A, b)[0]

    bb = A.dot(x)

    if renormalize_lstsq:
        f = max([abs(v) for v in bb]) / max([abs(v) for v in b])
        x = x * f

    x = [y for y in x]
    print x

    for j in block:
        with open("model/j%d.mod" % j, "w") as file:
            print >>file, x
    gc.collect()
