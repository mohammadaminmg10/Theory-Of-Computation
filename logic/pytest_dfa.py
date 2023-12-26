import unittest

from dfa import Dfa


class TestDfaMethods(unittest.TestCase):
    def setUp(self):
        self.dfa = Dfa(
            states=['q0', 'q1', 'q2'],
            alphabet=['a', 'b'],
            transitions={
                ('q0', 'a'): 'q1',
                ('q0', 'b'): 'q0',
                ('q1', 'a'): 'q2',
                ('q1', 'b'): 'q1',
                ('q2', 'a'): 'q2',
                ('q2', 'b'): 'q2'
            },
            start_state='q0',
            accept_states=['q2']
        )

    def test_is_empty_language(self):
        self.assertFalse(self.dfa.is_empty_language())
        self.assertTrue(Dfa(
            states=['q0', 'q1'],
            alphabet=['a', 'b'],
            transitions={
                ('q0', 'a'): 'q1',
                ('q0', 'b'): 'q0',
                ('q1', 'a'): 'q1',
                ('q1', 'b'): 'q1'
            },
            start_state='q0',
            accept_states=[]
        ).is_empty_language())

    def test_is_trap(self):
        self.assertFalse(self.dfa.is_trap('q0'))
        self.assertTrue(Dfa(
            states=['q0', 'q1'],
            alphabet=['a', 'b'],
            transitions={
                ('q0', 'a'): 'q0',
                ('q0', 'b'): 'q0',
                ('q1', 'a'): 'q1',
                ('q1', 'b'): 'q1'
            },
            start_state='q0',
            accept_states=['q1']
        ).is_trap('q0'))

    def test_is_finite(self):
        self.assertFalse(self.dfa.is_finite())
        self.assertTrue(Dfa(
            states=['q0', 'q1', 'q2'],
            alphabet=['a', 'b'],
            transitions={
                ('q0', 'a'): 'q1',
                ('q0', 'b'): 'q1',
                ('q1', 'a'): 'q2',
                ('q1', 'b'): 'q2',
                ('q2', 'a'): 'q2',
                ('q2', 'b'): 'q2'
            },
            start_state='q0',
            accept_states=['q1']
        ).is_finite())

    def test_all_strings(self):
        self.assertEqual(Dfa(
            states=['q0', 'q1', 'q2'],
            alphabet=['a', 'b'],
            transitions={
                ('q0', 'a'): 'q1',
                ('q0', 'b'): 'q1',
                ('q1', 'a'): 'q2',
                ('q1', 'b'): 'q2',
                ('q2', 'a'): 'q2',
                ('q2', 'b'): 'q2'
            },
            start_state='q0',
            accept_states=['q0']
        ).all_strings(), {''})

        self.assertEqual(Dfa(
            states=['q0', 'q1', 'q2', 'q3'],
            alphabet=['a', 'b'],
            transitions={
                ('q0', 'a'): 'q1',
                ('q0', 'b'): 'q1',
                ('q1', 'a'): 'q2',
                ('q1', 'b'): 'q2',
                ('q2', 'a'): 'q3',
                ('q2', 'b'): 'q3',
                ('q3', 'a'): 'q2',
                ('q3', 'b'): 'q3',
            },
            start_state='q0',
            accept_states=['q2']
        ).all_strings(), None)

    def test_accepts_string(self):
        self.assertTrue(self.dfa.accepts_string('abab'))
        self.assertFalse(self.dfa.accepts_string('bbbb'))

    def test_minimize(self):
        self.assertEqual(self.dfa.minimize(), self.dfa)
        self.assertTrue(self.dfa.minimize().accepts_string('abab'))
        self.assertFalse(self.dfa.minimize().accepts_string('bbbb'))

    def test_are_equivalent(self):
        self.assertTrue(self.dfa.are_equivalent(self.dfa))
        self.assertFalse(self.dfa.are_equivalent(Dfa(
            states=['q0', 'q1'],
            alphabet=['a', 'b'],
            transitions={
                ('q0', 'a'): 'q1',
                ('q0', 'b'): 'q0',
                ('q1', 'a'): 'q1',
                ('q1', 'b'): 'q1'
            },
            start_state='q0',
            accept_states=['q1']
        )))

        dfa_1 = Dfa(
            states=['q0', 'q1'],
            alphabet=['0', '1'],
            transitions={
                ('q0', '0'): 'q0',
                ('q0', '1'): 'q1',
                ('q1', '0'): 'q0',
                ('q1', '1'): 'q1'
            },
            start_state='q0',
            accept_states=['q0']
        )

        dfa_2 = Dfa(
            states=['q2', 'q3', 'q4'],
            alphabet=['0', '1'],
            transitions={
                ('q2', '0'): 'q3',
                ('q2', '1'): 'q4',
                ('q3', '0'): 'q3',
                ('q3', '1'): 'q4',
                ('q4', '0'): 'q2',
                ('q4', '1'): 'q4'
            },
            start_state='q2',
            accept_states=['q2', 'q3']
        )

        self.assertTrue(dfa_1.are_equivalent(dfa_2))

        dfa_1 = Dfa(
            states=['P', 'R', 'Q'],
            alphabet=['a', 'b'],
            transitions={
                ('P', 'a'): 'R',
                ('P', 'b'): 'Q',
                ('R', 'a'): 'Q',
                ('R', 'b'): 'P',
                ('Q', 'a'): 'Q',
                ('Q', 'b'): 'Q'
            },
            start_state='P',
            accept_states=['P']
        )

        dfa_2 = Dfa(
            states=['A', 'B', 'C', 'D', 'E'],
            alphabet=['a', 'b'],
            transitions={
                ('A', 'a'): 'B',
                ('A', 'b'): 'D',
                ('B', 'a'): 'D',
                ('B', 'b'): 'C',
                ('C', 'a'): 'B',
                ('C', 'b'): 'E',
                ('D', 'a'): 'D',
                ('D', 'b'): 'D',
                ('E', 'a'): 'D',
                ('E', 'b'): 'D'
            },
            start_state='A',
            accept_states=['A', 'C']
        )

        self.assertTrue(dfa_1.are_equivalent(dfa_2))


if __name__ == '__main__':
    unittest.main()
