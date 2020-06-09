import copy
from ctypes import *
import itertools
import math
from tqdm import tqdm
import os

if os.name == 'nt':
    libc = cdll.LoadLibrary("./linear_threshold_function/cpp/unweighted_ltf.dll")
    # libc = cdll.LoadLibrary("./cpp/unweighted_ltf.dll")
else:
    libc = cdll.LoadLibrary("./linear_threshold_function/cpp/unweighted_ltf.so")
libc.get_non_adaptive_cost_unit_cost.restype = c_double
libc.get_non_adaptive_cost_unit_cost.argtypes = (c_int, c_int, POINTER(c_double))
libc.get_non_adaptive_cost_arbitrary_cost.restype = c_double
libc.get_non_adaptive_cost_arbitrary_cost.argtypes = (c_int, c_int, POINTER(c_double), POINTER(c_int))


def get_non_adaptive_cost_unit_cost(k, n, p, order, display=False):
    p_with_order = [p[item] for item in order]

    p = [0] + p_with_order

    z = n - k + 1

    print("defining P ...") if display is True else False
    P = []
    P_row = []
    for _ in range(k + 1):
        P_row.append(1)
    for _ in range(n + 1):
        P.append(copy.deepcopy(P_row))
    for j in range(1, k + 1):
        P[0][j] = 0
    for i in range(1, n + 1):
        P_i_0 = 1
        for ii in range(1, i + 1):
            P_i_0 *= 1 - p[ii]
        P[i][0] = P_i_0
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            if j > i:
                P[i][j] = 0
            else:
                P[i][j] = P[i - 1][j - 1] * p[i] + P[i - 1][j] * (1 - p[i])

    print("defining Q ...") if display is True else False
    Q = []
    Q_row = []
    for _ in range(z + 1):
        Q_row.append(1)
    for _ in range(n + 1):
        Q.append(copy.deepcopy(Q_row))
    for j in range(1, z + 1):
        Q[0][j] = 0
    for i in range(1, n + 1):
        Q_i_0 = 1
        for ii in range(1, i + 1):
            Q_i_0 *= p[ii]
        Q[i][0] = Q_i_0
    for i in range(1, n + 1):
        for j in range(1, z + 1):
            if j > i:
                Q[i][j] = 0
            else:
                Q[i][j] = Q[i - 1][j - 1] * (1 - p[i]) + Q[i - 1][j] * p[i]

    print("summing Cost ...") if display is True else False
    cost = 0
    for i in range(1, n + 1):
        # print("P[" + str(i-1) + "][" + str(k-1) + "]")
        # print("P[" + str(i-1) + "][" + str(z-1) + "]")
        tmp = (P[i - 1][k - 1] * p[i] + Q[i - 1][z - 1] * (1 - p[i])) * i
        cost += tmp
        # print(P[i - 1][k - 1], p[i], Q[i - 1][z - 1], 1-p[i])
        # print(cost)

    print(cost) if display is True else False

    return cost


def get_non_adaptive_cost_arbitrary_cost(k, n, p, c, order, display=False):
    p_with_order = [p[item] for item in order]
    p = [0] + p_with_order

    c_with_order = [c[item] for item in order]
    c = [0] + c_with_order

    z = n - k + 1

    print("defining P ...") if display is True else False
    P = []
    P_row = []
    for _ in range(k + 1):
        P_row.append(1)
    for _ in range(n + 1):
        P.append(copy.deepcopy(P_row))
    for j in range(1, k + 1):
        P[0][j] = 0
    for i in range(1, n + 1):
        P_i_0 = 1
        for ii in range(1, i + 1):
            P_i_0 *= 1 - p[ii]
        P[i][0] = P_i_0
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            if j > i:
                P[i][j] = 0
            else:
                P[i][j] = P[i - 1][j - 1] * p[i] + P[i - 1][j] * (1 - p[i])

    print("defining Q ...") if display is True else False
    Q = []
    Q_row = []
    for _ in range(z + 1):
        Q_row.append(1)
    for _ in range(n + 1):
        Q.append(copy.deepcopy(Q_row))
    for j in range(1, z + 1):
        Q[0][j] = 0
    for i in range(1, n + 1):
        Q_i_0 = 1
        for ii in range(1, i + 1):
            Q_i_0 *= p[ii]
        Q[i][0] = Q_i_0
    for i in range(1, n + 1):
        for j in range(1, z + 1):
            if j > i:
                Q[i][j] = 0
            else:
                Q[i][j] = Q[i - 1][j - 1] * (1 - p[i]) + Q[i - 1][j] * p[i]

    print("summing Cost ...") if display is True else False
    cost = 0
    for i in range(1, n + 1):
        # print("P[" + str(i-1) + "][" + str(k-1) + "]")
        # print("P[" + str(i-1) + "][" + str(z-1) + "]")
        tmp = (P[i - 1][k - 1] * p[i] + Q[i - 1][z - 1] * (1 - p[i])) * sum(c[:i + 1])
        cost += tmp
        # print(P[i - 1][k - 1], p[i], Q[i - 1][z - 1], 1-p[i])
        # print(cost)

    print(cost) if display is True else False

    return cost


def c_get_non_adaptive_cost_unit_cost(k, n, p, order):
    p_with_order = [p[item] for item in order]
    return libc.get_non_adaptive_cost_unit_cost(k, n, (c_double * n)(*p_with_order))


def c_get_non_adaptive_cost_arbitrary_cost(k, n, p, c, order):
    p_with_order = [p[item] for item in order]
    c_with_order = [c[item] for item in order]
    return libc.get_non_adaptive_cost_arbitrary_cost(k, n, (c_double * n)(*p_with_order),
                                                     (c_int * n)(*c_with_order))


def get_optimal_non_adaptive_cost(k, n, p, c, cost_type):
    min_cost = math.inf
    min_order = None
    if cost_type == 'unit':
        for order in list(itertools.permutations(range(len(p)))):
            tmp_cost = get_non_adaptive_cost_unit_cost(k, n, p, order)
            if tmp_cost < min_cost:
                min_cost = tmp_cost
                min_order = order
        return min_cost, min_order
    elif cost_type == 'arbitrary':
        for order in list(itertools.permutations(range(len(p)))):
            tmp_cost = get_non_adaptive_cost_arbitrary_cost(k, n, p, c, order)
            if tmp_cost < min_cost:
                min_cost = tmp_cost
                min_order = order
        return min_cost, min_order
    else:
        raise Exception("cost_type error")


# for _ in tqdm(range(1000000)):
#     c_get_non_adaptive_cost_unit_cost(3, 5, [0.1, 0.1, 0.5, 0.9, 0.9], [0, 1, 2, 3, 4])
# # for _ in tqdm(range(1000000)):
# #     get_non_adaptive_cost_unit_cost(3, 5, [0.1, 0.1, 0.5, 0.9, 0.9], [0, 1, 2, 3, 4])
# # for _ in tqdm(range(1000000)):
# #     c_get_non_adaptive_cost_arbitrary_cost(3, 5, [0.1, 0.1, 0.5, 0.9, 0.9],[1,1,2,2,1], [0, 1, 2, 3, 4])
# # for _ in tqdm(range(1000000)):
# #     get_non_adaptive_cost_arbitrary_cost(3, 5, [0.1, 0.1, 0.5, 0.9, 0.9],[1,1,2,2,1], [0, 1, 2, 3, 4])
# print(c_get_non_adaptive_cost_unit_cost(3, 5, [0.1, 0.1, 0.5, 0.9, 0.9], [4, 0, 1, 2, 3]))
# print(get_non_adaptive_cost_unit_cost(3, 5, [0.1, 0.1, 0.5, 0.9, 0.9], [4, 0, 1, 2, 3]))
