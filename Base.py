import sys


class BooleanFunction:

    def __init__(self, num_of_variables, positive_in_truth_table=None, function_type=None):
        self.truth_table = [0 for _ in range(2 ** num_of_variables)]
        if positive_in_truth_table is not None:
            for i in positive_in_truth_table:
                self.truth_table[i] = 1
        self.num_of_variables = num_of_variables
        if function_type is not None:
            if function_type not in ['symmetric', 'monotone', 'LTF']:
                raise Exception("Invalid function_type")
            if self.check_function() is not True:
                raise Exception("Function_type error, this function is not " + function_type)

    def show(self):
        for i in range(2 ** self.num_of_variables):
            b_string = str(bin(i))[2:]
            while len(b_string) < self.num_of_variables:
                b_string = '0' + b_string
            print("| " + b_string + " | " + str(self.truth_table[i]) + " |")

    def check_function(self):
        # tbd
        return True

    def print_strategy_decision_tree(self, strategy, strategy_type=None):
        if strategy_type is None:
            if len(strategy) == self.num_of_variables:
                strategy_type = 'non-adaptive'
            elif len(strategy) == 2 ** self.num_of_variables - 1:
                strategy_type = 'adaptive'
            else:
                raise Exception("strategy error")
        import Tree
        if strategy_type == 'non-adaptive':
            tree = Tree.NonAdaptiveTree(self.num_of_variables)
        elif strategy_type == 'adaptive':
            tree = Tree.AdaptiveTree(self.num_of_variables)
        else:
            raise Exception("strategy_type error")

        tree.fill_in_strategy(strategy)
        tree.restructure_with_boolean_function(self)
        tree.print_tree()


class LinearThresholdFunction(BooleanFunction):

    def __init__(self, num_of_variables, weights, threshold):
        BooleanFunction.__init__(self, num_of_variables=num_of_variables,
                                 positive_in_truth_table=self.__get_truth_table(num_of_variables, weights, threshold),
                                 function_type='LTF')
        self.weights = weights
        self.threshold = threshold

    def __get_truth_table(self, num_of_variables, weights, threshold):

        self.num_of_variables = num_of_variables

        if weights == [1] * num_of_variables:
            self.weight_type = 'unit'
        else:
            self.weight_type = 'arbitrary'

        positive_in_truth_table = []
        if self.weight_type == 'unit':
            for i in range(2 ** num_of_variables):
                binary = bin(i)
                one_count = len([ones for ones in binary[2:] if ones == '1'])
                if one_count >= threshold:
                    positive_in_truth_table.append(i)
            return positive_in_truth_table
        else:
            for i in range(2 ** num_of_variables):
                binary = str(bin(i))[2:]
                while len(binary) < self.num_of_variables:
                    binary = '0' + binary
                sum_list = list(map(int, binary))
                if dot_product(sum_list, weights) >= threshold:
                    positive_in_truth_table.append(i)
            return positive_in_truth_table

    def get_non_adaptive_strategy_cost(self, strategy, probabilities, costs=None):
        if costs is None or costs == [1] * self.num_of_variables:
            cost_type = 'unit'
        else:
            cost_type = 'arbitrary'
        if self.weight_type == 'unit':
            from linear_threshold_function import unweighted as ltf
            if cost_type == 'unit':
                return ltf.get_non_adaptive_cost_unit_cost(self.threshold, self.num_of_variables, probabilities, strategy)
            elif cost_type == 'arbitrary':
                return ltf.get_non_adaptive_cost_unit_cost(self.threshold, self.num_of_variables, probabilities, costs,
                                                           strategy)
        elif self.weight_type == 'arbitrary':
            from linear_threshold_function import weighted as ltf
            return ltf.get_non_adaptive_cost(self.threshold, self.num_of_variables, probabilities, self.weights,
                                             strategy, cost_type)
        else:
            raise Exception("weight_type error")

    def get_optimal_non_adaptive_strategy(self, probabilities, costs=None):
        if costs is None or costs == [1] * self.num_of_variables:
            cost_type = 'unit'
        else:
            cost_type = 'arbitrary'
        if self.weight_type == 'unit':
            from linear_threshold_function import unweighted as ltf
            return ltf.get_optimal_non_adaptive_cost(self.threshold, self.num_of_variables, probabilities, costs, cost_type)
        elif self.weight_type == 'arbitrary':
            from linear_threshold_function import weighted as ltf
            return ltf.get_optimal_non_adaptive_cost(self.threshold, self.num_of_variables, probabilities, costs, self.weights)
        else:
            raise Exception("weight_type error")

    def get_adaptive_strategy_cost(self, strategy, probabilities, costs=None):
        if costs is None or costs == [1] * self.num_of_variables:
            cost_type = 'unit'
        if self.weight_type == 'unit':
            from linear_threshold_function import unweighted as ltf
            return ltf.get_adaptive_cost(self.threshold, self.num_of_variables, probabilities, costs, strategy, cost_type)
        elif self.weight_type == 'arbitrary':
            from linear_threshold_function import weighted as ltf
            return ltf.get_adaptive_cost(self.threshold, self.num_of_variables, probabilities, costs, self.weights, strategy,
                                         cost_type)
        else:
            raise Exception("weight_type error")

    def get_optimal_adaptive_strategy(self, probabilities, costs=None):
        if costs is None or costs == [1] * self.num_of_variables:
            cost_type = 'unit'
        if self.weight_type == 'unit':
            from linear_threshold_function import unweighted as ltf
            return ltf.get_optimal_adaptive_cost(self.threshold, self.num_of_variables, probabilities, costs, cost_type)
        elif self.weight_type == 'arbitrary':
            from linear_threshold_function import weighted as ltf
            return ltf.get_optimal_adaptive_cost(self.threshold, self.num_of_variables, probabilities, costs, self.weights,
                                                 cost_type)
        else:
            raise Exception("weight_type error")


def dot_product(a, b):
    if len(a) != len(b):
        raise Exception("dot_product error")
    result = 0
    for i in range(len(a)):
        result += a[i] * b[i]
    return result


sample = LinearThresholdFunction(num_of_variables=5, weights=[1, 1, 1, 1, 1], threshold=3)
sample.print_strategy_decision_tree([2,1,3,4,0])
# print(sample.get_optimal_non_adaptive_strategy([0.01, 0.01, 0.5, 0.99, 0.99]))
# print(vars(sample))

# BooleanFunction(num_of_variables=4, positive_in_truth_table=[5, 6, 7]).show()
