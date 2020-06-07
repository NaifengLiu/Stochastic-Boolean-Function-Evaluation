import copy
import itertools


def generate_all_adaptive_strategies(n, p_list=None):
    if p_list is None:
        p_list = range(n)
    if n == 3:
        def select_2_from_list(x):
            output = []
            for i in x:
                for j in x:
                    tmp = [i, j]
                    output.append(tmp)
            return output

        def make_path(left_over):
            for i in left_over:
                tmp_left_over = [j for j in left_over if j != i]
                yield [[i, list(tmp_left_over)]]

        strategies = list(make_path(p_list))
        for a in range(2 ** (n - 1) - 1):
            new_strategy = []
            for strategy in strategies:
                possible_children = select_2_from_list(strategy[a][1])
                for children in possible_children:
                    tmp_strategy = copy.deepcopy(strategy)
                    tmp_leftover_0 = copy.deepcopy(strategy)
                    tmp_leftover_1 = copy.deepcopy(strategy)
                    tmp_leftover_0[a][1].remove(children[0])
                    tmp_leftover_1[a][1].remove(children[1])
                    tmp_strategy.append([children[0], tmp_leftover_0[a][1]])
                    tmp_strategy.append([children[1], tmp_leftover_1[a][1]])
                    new_strategy.append(tmp_strategy)
            # print(new_strategy)
            strategies = new_strategy

        # remove redundancy
        strategies_output = []
        for strategy in strategies:
            tmp_line = []
            for item in strategy:
                tmp_line.append(item[0])
            strategies_output.append(tmp_line)

        # print(strategies_output)
        return strategies_output
    elif n > 3:
        final_output = []
        for item in range(n):
            previous = generate_all_adaptive_strategies(n-1, [j for j in range(n) if j != item])

            # modified_output = []
            for item_i in previous:
                for item_j in previous:
                    tmp_output = [item]
                    for a in range(n-1):
                        tmp_output += item_i[2**a-1: 2**(a+1)-1] + item_j[2**a-1: 2**(a+1)-1]
                    final_output.append(tmp_output)
        return final_output


def generate_all_non_adaptive_strategies(n):
    return list(itertools.permutations(range(n)))




