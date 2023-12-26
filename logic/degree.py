
class Degree:
    def __init__(self, regular_expression):
        self.regular_expression = regular_expression

    def get_degree(self):
        regular_exp = self.regular_expression
        if regular_exp == '':
            return 0
        elif regular_exp == 'λ' or regular_exp.isalpha():
            return 0
        elif regular_exp[-1] == '*':
            inner_degree = Degree(regular_exp[:-1]).get_degree()
            if inner_degree != float('inf'):
                return inner_degree + 1
        elif '+' in regular_exp:
            parts = regular_exp.split('+')
            max_degree = float('-inf')
            for part in parts:
                part_degree = Degree(part).get_degree()
                max_degree = max(max_degree, part_degree)
            return max_degree
        return float('-inf')
