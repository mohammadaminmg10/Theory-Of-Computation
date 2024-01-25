import re


class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states


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


class RegularExpressionAnalyzer:
    def __init__(self):
        self.expressions = []

    def simplize_expression(self):
        pass

    def is_regular(self, expression):
        # Q1
        """
        Check if the given expression is a regular expression.
        
        :param expression: The input regular expression.
        :return: True if the expression is a regular expression, False otherwise.
        """
        operator_precedence = {'|': 1, '.': 2, '*': 3, '+': 3}  # Define operator precedence
        valid_symbols = {'∅', 'ε', '|', '*', '+', '(', ')'}
        def is_operator(token):
            return token in operator_precedence
        def validate_infix_expression():
            stack = []
            for i, char in enumerate(expression):
                if char == '(':
                    stack.append(char)
                elif char == ')':
                    if not stack or stack[-1] != '(':
                        return False  # Unmatched closing parenthesis or misplaced operator
                    stack.pop()
                elif is_operator(char):
                    if i == 0 or (i == len(expression) - 1 or expression[i - 1] in operator_precedence or expression[i + 1] in operator_precedence) and char not in ['*', '+']:
                        return False  # Misplaced operator
                elif char not in valid_symbols and not char.isalpha():
                    return False  # Invalid symbol
            return not stack  # Check if all opening parentheses are matched
        return validate_infix_expression() and self.to_nfa(expression) is not None

    def to_nfa(self, expression):
        def _create_state():
            nonlocal state_counter
            state = f"q{state_counter}"
            state_counter += 1
            return state

        def _concatenate_nfas(nfa1, nfa2):
            new_start = nfa1.start_state
            new_accept = nfa2.accept_states
            # for state in nfa1.transitions:
            #     if state != 'ε':
            #         for symbol in nfa1.transitions[state]:
            #             if symbol != 'ε':
            #                 nfa1.transitions[state][symbol] = [state + suffix for suffix in nfa1.transitions[state][symbol]]
            # for state in nfa2.transitions:
            #     if state != 'ε':
            #         for symbol in nfa2.transitions[state]:
            #             if symbol != 'ε':
            #                 nfa2.transitions[state][symbol] = [state + suffix for suffix in nfa2.transitions[state][symbol]]

            for state in nfa1.accept_states:
                if 'ε' not in nfa1.transitions[state]:
                    nfa1.transitions[state]['ε'] = []
                nfa1.transitions[state]['ε'].extend([nfa2.start_state])

            return NFA(
                states=nfa1.states + nfa2.states,
                alphabet=list(set(nfa1.alphabet + nfa2.alphabet)),
                transitions={**nfa1.transitions, **nfa2.transitions},
                start_state=new_start,
                accept_states=new_accept
            )

        def _alternative_nfas(nfa1, nfa2):
            new_start = _create_state()
            new_accept = _create_state()
            transitions = {
                new_start: {'ε': [nfa1.start_state, nfa2.start_state]},
                new_accept: {}
            }
            for state in nfa1.accept_states:
                if 'ε' not in nfa1.transitions[state]:
                    nfa1.transitions[state]['ε'] = []
                nfa1.transitions[state]['ε'].extend([new_accept])
            for state in nfa2.accept_states:
                if 'ε' not in nfa2.transitions[state]:
                    nfa2.transitions[state]['ε'] = []
                nfa2.transitions[state]['ε'].extend([new_accept])
            return NFA(
                states=[new_start, new_accept] + nfa1.states + nfa2.states,
                alphabet=list(set(nfa1.alphabet + nfa2.alphabet)),
                transitions={**transitions, **nfa1.transitions, **nfa2.transitions},
                start_state=new_start,
                accept_states=[new_accept]
            )

        def infix_to_postfix(infix_expression):
            operator_precedence = {'|': 1, '.': 2, '*': 3, '+': 3, '(': -1, ')': -1}  # Define operator precedence

            def is_operator(token):
                return token in operator_precedence

            output_stack = []
            operator_stack = []

            for token in infix_expression:
                if token.isalpha() or token in {'∅', 'ε'}:
                    output_stack.append(token)
                elif token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        output_stack.append(operator_stack.pop())
                    operator_stack.pop()  # Discard '('
                elif is_operator(token):
                    while operator_stack and operator_precedence.get(operator_stack[-1], 0) >= operator_precedence[token]:
                        output_stack.append(operator_stack.pop())
                    operator_stack.append(token)
            while operator_stack:
                output_stack.append(operator_stack.pop())
            return ''.join(output_stack)
    
        state_counter = 0
        stack = []
        expression = infix_to_postfix(expression)

        for char in expression:
            if char.isalpha() or char in {'∅', 'ε'}:
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
                new_nfa = _alternative_nfas(nfa1, nfa2)
                stack.append(new_nfa)
            elif char == '+':
                # this means we should have at least 1 expression of its previous expression; shuch as (ab)+
                nfa = stack.pop()
                # start_state = _create_state()
                # accept_state = _create_state()
                # transitions = {
                #     start_state: {},
                #     accept_state: {}
                # }

                for state in nfa.accept_states:
                    if 'ε' not in nfa.transitions[state]:
                        nfa.transitions[state]['ε'] = [nfa.start_state]
                    # nfa.transitions[state]['ε'].extend([nfa.start_state, accept_state])
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
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                new_nfa = _concatenate_nfas(nfa1, nfa2)
                stack.append(new_nfa)
            elif char == '*':
                nfa = stack.pop()
                for state in nfa.accept_states:
                    if 'ε' not in nfa.transitions[state]:
                        nfa.transitions[state]['ε'] = [nfa.start_state]
                    if 'ε' in nfa.transitions[nfa.start_state]:
                        nfa.transitions[nfa.start_state]['ε'].extend([state])
                    nfa.transitions[nfa.start_state]['ε'] = [state]                        
                stack.append(nfa)

        return stack.pop() if stack else None

    def to_dfa(self, expression):
        def epsilon_closure(states):
            epsilon_closure_set = set(states)
            stack = list(states)

            while stack:
                state = stack.pop()
                if state in nfa.transitions and 'ε' in nfa.transitions[state]:
                    for epsilon_state in nfa.transitions[state]['ε']:
                        if epsilon_state not in epsilon_closure_set:
                            epsilon_closure_set.add(epsilon_state)
                            stack.append(epsilon_state)

            return list(epsilon_closure_set)

        def get_next_state(current_states, symbol):
            next_states = []
            for state in current_states:
                if state in nfa.transitions and symbol in nfa.transitions[state]:
                    next_states.extend(nfa.transitions[state][symbol])
            return epsilon_closure(next_states)

        nfa = self.to_nfa(expression)

        nfa_transition_table = {state: {symbol: [] for symbol in nfa.alphabet} for state in nfa.states}
        for state in nfa.states:
            for symbol in nfa.alphabet:
                nfa_transition_table[state][symbol] = get_next_state([state], symbol)

        dfa_start_state = epsilon_closure([nfa.start_state])

        dfa_transition_table = {tuple(dfa_start_state): {symbol: [] for symbol in nfa.alphabet}}
        stack = [tuple(dfa_start_state)]
        while stack:
            current_states = stack.pop()
            for symbol in nfa.alphabet:
                next_states = get_next_state(list(current_states), symbol)
                if next_states:
                    if tuple(next_states) not in dfa_transition_table:
                        dfa_transition_table[tuple(next_states)] = {symbol: [] for symbol in nfa.alphabet}
                        stack.append(tuple(next_states))
                    dfa_transition_table[tuple(current_states)][symbol] = list(next_states)

        dfa_accept_states = [state_set for state_set in dfa_transition_table.keys() if
                             any(state in nfa.accept_states for state in state_set)]

        # Return the DFA
        return DFA(
            states=list(dfa_transition_table.keys()),
            alphabet=nfa.alphabet,
            transitions=dfa_transition_table,
            start_state=tuple(dfa_start_state),
            accept_states=dfa_accept_states
        )

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
    