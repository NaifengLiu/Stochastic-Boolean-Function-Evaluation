from BinaryTree import Node as BNode
import sympy
import math
from tqdm import tqdm


class Node:
    def __init__(self, index, leaf=False, value=None):
        self.index = index
        self.which = index
        self.existence = True
        self.left_child = None
        self.right_child = None
        self.leaf = leaf
        self.value = value
        self.reach_here_probability = 1
        self.reach_here_cost = 0
        self.parent = None


class Tree:

    def __init__(self, max_level):
        self.max_level = max_level
        self.root = None
        self.filled = False
        self.boolean_function_weight_type = None
        self.formula = None
        self.max_index = 0
        self.type = 'adaptive'

    def build_print_tree(self, node):
        if self.filled is False:
            if node is not None:
                if node.leaf is False:
                    root = BNode('x' + str(node.which))
                else:
                    root = BNode(node.value)
                if node.right_child is not None:
                    root.right = self.build_print_tree(node.right_child)
                else:
                    if node.leaf is False:
                        root.right = BNode(None)
                if node.left_child is not None:
                    root.left = self.build_print_tree(node.left_child)
                else:
                    if node.leaf is False:
                        root.left = BNode(None)
                return root

    def print_tree(self):
        print_tree = self.build_print_tree(self.root)
        print(print_tree)

    def restructure_with_boolean_function(self, BooleanFunction):
        self.boolean_function_weight_type = BooleanFunction.weight_type
        self.__restructure(self.root, BooleanFunction.truth_table)
        for _ in range(self.max_level):
            self.__pruning(self.root)
        return self.root

    def __restructure(self, node, truth_table):
        if self.type == 'adaptive':
            if node.index < 2 ** (self.max_level - 1) - 1:
                self.__restructure(node.left_child, truth_table)
                self.__restructure(node.right_child, truth_table)
            else:
                node.left_child = Node(None, leaf=True, value=truth_table[node.index * 2 + 1 - 2 ** self.max_level + 1])
                node.right_child = Node(None, leaf=True, value=truth_table[node.index * 2 + 2 - 2 ** self.max_level + 1])
        elif self.type == 'non-adaptive':
            if node.index < 2 ** (self.max_level - 1) - 1:
                self.__restructure(node.left_child, truth_table)
                self.__restructure(node.right_child, truth_table)
            else:
                node.left_child = Node(None, leaf=True, value=truth_table[node.index * 2 + 1 - 2 ** self.max_level + 1])
                node.right_child = Node(None, leaf=True, value=truth_table[node.index * 2 + 2 - 2 ** self.max_level + 1])

    def __pruning(self, node):
        # print(node.index)
        # if node.left_child is not None:
        #     print(vars(node.left_child))
        # if node.right_child is not None:
        #     print(vars(node.right_child))
        if node.left_child is not None and node.right_child is not None:
            if node.left_child.leaf is True and node.right_child.leaf is True:
                if node.left_child.value == node.right_child.value:
                    node.value = node.left_child.value
                    node.left_child = None
                    node.right_child = None
                    node.leaf = True
        if node.left_child is not None:
            self.__pruning(node.left_child)
        if node.right_child is not None:
            self.__pruning(node.right_child)
        # self.print_tree()
        return self

    def calculate_sympy_formula(self, tmp_p, tmp_c):
        if self.formula is None:
            f = self.__dfs(self.root, 1, 0)
            # print(f)
            f = sympy.simplify(f)

            # p = []
            # c = []
            x = []
            for i in range(self.max_index + 1):
                # p.append(0)
                # c.append(0)
                x.append(0)
                # p[i] = sympy.Symbol('p' + str(i))
                # c[i] = sympy.Symbol('c' + str(i))
                x[i] = sympy.Symbol('p' + str(i))
            for i in range(self.max_index + 1):
                # p.append(0)
                # c.append(0)
                x.append(0)
                # p[i] = sympy.Symbol('p' + str(i))
                # c[i] = sympy.Symbol('c' + str(i))
                x[i + self.max_index + 1] = sympy.Symbol('c' + str(i))
            self.formula = sympy.lambdify([x], f)

        # print(len(tmp_p + tmp_c))
        return self.formula(tmp_p + tmp_c)

    def __dfs(self, node, prob, cost):
        if node.leaf is not True:
            tmp = 0
            if node.left_child is not None:
                tmp += self.__dfs(node.left_child, prob * (1 - sympy.Symbol('p' + str(node.index))),
                                  cost + sympy.Symbol('c' + str(node.index)))
            if node.right_child is not None:
                tmp += self.__dfs(node.right_child, prob * sympy.Symbol('p' + str(node.index)),
                                  cost + sympy.Symbol('c' + str(node.index)))
            return tmp
        else:
            return prob * cost


class NonAdaptiveTree(Tree):
    def __init__(self, max_level):
        Tree.__init__(self, max_level)
        level = 0
        self.root = self.build_tree(level)
        self.max_index = max_level
        self.type = 'non-adaptive'

    def build_tree(self, level):
        if level >= 2 ** self.max_level - 1:
            return None
        root = Node(level)
        if level < 2 ** self.max_level - 1:
            root.left_child = self.build_tree(2 * level + 1)
            root.right_child = self.build_tree(2 * level + 2)
        else:
            return None
        return root

    def fill_in_strategy(self, strategy):
        if len(strategy) != self.max_level:
            raise Exception("strategy error")
        else:
            self.__fill(strategy, self.root)
            return self

    def __fill(self, strategy, node):
        if node is not None:

            node.which = strategy[math.floor(math.log2(node.which+1))]
            self.__fill(strategy, node.left_child)
            self.__fill(strategy, node.right_child)


class AdaptiveTree(Tree):
    def __init__(self, max_level):
        Tree.__init__(self, max_level)
        self.levels = range(2 ** max_level - 1)
        level = 0
        self.root = self.build_tree(level)
        self.max_index = 2 ** max_level - 2

    def build_tree(self, level):
        if level >= 2 ** self.max_level - 1:
            return None
        root = Node(level)
        if level < 2 ** self.max_level - 1:
            root.left_child = self.build_tree(2 * level + 1)
            root.right_child = self.build_tree(2 * level + 2)
        else:
            return None
        return root

    def fill_in_strategy(self, strategy):
        if len(strategy) != 2 ** self.max_level - 1:
            raise Exception("strategy error")
        else:
            self.__fill(strategy, self.root)
            return self

    def __fill(self, strategy, node):
        if node is not None:
            node.which = strategy[node.which]
            self.__fill(strategy, node.left_child)
            self.__fill(strategy, node.right_child)


# import Strategy
#
# s = Strategy.generate_all_adaptive_strategies(5)[0]
# print(s)
# # a = AdaptiveTree(5).fill_in_strategy(s)
# a = AdaptiveTree(5)
# a.print_tree()
#
# import Base
#
# b = Base.LinearThresholdFunction(num_of_variables=5, weights=[1] * 5, threshold=3)
# print(b.truth_table)
# a.restructure_with_boolean_function(b)
# a.print_tree()
#
# prob = [0.1, 0.1, 0.5, 0.9, 0.9]
# cost = [1, 1, 1, 1, 1]
# ps = []
# cs = []
# for b in s:
#     ps.append(prob[b])
#     cs.append(1)
# print(ps)
#
# import RandomInput
#
# for _ in tqdm(range(1000000)):
#     ps = []
#     cs = []
#     prob = RandomInput.get_random_probabilities(5)
#     cost = [1, 1, 1, 1, 1]
#     for b in s:
#         ps.append(prob[b])
#         cs.append(1)
#     a.calculate_sympy_formula(ps, cs)
#

