import unittest

from dfa import Dfa
from regular_language import RegularExpressionAnalyzer


class TestRegularExpressionAnalyzer(unittest.TestCase):
    def setUp(self):
        self.regex_analyzer = RegularExpressionAnalyzer()

    def test_is_regular(self):
        pass

    def test_to_nfa(self):
        pass

    def test_to_dfa(self):
        # regex = "a*b"
        # dfa = self.regex_analyzer.to_dfa(regex)
        #
        # # Create an expected DFA manually or through an alternative method
        # expected_dfa = Dfa(
        #     states=['q0', 'q1'],
        #     alphabet=['a', 'b'],
        #     transitions={
        #         ('q0', 'a'): 'q1',
        #         ('q0', 'b'): 'q0',
        #         ('q1', 'a'): 'q1',
        #         ('q1', 'b'): 'q1'
        #     },
        #     start_state='q0',
        #     accept_states=['q1']
        # )
        #
        # # Compare the generated DFA with the expected DFA
        # self.assertEqual(dfa, expected_dfa)
        pass

    def test_compare_languages(self):
        expression1 = "a*b"
        expression2 = "a*b+c"

        # Compare languages of the generated DFAs
        self.assertFalse(self.regex_analyzer.compare_languages(expression1, expression2))


if __name__ == '__main__':
    unittest.main()
