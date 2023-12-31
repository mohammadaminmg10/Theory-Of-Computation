class PDA:
    def __init__(self):
        self.stack = []

    def push(self, symbol):
        self.stack.append(symbol)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            return None

    def is_empty(self):
        return len(self.stack) == 0

    def process_string(self, input_string):
        for symbol in input_string:
            if symbol == 'a':
                self.push(symbol)
                print(f"Pushed 'a', Stack: {self.stack}")
            elif symbol == 'b':
                popped_symbol = self.pop()
                if popped_symbol == 'a':
                    print(f"Popped 'a', Stack: {self.stack}")
                else:
                    print("Invalid input! 'b' cannot be processed.")
                    return
            else:
                print("Invalid input! Only 'a' and 'b' are allowed.")
                return

        if self.is_empty():
            print("String accepted by the PDA.")
        else:
            print("String not accepted by the PDA.")

pda1 = PDA()

accepted_string = "aabb"
print(f"Processing string: {accepted_string}")
pda1.process_string(accepted_string)

pda2 = PDA()
rejected_string = "aabbbaa"
print(f"\nProcessing string: {rejected_string}")
pda2.process_string(rejected_string)
