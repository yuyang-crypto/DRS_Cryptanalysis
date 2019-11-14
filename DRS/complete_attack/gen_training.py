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

# System params

n = 912
D = n
b = 28
Nb = 16
N1 = 432

# Global attack param

feature_count = 7

# Training set params

Samples_per_key = int(sys.argv[1])
keys_start = int(sys.argv[2])  # included
keys_end = int(sys.argv[3])  # excluded


def RandomSign():
    return random.randint(0, 1) * 2 - 1


def KeyGen():
    L = Nb * [b] + N1 * [1] + (n - 1 - Nb - N1) * [0]
    random.shuffle(L)
    t = [D] + L
    S = zeros((n, n), dtype=int64)

    for i in xrange(n):
        S[i, i] = t[0]
        for j in xrange(1, n):
            S[i, (i + j) % n] = t[j] * RandomSign()
    return S


def c_double_ptr(x):
    return x.ctypes.data_as(ctypes.POINTER(ctypes.c_double))


def c_long_ptr(x):
    return x.ctypes.data_as(ctypes.POINTER(ctypes.c_int))

lib = ctypes.cdll.LoadLibrary("./signlib.so")
lib.init_stats()


def generate_training(append):

    S = KeyGen()
    print "Key Generated"

    lib.sample_many(c_long_ptr(S), Samples_per_key)
    print "Sampling done"

    feature_matrices = []
    for d in range(feature_count):
        mat = zeros((n, n), dtype=float64)
        lib.export_feature_matrix(c_long_ptr(mat), d)

        feature_matrices += [mat, mat.transpose()] if d != 0 else [mat]
    print "data collected"

    for j in xrange(1, n):
        mode = "a" if append else "w"
        with open("training/j%d.dat" % j, mode) as file:
            for i in range(n):
                l = (i + j) % n
                v = [float("%.4e" % (M[i, l])) for M in feature_matrices]
                D = {"i": i, "j": j, "l": l, "s": S[i, l], "leak": v}
                print >>file, D

    print "stored to files"


if os.path.exists('./training') == False:
    os.makedirs('./training')
for k in range(keys_start, keys_end):
    print
    print "Key ", k, " / ", keys_end
    generate_training(k > 0)
