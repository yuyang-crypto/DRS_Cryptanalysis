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

idx_range = range(5)

# Input
n = int(sys.argv[1])
expo = int(sys.argv[2])
keys_start = int(sys.argv[3])  # included
keys_end = int(sys.argv[4])  # excluded

block_count = 1
blocks = [[0]]
# block_count = n
# blocks = []
for i in range(block_count):
    a = max(1, i * n / block_count)
    # a = i * n / block_count
    b = (i + 1) * n / block_count
    blocks += [range(a, b)]
print blocks

if not os.path.exists('./model/%d_%d' % (n, expo)):
    os.makedirs('./model/%d_%d' % (n, expo))

for block in blocks:
    b = []
    A = []
    for idx in range(keys_start, keys_end):
        for j in block:
            print j,
            with open("training/%d_%d/%d/j%d.dat" % (n, expo, idx, j), "r") as file:
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

    x = [y for y in x]
    print x
    
    if block == [0]:
        with open("model/%d_%d/on-diag.mod" % (n, expo), "w") as file:
            print >>file, x
    else:
        with open("model/%d_%d/off-diag.mod" % (n, expo), "w") as file:
            print >>file, x
    gc.collect()
