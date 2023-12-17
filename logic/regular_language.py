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
        pass

    def compare_languages(self, expression1, expression2):
        # dfa1 = self.to_dfa(expression1)  # Convert expression1 to a Dfa object
        # dfa2 = self.to_dfa(expression2)  # Convert expression2 to a Dfa object
        #
        # # Use are_equivalent method from the Dfa class to compare languages
        # return dfa1.are_equivalent(dfa2)

    def language_relation(self, expression1, expression2):
        # Q5
        """
        Check the relationship between two regular languages.

        :param expression1: The first regular expression.
        :param expression2: The second regular expression.
        :return: A string indicating the relationship (subset, superset, equal, or none).
        """
