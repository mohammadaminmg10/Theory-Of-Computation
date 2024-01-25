import unittest

from dfa import Dfa
from regular_language import RegularExpressionAnalyzer, NFA, DFA


class TestRegularExpressionAnalyzer(unittest.TestCase):
    def setUp(self):
        self.regex_analyzer = RegularExpressionAnalyzer()

    def test_is_regular(self):
        self.assertTrue(self.regex_analyzer.is_regular("a"))
        self.assertTrue(self.regex_analyzer.is_regular("a.b|c"))
        self.assertTrue(self.regex_analyzer.is_regular("((a|b))*"))
        self.assertTrue(self.regex_analyzer.is_regular("∅|ε"))
        self.assertTrue(self.regex_analyzer.is_regular("a+"))
        self.assertTrue(self.regex_analyzer.is_regular("(a*)|(b*)"))
        self.assertFalse(self.regex_analyzer.is_regular("(a|b"))
        self.assertTrue(self.regex_analyzer.is_regular("(a*)*"))
        self.assertFalse(self.regex_analyzer.is_regular("a|*b"))
        self.assertFalse(self.regex_analyzer.is_regular("a|b|"))
        self.assertTrue(self.regex_analyzer.is_regular("a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q"))

    def test_to_nfa(self):

        regex = "(((a.b))|c*)"
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
        regex = "a.b|c*"
        result_dfa = self.regex_analyzer.to_dfa(regex)
        # Assert the expected properties of the resulting DFA

        # States
        expected_states = {('q7', 'q4', 'q6', 'q0', 'q5'), ('q3', 'q7'), ('q4', 'q5', 'q7'), ('q1', 'q2')}
        self.assertEqual(set(result_dfa.states), expected_states)

        # Alphabet
        expected_alphabet = {'a', 'b', 'c'}
        self.assertEqual(set(result_dfa.alphabet), expected_alphabet)

        # Transitions
        expected_transitions = {
            ('q3', 'q7'): {'a': ('q0', 'q1', 'q2'), 'b': ('q3',), 'c': ('q4', 'q7', 'q5')},
            ('q1', 'q2'): {'a': ('q0', 'q1', 'q2'), 'b': ('q3',), 'c': ('q4', 'q7', 'q5')},
            ('q7', 'q4', 'q6', 'q0', 'q5'): {'a': ('q0', 'q1', 'q2'), 'b': ('q3',), 'c': ('q4', 'q7', 'q5')},
            ('q4', 'q5', 'q7'): {'a': ('q0', 'q1', 'q2'), 'b': ('q3',), 'c': ('q4', 'q7', 'q5')}
        }
        self.assertEqual(result_dfa.transitions, expected_transitions)

        # Start State
        expected_start_state = ('q3', 'q7')
        self.assertEqual(result_dfa.start_state, expected_start_state)

        # Accept States
        expected_accept_states = {('q3', 'q7'), ('q1', 'q2'), ('q7', 'q4', 'q6', 'q0', 'q5'), ('q4', 'q5', 'q7')}
        self.assertEqual(set(result_dfa.accept_states), expected_accept_states)
        self.assertIsNotNone(result_dfa, "Resulting DFA should not be None")

        # Additional test case
        regex = "(a*).b"
        dfa = self.regex_analyzer.to_dfa(regex)
        expected_dfa = DFA(
            states={('q0', 'q1', 'q2'), ('q3',)},
            alphabet={'a', 'b'},
            transitions={
                ('q0', 'q1', 'q2'): {'a': ('q0', 'q1', 'q2'), 'b': ('q3',)},
                ('q3',): {'a': (), 'b': ()}
            },
            start_state=('q0', 'q1', 'q2'),
            accept_states={('q3',)}
        )
        self.assertEqual(set(dfa.states), expected_dfa.states)
        self.assertEqual(expected_dfa.alphabet, set(dfa.alphabet))
        self.assertEqual(expected_dfa.accept_states, set(dfa.accept_states))
        self.assertEqual(expected_dfa.start_state, dfa.start_state)
        self.assertEqual(dfa.transitions, expected_dfa.transitions)

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
    