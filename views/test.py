expected_transitions = {
            ('q3', 'q7'): {'a': ('q0', 'q1', 'q2'), 'b': ('q3',), 'c': ('q4', 'q7', 'q5')},
            ('q1', 'q2'): {'a': ('q0', 'q1', 'q2'), 'b': ('q3',), 'c': ('q4', 'q7', 'q5')},
            ('q7', 'q4', 'q6', 'q0', 'q5'): {'a': ('q0', 'q1', 'q2'), 'b': ('q3',), 'c': ('q4', 'q7', 'q5')},
            ('q4', 'q5', 'q7'): {'a': ('q0', 'q1', 'q2'), 'b': ('q3',), 'c': ('q4', 'q7', 'q5')}
        }

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
            }

transitions = {}

for current_states, transitions_dict in expected_transitions.items():
    for symbol, next_states in transitions_dict.items():
        for next_state in next_states:
            transitions[(current_states, symbol)] = next_state

print(transitions)

        
