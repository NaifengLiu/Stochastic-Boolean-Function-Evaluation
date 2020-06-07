import copy
from ctypes import *
import itertools
import math


# libc = cdll.LoadLibrary("./Linear-Threshold-Function.dll")
# libc.get_cost.restype = c_double
# libc.get_cost.argtypes = (c_int, c_int, POINTER(c_double), POINTER(c_int))


def get_non_adaptive_cost_unit_cost(k, n, p, w, order, display=False):
    p_with_order = [p[item] for item in order]
    w_with_order = [w[item] for item in order]

    p = [0] + p_with_order
    w = [0] + w_with_order

    W = sum(w)

    z = W - k + 1

    print("defining P ...") if display is True else False
    P = []
    P_row = []
    for _ in range(W + 1):
        P_row.append(0)
    for _ in range(n + 1):
        P.append(copy.deepcopy(P_row))
    for j in range(1, W + 1):
        P[0][j] = 0
    for i in range(1, n + 1):
        P_i_0 = 1
        for ii in range(1, i + 1):
            P_i_0 *= 1 - p[ii]
        P[i][0] = P_i_0
    P[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, W + 1):
            max_possible = 0
            for o in range(1, i+1):
                max_possible += w[o]
            if j > max_possible:
                P[i][j] = 0
            else:
                if j - w[i] >= 0:
                    P[i][j] = P[i - 1][j - w[i]] * p[i] + P[i - 1][j] * (1 - p[i])
                else:
                    P[i][j] = P[i - 1][j] * (1 - p[i])

    print("defining Q ...") if display is True else False
    Q = []
    Q_row = []
    for _ in range(W + 1):
        Q_row.append(0)
    for _ in range(n + 1):
        Q.append(copy.deepcopy(Q_row))
    for j in range(1, W + 1):
        Q[0][j] = 0
    for i in range(1, n + 1):
        Q_i_0 = 1
        for ii in range(1, i + 1):
            Q_i_0 *= p[ii]
        Q[i][0] = Q_i_0
    Q[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, W + 1):
            max_possible = 0
            for o in range(1, i + 1):
                max_possible += w[o]
            if j > max_possible:
                Q[i][j] = 0
            else:
                if j - w[i] >= 0:
                    Q[i][j] = Q[i - 1][j - w[i]] * (1 - p[i]) + Q[i - 1][j] * p[i]
                else:
                    Q[i][j] = Q[i - 1][j] * p[i]

    # for i in range(1, n+1):
    #     for j in range(0, W+1):
    #         print("P["+str(i)+"]["+str(j)+"] = " + str(P[i][j]))
    #
    # for i in range(1, n+1):
    #     for j in range(0, W+1):
    #         print("Q["+str(i)+"]["+str(j)+"] = " + str(Q[i][j]))

    print("summing Cost ...") if display is True else False
    cost = 0
    for i in range(1, n + 1):
        # print("P[" + str(i-1) + "][" + str(k-1) + "]")
        # print("P[" + str(i-1) + "][" + str(z-1) + "]")
        # tmp = (P[i - 1][k - 1] * p[i] + Q[i - 1][z - 1] * (1 - p[i])) * i
        # cost += tmp
        # print(P[i - 1][k - 1], p[i], Q[i - 1][z - 1], 1-p[i])
        # print(cost)

        tmp_p = 0
        tmp_q = 0
        for j in range(1, w[i] + 1):
            if k-j >= 0:
                tmp_p += P[i - 1][k - j]
            if z-j >= 0:
                tmp_q += Q[i - 1][z - j]
        tmp_p *= p[i]
        tmp_q *= 1 - p[i]

        pr = tmp_p + tmp_q

        cost += pr * i

    print(cost) if display is True else False

    return cost


def get_non_adaptive_cost_arbitrary_cost(k, n, p, c, w, order, display=False):
    p_with_order = [p[item] for item in order]
    w_with_order = [w[item] for item in order]
    c_with_order = [c[item] for item in order]

    p = [0] + p_with_order
    w = [0] + w_with_order
    c = [0] + c_with_order

    W = sum(w)

    z = W - k + 1

    print("defining P ...") if display is True else False
    P = []
    P_row = []
    for _ in range(W + 1):
        P_row.append(0)
    for _ in range(n + 1):
        P.append(copy.deepcopy(P_row))
    for j in range(1, W + 1):
        P[0][j] = 0
    for i in range(1, n + 1):
        P_i_0 = 1
        for ii in range(1, i + 1):
            P_i_0 *= 1 - p[ii]
        P[i][0] = P_i_0
    P[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, W + 1):
            max_possible = 0
            for o in range(1, i+1):
                max_possible += w[o]
            if j > max_possible:
                P[i][j] = 0
            else:
                if j - w[i] >= 0:
                    P[i][j] = P[i - 1][j - w[i]] * p[i] + P[i - 1][j] * (1 - p[i])
                else:
                    P[i][j] = P[i - 1][j] * (1 - p[i])

    print("defining Q ...") if display is True else False
    Q = []
    Q_row = []
    for _ in range(W + 1):
        Q_row.append(0)
    for _ in range(n + 1):
        Q.append(copy.deepcopy(Q_row))
    for j in range(1, W + 1):
        Q[0][j] = 0
    for i in range(1, n + 1):
        Q_i_0 = 1
        for ii in range(1, i + 1):
            Q_i_0 *= p[ii]
        Q[i][0] = Q_i_0
    Q[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, W + 1):
            max_possible = 0
            for o in range(1, i + 1):
                max_possible += w[o]
            if j > max_possible:
                Q[i][j] = 0
            else:
                if j - w[i] >= 0:
                    Q[i][j] = Q[i - 1][j - w[i]] * (1 - p[i]) + Q[i - 1][j] * p[i]
                else:
                    Q[i][j] = Q[i - 1][j] * p[i]

    # for i in range(1, n+1):
    #     for j in range(0, W+1):
    #         print("P["+str(i)+"]["+str(j)+"] = " + str(P[i][j]))
    #
    # for i in range(1, n+1):
    #     for j in range(0, W+1):
    #         print("Q["+str(i)+"]["+str(j)+"] = " + str(Q[i][j]))

    print("summing Cost ...") if display is True else False
    cost = 0
    for i in range(1, n + 1):
        # print("P[" + str(i-1) + "][" + str(k-1) + "]")
        # print("P[" + str(i-1) + "][" + str(z-1) + "]")
        # tmp = (P[i - 1][k - 1] * p[i] + Q[i - 1][z - 1] * (1 - p[i])) * i
        # cost += tmp
        # print(P[i - 1][k - 1], p[i], Q[i - 1][z - 1], 1-p[i])
        # print(cost)

        tmp_p = 0
        tmp_q = 0
        for j in range(1, w[i] + 1):
            if k-j >= 0:
                tmp_p += P[i - 1][k - j]
            if z-j >= 0:
                tmp_q += Q[i - 1][z - j]
        tmp_p *= p[i]
        tmp_q *= 1 - p[i]

        pr = tmp_p + tmp_q

        cost += pr * sum(c[:i+1])

    print(cost) if display is True else False

    return cost


def c_get_non_adaptive_cost(k, n, p, c, w, order):
    p_with_order = [p[item] for item in order]
    w_with_order = [w[item] for item in order]
    # print(p_with_order)

    # return libc.get_cost(k, n, (c_double * len(p_with_order))(*p_with_order), (c_int * len(w_with_order))(*w_with_order))
    return None


def get_optimal_non_adaptive_cost(k, n, p, c, w, cost_type):
    min_cost = math.inf
    min_order = None
    if cost_type == 'unit':
        for order in list(itertools.permutations(range(len(p)))):
            tmp_cost = get_non_adaptive_cost(k, n, p, w, order)
            if tmp_cost < min_cost:
                min_cost = tmp_cost
                min_order = order
        return min_cost, min_order


# print(get_non_adaptive_cost(5, 5, [0.2, 0.25, 0.5, 0.75, 0.8], [1, 2, 3, 1, 1], [0, 1, 2, 3, 4]))
# print(c_get_non_adaptive_cost(5, 5, [0.2, 0.25, 0.5, 0.75, 0.8], [1, 2, 3, 1, 1], [0, 1, 2, 3, 4]))
