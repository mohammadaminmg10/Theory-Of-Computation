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

    def test_accepts_string(self):
        self.assertTrue(self.dfa.accepts_string('abab'))
        self.assertFalse(self.dfa.accepts_string('bbbb'))

    def test_minimize(self):
        self.assertEqual(self.dfa.minimize(), self.dfa)
        self.assertTrue(self.dfa.minimize().accepts_string('abab'))
        self.assertFalse(self.dfa.minimize().accepts_string('bbbb'))


if __name__ == '__main__':
    unittest.main()
