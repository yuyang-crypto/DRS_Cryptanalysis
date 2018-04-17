"""statitical attack against DRS with trained models."""

import random
from numpy import zeros, int64, float64, array
from numpy.linalg import lstsq
import sys
import ctypes
import _ctypes
import matplotlib.pyplot as plt
from math import sqrt
from copy import copy

# System params

n = 912
D = n
b = 28
Nb = 16
N1 = 432

# Global attack param
features = 7


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


def generate_leak(S, samples):

    lib.init_stats()
    lib.sample_many(c_long_ptr(S), samples)

    feature_matrices = []
    for d in range(features):
        mat = zeros((n, n), dtype=float64)
        lib.export_feature_matrix(c_long_ptr(mat), d)

        feature_matrices += [mat, mat.transpose()] if d != 0 else [mat]

    return feature_matrices


idx_range = xrange(10)  # instance indices
samples = 200000  # sample size per instance

for idx in idx_range:
    print "current instance", idx
    S = KeyGen()
    with open("attack/data/S%d.dat" % idx, "a") as file:
        for i in range(n):
            for j in range(n):
                print>> file, S[i, j], " ",
            print>> file

    SS = copy(S)
    for i in range(n):
        SS[i, i] = 0
    Sv = abs(SS[0]) / max(abs(SS[0]))

    mom = generate_leak(S, samples)
    print "sampled ", samples
    guess = zeros((n, n), dtype=float64)  # predicted weights
    guess_sign = zeros((n, n), dtype=float64)  # the guesses of signs
    guess_v = zeros(n, dtype=float64)  # diagonal weights

    for j in range(1, n):
        # Load model
        if j < n / 2:
            f_mod = [-48.364026274970186, 354.97880341243166, -21.25736730213228, -289.1598151475356, 6.6580718153056893,\
                    58.714890352244808, 3.5597628551444984, -3.7709174933091134, 1.0255100487142101,\
                    -2.9137660813109889, 0.48345680620438714, 2.3777128962066225, -0.36369410178854267]
        else:
            f_mod = [-67.978135679162492, 324.84415957709655, -9.0923411348513952, -248.78815989534596, 3.1639153880021809,\
                    44.626793679338022, -0.81451246605513461, -4.1115747857187088, 0.52042559601807881,\
                    -2.6162619223764345, 0.34860216847098613, 2.8287948283611168, 0.4920230967120176]
        # calculate the value of f
        for i in range(n):
            l = (i + j) % n
            for k in range(2 * features - 1):
                guess[i, l] += f_mod[k] * mom[k][i, l]

    with open("attack/data/guess%d_%d.dat" % (idx, samples), "a") as file:
        for i in range(n):
            for j in range(n):
                print>> file, guess[i, j], " ",
            print>> file

    for j in range(1, n):
        for i in range(n):
            l = (i + j) % n
            guess_v[j] += guess[i, l]**2
            if guess[i, l] >= 0:
                guess_sign[i, l] = 1
            else:
                guess_sign[i, l] = -1

    # graph for locations
    plt.plot(Sv, 'g')
    for i in range(2):
        x = max(1, i * n / 2)
        y = (i + 1) * n / 2
        guess_v[x: y] /= max(guess_v[x: y])
    plt.plot(guess_v, 'r')
    plt.savefig("attack/graph/W%d_%d.svg" % (idx, samples), dpi=1500)
    plt.close("all")

    # statistics for sign prediction
    cnt_l = 0
    cnt_u = 0
    correct_l = 0
    correct_u = 0
    for j in range(1, n):
        for i in range(n):
            l = (i + j) % n
            if abs(S[i, l]) != b:
                continue
            if l < i:
                cnt_l += 1
                if guess_sign[i, l] * S[i, l] > 0:
                    correct_l += 1
            else:
                cnt_u += 1
                if guess_sign[i, l] * S[i, l] > 0:
                    correct_u += 1
    rate_l = correct_l * 1. / cnt_l  # correct sign-prediction rate for large coefficients in the lower-triangle part
    rate_u = correct_u * 1. / cnt_u  # correct sign-prediction rate for large coefficients in the upper-triangle part
    with open("attack/data/stat%d.dat" % idx, "a") as file:
        print>> file, samples
        print>> file, correct_l, cnt_l, rate_l
        print>> file, correct_u, cnt_u, rate_u
