"""generating training set."""

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

# Global attack param
feature_count = 7

# Input
n = int(sys.argv[1])
expo = int(sys.argv[2])
keys_start = int(sys.argv[3])  # included
keys_end = int(sys.argv[4])  # excluded

def RandomSign():
    return random.randint(0, 1) * 2 - 1

def KeyGen(n, D, idx):
    fin = open("./sk/" + str(n) + "_" + str(idx))
    S = zeros((n, n), dtype=int64)
    row = 0
    for line in fin:
        if line == "":
            break
        col = 0
        for d in line.split():
            S[row, col] = int(d)
            if row == col:
                S[row, col] += D
            col += 1
        row += 1
    return S


def c_double_ptr(x):
    return x.ctypes.data_as(ctypes.POINTER(ctypes.c_double))


def c_long_ptr(x):
    return x.ctypes.data_as(ctypes.POINTER(ctypes.c_int))


def generate_training(n, D, idx, expo):
    S = KeyGen(n, D, idx)
    print "Key Generated"

    lib.init_stats()

    Samples_per_key = 2 ** expo

    lib.sample_many(c_long_ptr(S), Samples_per_key)
    print "Sampling done"

    if not os.path.exists('./training/%d_%d/%d' % (n, expo, idx)):
        os.makedirs('./training/%d_%d/%d' % (n, expo, idx))

    feature_matrices = []
    for d in range(feature_count):
        mat = zeros((n, n), dtype=float64)
        lib.export_feature_matrix(c_long_ptr(mat), d)
        feature_matrices += [mat, mat.transpose()] if d > 0 else [mat]
    print "data collected"

    for j in xrange(n):
        with open("training/%d_%d/%d/j%d.dat" % (n, expo, idx, j), "a") as file:
            for i in range(n):
                l = (i + j) % n
                v = [float("%.6e" % (M[i, l])) for M in feature_matrices]
                D = {"s": S[i, l], "leak": v}
                print >>file, D

    print "stored to files"


D = n
# keys_start = 0
# keys_end = 5
lib = ctypes.cdll.LoadLibrary("./clib/signlib%d.so" % n)
lib.init_stats()
for k in range(keys_start, keys_end):
    print
    print "Key ", k, " / ", keys_end
    generate_training(n, D, k, expo)
