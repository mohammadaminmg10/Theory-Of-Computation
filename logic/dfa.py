
class Dfa:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def is_empty_language(self):
        if not self.accept_states:
            return True
        if self.start_state in self.accept_states:
            return False
        for state in self.states:
            for symbol in self.alphabet:
                next_state = self.transitions[(state, symbol)]
                if next_state in self.accept_states:
                    return False
        return True

    def is_trap(self, state):
        for symbol in self.alphabet:
            if self.transitions[(state, symbol)] != state:
                return False
        return True

    def is_finite(self):
        """
        Q2
        Checks whether the language of the DFA is finite.
        :return: True if the language is finite, False otherwise.
        """
        if self.is_empty_language():
            return True

        self.minimize()
        for state in self.states:
            for symbol in self.alphabet:
                next_state = self.transitions[(state, symbol)]
                if next_state == state:
                    if not self.is_trap(state):
                        return False
                    if state in self.accept_states:
                        return False          
        return True

    def all_strings(self):
        """
        Q2*
        Returns all strings in the language of the DFA.
        :return: A set of all strings in the language.
        """
        strings = set()
        if self.is_empty_language():
            return set()

        if not self.is_finite():
            return None

        def DFS(state, string):
            if self.is_trap(state):
                strings.add(string[:-1])
                return
            if state in self.accept_states:
                strings.add(string)
            for symbol in self.alphabet:
                next_state = self.transitions[(state, symbol)]
                DFS(next_state, string + symbol)
        DFS(self.start_state, '')
        return strings, len(strings)

    def accepts_string(self, input_string):
        current_state = self.start_state

        for symbol in input_string:
            if (current_state, symbol) in self.transitions:
                current_state = self.transitions[(current_state, symbol)]
            else:
                return False

        return current_state in self.accept_states

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
                new_state = ",".join(group)
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
            return Dfa(new_states, self.alphabet, new_transitions, new_start_state, new_accept_states)
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
