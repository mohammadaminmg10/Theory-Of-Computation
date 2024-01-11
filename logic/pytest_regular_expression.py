import unittest

from dfa import Dfa
from regular_language import RegularExpressionAnalyzer, NFA


class TestRegularExpressionAnalyzer(unittest.TestCase):
    def setUp(self):
        self.regex_analyzer = RegularExpressionAnalyzer()

    def test_is_regular(self):
        pass

    def test_to_nfa(self):

        regex = "a.b|c*"
        result_nfa = self.regex_analyzer.to_nfa(regex)
        # Assert the expected properties of the resulting NFA

        # States
        expected_states = {'q0', 'q1','q2','q3','q4', 'q5', 'q6', 'q7'}
        self.assertEqual(set(result_nfa.states), expected_states)

        # Alphabet
        expected_alphabet = {'a', 'b', 'c'}
        self.assertEqual(set(result_nfa.alphabet), expected_alphabet)

        # Transitions
        expected_transitions = {
            'q0': {'a': ['q1']},
            'q1': {'ε': ['q2']},
            'q2': {'b': ['q3']},
            'q3': {'ε': ['q7']},
            'q4': {'c': ['q5'], 'ε': ['q5']},
            'q5': {'ε': ['q4', 'q7']},
            'q6': {'ε': ['q0', 'q4']},
            'q7': {}
        }
        self.assertEqual(result_nfa.transitions, expected_transitions)

        # Start State
        self.assertEqual(result_nfa.start_state, 'q6')

        # Accept States
        expected_accept_states = {'q7'}
        self.assertEqual(set(result_nfa.accept_states), expected_accept_states)
        self.assertIsNotNone(result_nfa, "Resulting NFA should not be None")

        regex = "(a*).b"
        nfa = self.regex_analyzer.to_nfa(regex)
        expected_nfa = NFA(
            states={'q0', 'q1','q2', 'q3'},
            alphabet={'a', 'b'},
            transitions={
                'q0': {'a': ['q1'], 'ε': ['q1']},
                'q1': {'ε': ['q0', 'q2']},
                'q2': {'b': ['q3']},
                'q3': {},
            },
            start_state='q0',
            accept_states={'q3'}
        )
        self.assertEqual(set(nfa.states), expected_nfa.states)
        self.assertEqual(expected_nfa.alphabet, set(nfa.alphabet))
        self.assertEqual(expected_nfa.accept_states, set(nfa.accept_states))
        self.assertEqual(expected_nfa.start_state, nfa.start_state)
        self.assertEqual(nfa.transitions, expected_nfa.transitions)

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
        # self.assertFalse(self.regex_analyzer.compare_languages(expression1, expression2))

    def test_is_relation(self):
        expression1 = "a*b"
        expression2 = "a*b+c"

        # Compare languages of the generated DFAs
        # self.assertTrue(self.regex_analyzer.is_relation(expression1, expression2))


if __name__ == '__main__':
    unittest.main()
