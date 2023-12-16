import re

from dfa import Dfa


class RegularExpressionAnalyzer:
    def __init__(self):
        self.expressions = []

    def is_regular(self, expression):
        # Q1
        """
        Check if the given expression is a regular expression.
        
        :param expression: The input regular expression.
        :return: True if the expression is a regular expression, False otherwise.
        """

    def to_nfa(self, expression):
        # Q2
        """
        Convert a regular expression to a NFA.

        :param expression: The input regular expression.
        :return: An NFA representing the given regular expression.
        """

    def to_dfa(self, expression):
        pattern = re.compile(expression)

        states = ['q' + str(i) for i in range(1, len(expression) + 2)]

        alphabet = list(set(expression))

        transitions = {(state, symbol): None for state in states for symbol in alphabet}

        for state in states:
            for symbol in alphabet:
                next_state = 'q' + str(states.index(state) + 1) if pattern.match(symbol, pos=pattern.match(
                    state).end()) else None
                transitions[(state, symbol)] = next_state

        start_state = 'q1'
        accept_states = [state for state in states if
                         pattern.match(state)]

        return Dfa(states, alphabet, transitions, start_state, accept_states)

    def compare_languages(self, expression1, expression2):
        dfa1 = self.to_dfa(expression1)  # Convert expression1 to a Dfa object
        dfa2 = self.to_dfa(expression2)  # Convert expression2 to a Dfa object

        # Use are_equivalent method from the Dfa class to compare languages
        return dfa1.are_equivalent(dfa2)

    def language_relation(self, expression1, expression2):
        # Q5
        """
        Check the relationship between two regular languages.

        :param expression1: The first regular expression.
        :param expression2: The second regular expression.
        :return: A string indicating the relationship (subset, superset, equal, or none).
        """
