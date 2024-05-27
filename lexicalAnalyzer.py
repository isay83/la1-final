class Lexer:
    def __init__(self, alphabet, tokens):
        self.alphabet = alphabet
        self.tokens = tokens
        self.transition_table = self.build_transition_table()
        self.accepting_states = self.build_accepting_states()

    def build_transition_table(self):
        transition_table = [[50] * len(self.alphabet) for _ in range(35)]

        # Definir transiciones específicas basadas en las reglas de tokens
        transition_table[0][self.alphabet.index('i')] = 1  # para "if" o "int"
        transition_table[0][self.alphabet.index('*')] = 4  # para "*"
        transition_table[0][self.alphabet.index('+')] = 5  # para "+"
        transition_table[0][self.alphabet.index('>')] = 6  # para ">"
        transition_table[0][self.alphabet.index('&')] = 7  # para "&&"
        transition_table[0][self.alphabet.index('(')] = 8  # para "("
        transition_table[0][self.alphabet.index(')')] = 9  # para ")"
        transition_table[0][self.alphabet.index('{')] = 10 # para "{"
        transition_table[0][self.alphabet.index(']')] = 11 # para "]"
        transition_table[0][self.alphabet.index(';')] = 12 # para ";"

        for i in range(10):  # dígitos 0-9
            transition_table[0][self.alphabet.index(str(i))] = 13
            transition_table[13][self.alphabet.index(str(i))] = 13
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            if letter in self.alphabet:
                transition_table[0][self.alphabet.index(letter)] = 14
                transition_table[14][self.alphabet.index(letter)] = 14

        transition_table[1][self.alphabet.index('f')] = 15  # "if"
        transition_table[1][self.alphabet.index('n')] = 16  # "int"
        transition_table[16][self.alphabet.index('t')] = 17 # "int"

        # Manejo de números decimales
        transition_table[13][self.alphabet.index('.')] = 18
        for i in range(10):
            transition_table[18][self.alphabet.index(str(i))] = 19
            transition_table[19][self.alphabet.index(str(i))] = 19

        return transition_table

    def build_accepting_states(self):
        return {
            1: 'TOKEN',
            2: 'IDENTIFIER',
            3: 'CONSTANT',
            4: 'STRING',
            5: 'ADD',
            6: 'GT',
            7: 'AND',
            8: 'LPAREN',
            9: 'RPAREN',
            10: 'LBRACE',
            11: 'RBRACKET',
            12: 'SEMI',
            13: 'NUMBER',
            14: 'TOKEN',
            15: 'IF',
            17: 'INT',
            19: 'NUMBER'
        }

    def char_type(self, char):
        if char in self.alphabet:
            return self.alphabet.index(char)
        else:
            return 33  # Estado de error para caracteres no permitidos

    def scan(self, text):
        state = 0
        tokens = []
        current_token = ''

        for char in text:
            if char.isspace():
                if state != 0 and current_token:
                    if state in self.accepting_states:
                        tokens.append((self.accepting_states[state], current_token))
                    else:
                        tokens.append(('ERROR', current_token))
                    current_token = ''
                    state = 0
                continue

            ctype = self.char_type(char)
            new_state = self.transition_table[state][ctype]

            if new_state == 50:  # Estado de error
                raise ValueError(f"Unexpected character '{char}' at state {state}")

            current_token += char
            state = new_state

        if state != 0 and current_token:
            if state in self.accepting_states:
                tokens.append((self.accepting_states[state], current_token))
            else:
                tokens.append(('ERROR', current_token))

        return tokens

    def analyze_file(self, input_file, output_file):
        with open(input_file, 'r') as infile:
            text = infile.read()

        tokens = self.scan(text)

        with open(output_file, 'w') as outfile:
            for token in tokens:
                outfile.write(f"{token[0]}: {token[1]}\n")


# Alfabeto y tokens definidos
alphabet = list('abcfinputuz0123456789.;*+<>&_={ñ()[]} ')
tokens = ['int', 'input', 'if', '*', '+', '>', '&&', '(', ')', '{', '}', ';']

# Crear una instancia del Lexer y analizar un archivo
lexer = Lexer(alphabet, tokens)
lexer.analyze_file('in.txt', 'out.txt')
