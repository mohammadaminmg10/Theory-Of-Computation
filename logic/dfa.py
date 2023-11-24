
class Dfa:
    def __init__(self):
        pass

    def is_empty(self):
        """
        Q1
        Checks whether the language of the DFA is empty or not.
        :return: True if the language is empty, False otherwise.
        """

    def is_finite(self):
        """
        Q2
        Checks whether the language of the DFA is finite.
        :return: True if the language is finite, False otherwise.
        """

    def all_strings(self):
        """
        Q2*
        Returns all strings in the language of the DFA.
        :return: A list of all strings in the language.
        """

    def accepts_string(self, input_string):
        """
        Q3
        Checks whether the DFA accepts the given input string.
        :param input_string: The input string to be checked.
        :return: True if the DFA accepts the string, False otherwise.
        """

    def minimize(self):
        """
        Q4
        Minimizes the DFA by reducing the number of states and transitions while preserving the language.
        """

    def are_equivalent(self, other_dfa):
        """
        Q5
        Checks whether the current DFA is equivalent to another DFA.
        :param other_dfa: The other DFA for comparison.
        :return: True if the DFAs are equivalent, False otherwise.
        """
