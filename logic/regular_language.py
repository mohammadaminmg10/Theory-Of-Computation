class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def minimize(self):
        # firt check for unreachable states and delete them
        global equivalent_groups
        reachable_states = [self.start_state]
        for state in reachable_states:
            for symbol in self.alphabet:
                if (state, symbol) in self.transitions:
                    next_state = self.transitions[(state, symbol)]
                    if next_state not in reachable_states:
                        reachable_states.append(next_state)

        self.states = reachable_states

        # Step 1: Initialize the table
        table_size = len(self.states)
        table = []
        for _ in range(table_size):
            row = []
            for _ in range(table_size):
                row.append(False)
            table.append(row)

        # Mark non-accepting and accepting states as different
        for i in range(len(self.states)):
            for j in range(len(self.states)):
                if (self.states[i] in self.accept_states and self.states[j] not in self.accept_states) or \
                        (self.states[j] in self.accept_states and self.states[i] not in self.accept_states):
                    table[i][j] = True

        # Step 2: Mark pairs that lead to different states
        changed = True
        while changed:
            changed = False
            for i in range(len(self.states)):
                for j in range(i + 1, len(self.states)):
                    for symbol in self.alphabet:
                        index_i = self.states.index(
                            self.transitions[(self.states[i], symbol)])
                        index_j = self.states.index(
                            self.transitions[(self.states[j], symbol)])
                        if table[index_i][index_j] or table[index_j][index_i]:
                            if not table[i][j]:
                                table[i][j] = True
                                changed = True

            # Step 3: Merge equivalent states
            equivalent_groups = []
            for i in range(len(self.states)):
                for j in range(i + 1, len(self.states)):
                    if not table[i][j]:
                        found = False
                        for group in equivalent_groups:
                            if self.states[i] in group or self.states[j] in group:
                                group.add(self.states[i])
                                group.add(self.states[j])
                                found = True
                                break
                        if not found:
                            equivalent_groups.append({self.states[i], self.states[j]})

        # Reconstruct the minimized DFA
        new_start_state = None
        if equivalent_groups or len(self.states) > len(equivalent_groups):
            new_states = []
            new_transitions = {}
            new_accept_states = []

            for state in self.states:
                found = False
                for group in equivalent_groups:
                    if state in group:
                        found = True
                        break
                if not found:
                    equivalent_groups.append({state})

            for group in equivalent_groups:
                group = sorted(group)
                try:
                    new_state = ",".join(group)
                except:
                    new_state = ""
                    for i in new_state:
                        new_state += i
                new_states.append(new_state)

                if list(group)[0] == self.start_state:
                    new_start_state = new_state

                if any(state in self.accept_states for state in group):
                    new_accept_states.append(new_state)

            for group in equivalent_groups:
                for symbol in self.alphabet:
                    next_state = None
                    for state in group:
                        state_trans = self.transitions.get((state, symbol))
                        if state_trans:
                            next_group = None
                            for eq_group in equivalent_groups:
                                if state_trans in eq_group:
                                    next_group = sorted(eq_group)
                                    break
                            if next_group:
                                next_state = ",".join(next_group)
                                break
                    if next_state:
                        new_transitions[(",".join(sorted(group)), symbol)] = next_state

            self.start_state = new_start_state
            self.transitions = new_transitions
            self.states = new_states
            self.accept_states = new_accept_states
            return DFA(new_states, self.alphabet, new_transitions, new_start_state, new_accept_states)
        else:
            return self  # No minimization needed

    def are_equivalent(self, other_dfa):

        for dfa_1, dfa_2 in zip(self.start_state, other_dfa.start_state):
            if (dfa_1 in self.accept_states and dfa_2 not in other_dfa.accept_states) or \
                    (dfa_2 in other_dfa.accept_states and dfa_1 not in self.accept_states):
                return False
            for state_1, state_2 in zip(self.states, other_dfa.states):
                for symbol_1, symbol_2 in zip(self.alphabet, other_dfa.alphabet):
                    if ((state_1, symbol_1) in self.transitions) and ((state_2, symbol_2) in other_dfa.transitions):
                        next_state_1 = self.transitions[(state_1, symbol_1)]
                        next_state_2 = other_dfa.transitions[(
                            state_2, symbol_2)]
                        if (next_state_1 in self.accept_states and next_state_2 not in other_dfa.accept_states) or \
                                (next_state_2 in other_dfa.accept_states and next_state_1 not in self.accept_states):
                            return False
            return True
        
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

                for state in nfa.accept_states:
                    if 'ε' not in nfa.transitions[state]:
                        nfa.transitions[state]['ε'] = [nfa.start_state]
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

        minimized_dfa1 = dfa1.minimize()
        minimized_dfa2 = dfa2.minimize()
        # Use are_equivalent method from the Dfa class to compare languages
        
        return minimized_dfa1.are_equivalent(minimized_dfa2)

    def is_relation(self, expression1, expression2):
        if self.is_subset(expression1, expression2) or self.is_subset(expression2, expression1):
            return True

    def is_subset(self, expression1, expression2):
        dfa1 = self.to_dfa(expression1)
        dfa2 = self.to_dfa(expression2)

        def are_dfas_subsets(dfa1, dfa2):
            state_mapping = {state1: state2 for state1, state2 in zip(dfa1.states, dfa2.states)}
            if set(dfa1.alphabet) <= set(dfa2.alphabet):
                if all(
                    state_mapping[state1] in dfa2.transitions and symbol in dfa2.transitions[state_mapping[state1]]
                    for state1 in dfa1.transitions
                    for symbol in dfa1.transitions[state1]
                ):
                    if state_mapping[dfa1.start_state] in dfa2.states:
                        if set(state_mapping[state1] for state1 in dfa1.accept_states) <= set(dfa2.states):
                            return True

            return False
        return are_dfas_subsets(dfa1, dfa2)
    