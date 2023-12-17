import re

from dfa import Dfa
class NFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    @staticmethod
    def epsilon_closure(states, transitions):
        epsilon_closure_set = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            if state in transitions and 'ε' in transitions[state]:
                for epsilon_state in transitions[state]['ε']:
                    if epsilon_state not in epsilon_closure_set:
                        epsilon_closure_set.add(epsilon_state)
                        stack.append(epsilon_state)

        return list(epsilon_closure_set)
class RegularExpression:
    def __init__(self):
        pass

    def to_nfa(self, expression):
        def _create_state():
            nonlocal state_counter
            state = f"q{state_counter}"
            state_counter += 1
            return state

        def _concatenate_nfas(nfa1, nfa2):
            # Concatenation logic
            pass

        def _parse(expression):
            # Parse regular expression and construct NFA
            pass

        state_counter = 0

        # Use _parse function to convert expression to NFA
        nfa = _parse(expression)

        # For demonstration purposes, return an empty NFA
        return NFA(states=[], alphabet=[], transitions={}, start_state='', accept_states=[])


# Example usage:
regex = RegularExpression()
result_nfa = regex.to_nfa("your_regular_expression_here")


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
        def _create_state():
            nonlocal state_counter
            state = f"q{state_counter}"
            state_counter += 1
            return state

        def _concatenate_nfas(nfa1, nfa2):
            new_start = nfa1.start_state
            new_accept = nfa2.accept_states[0]

            for state in nfa1.transitions:
                if state != 'ε':
                    for symbol in nfa1.transitions[state]:
                        if symbol != 'ε':
                            nfa1.transitions[state][symbol] = [state + suffix for suffix in nfa1.transitions[state][symbol]]

            for state in nfa2.transitions:
                if state != 'ε':
                    for symbol in nfa2.transitions[state]:
                        if symbol != 'ε':
                            nfa2.transitions[state][symbol] = [state + suffix for suffix in nfa2.transitions[state][symbol]]

            for state in nfa1.accept_states:
                if 'ε' not in nfa1.transitions[state]:
                    nfa1.transitions[state]['ε'] = []
                nfa1.transitions[state]['ε'].append(nfa2.start_state)

            return NFA(
                states=nfa1.states + nfa2.states,
                alphabet=list(set(nfa1.alphabet + nfa2.alphabet)),
                transitions={**nfa1.transitions, **nfa2.transitions},
                start_state=new_start,
                accept_states=[new_accept]
            )

        state_counter = 0
        stack = []

        for char in expression:
            if char.isalpha():
                start_state = _create_state()
                accept_state = _create_state()

                transitions = {
                    start_state: {char: [accept_state]},
                    accept_state: {}
                }

                nfa = NFA(
                    states=[start_state, accept_state],
                    alphabet=[char],
                    transitions=transitions,
                    start_state=start_state,
                    accept_states=[accept_state]
                )
                stack.append(nfa)
            elif char == '|':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                new_nfa = _concatenate_nfas(nfa1, nfa2)
                stack.append(new_nfa)
            elif char == '*':
                nfa = stack.pop()
                start_state = _create_state()
                accept_state = _create_state()

                transitions = {
                    start_state: {},
                    accept_state: {}
                }

                for state in nfa.accept_states:
                    if 'ε' not in nfa.transitions[state]:
                        nfa.transitions[state]['ε'] = []
                    nfa.transitions[state]['ε'].append(nfa.start_state)
                    nfa.transitions[state]['ε'].append(accept_state)

                transitions[start_state]['ε'] = [nfa.start_state, accept_state]

                new_nfa = NFA(
                    states=[start_state, accept_state] + nfa.states,
                    alphabet=nfa.alphabet,
                    transitions={**transitions, **nfa.transitions},
                    start_state=start_state,
                    accept_states=[accept_state]
                )
                stack.append(new_nfa)
            elif char == '.':
                # Concatenation logic
                pass

        return stack.pop() if stack else None

    def to_dfa(self, expression):
        # pattern = re.compile(expression)
        # alphabet = {symbol for symbol in pattern.pattern if symbol.isalpha()}
        # states = {frozenset({''})}  # Initialize states with the empty set
        #
        # def get_next_state(current_state, symbol):
        #     next_states = set()
        #     for state in current_state:
        #         match = pattern.match(state + symbol, pos=len(state))
        #         if match:
        #             next_states.add(match.group())
        #     return frozenset(next_states)
        #
        # unprocessed_states = states.copy()
        # transitions = {}
        #
        # while unprocessed_states:
        #     current_state = unprocessed_states.pop()
        #     for symbol in alphabet:
        #         next_state = get_next_state(current_state, symbol)
        #         if next_state:
        #             transitions.setdefault(current_state, {})[symbol] = next_state
        #             if next_state not in states:
        #                 unprocessed_states.add(next_state)
        #                 states.add(next_state)
        #
        # dfa_start_state = frozenset({''})
        # dfa_accept_states = [state for state in states if pattern.fullmatch(''.join(state))]
        #
        # return Dfa(states, list(alphabet), transitions, dfa_start_state, dfa_accept_states)
        pass

    def compare_languages(self, expression1, expression2):
        dfa1 = self.to_dfa(expression1)  # Convert expression1 to a Dfa object
        dfa2 = self.to_dfa(expression2)  # Convert expression2 to a Dfa object

        # Use are_equivalent method from the Dfa class to compare languages
        return dfa1.are_equivalent(dfa2)
    
    def is_relation(self, expression1, expression2):
        if self.is_subset(expression1, expression2) or self.is_subset(expression2, expression1):
            return True

    def is_subset(self, expression1, expression2):
        dfa1 = self.to_dfa(expression1)
        dfa2 = self.to_dfa(expression2)

        for string in dfa1.all_strings():
            if not dfa2.accepts_string(string):
                return False
        return True
        