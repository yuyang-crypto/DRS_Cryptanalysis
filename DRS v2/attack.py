"""statitical attack against DRS."""

import random
from numpy import zeros, int64, float64, array
from numpy.linalg import lstsq
import sys
import ctypes
import _ctypes
import matplotlib.pyplot as plt
from math import sqrt
from copy import copy

import os

# Global attack param
features = 7

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


def generate_leak(S, samples):

    lib.init_stats()
    lib.sample_many(c_long_ptr(S), samples)

    feature_matrices = []
    for d in range(features):
        mat = zeros((n, n), dtype=float64)
        lib.export_feature_matrix(c_long_ptr(mat), d)

        feature_matrices += [mat, mat.transpose()] if d > 0 else [mat]

    return feature_matrices


def load_models(expo):
    X = []
    for j in range(n):
	if j == 0:
            with open("model/%d_%d/on-diag.mod" % (n, expo), "r") as file:
                for line in file:
                    X += [eval(line)]
	else:
            with open("model/%d_%d/off-diag.mod" % (n, expo), "r") as file:
                for line in file:
                    X += [eval(line)]
    return X


D = n
idx_range = xrange(keys_start, keys_end)  # instance indices

if os.path.exists('./attack/data%d' % n) == False:
    os.makedirs('./attack/data%d' % n)

lib = ctypes.cdll.LoadLibrary("./clib/signlib%d.so" % n)

samples = 2 ** expo
for idx in idx_range:
    print "current instance", idx
    S = KeyGen(n, D, idx)
    with open("attack/data%d/S%d.dat" % (n, idx), "w") as file:
        for i in range(n):
            for j in range(n):
                print>> file, S[i, j], " ",
            print>> file

    mom = generate_leak(S, samples)
    print "sampled ", samples
    guess = zeros((n, n), dtype=float64)  # predicted weights

    # load models
    f_mod = load_models(expo)

    for j in range(n):
        # calculate the value of f
        for i in range(n):
            l = (i + j) % n
            for k in range(2 * features - 1):
                guess[i, l] += f_mod[j][k] * mom[k][i, l]

    with open("attack/data%d/guess%d_%d.dat" % (n, idx, samples), "w") as file:
        for i in range(n):
            for j in range(n):
                print>> file, guess[i, j], " ",
            print>> file
