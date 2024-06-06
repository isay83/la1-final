class Lexer:
    def __init__(self, alphabet, tokens):
        self.alphabet = alphabet
        self.tokens = tokens
        self.transition_table = self.build_transition_table()
        self.accepting_states = self.build_accepting_states()

    def build_transition_table(self):
        transition_table = [[50] * len(self.alphabet) for _ in range(500)]
        # Definir transiciones específicas basadas en las reglas de tokens
        transition_table[0][self.alphabet.index('i')] = 10  # para "if", "int" o "input"
        transition_table[10][self.alphabet.index('n')] = 11  # para "int" o "input"
        transition_table[11][self.alphabet.index('t')] = 1  # para "int"
        transition_table[10][self.alphabet.index('f')] = 1  # "if"
        transition_table[11][self.alphabet.index('p')] = 12  # "input"
        transition_table[12][self.alphabet.index('u')] = 13  # "input"
        transition_table[13][self.alphabet.index('t')] = 1  # "input"

        transition_table[0][self.alphabet.index('*')] = 1  # para "*"
        transition_table[0][self.alphabet.index('+')] = 1  # para "+"
        transition_table[0][self.alphabet.index('>')] = 1  # para ">"
        transition_table[0][self.alphabet.index('&')] = 14  # para "&&"
        transition_table[14][self.alphabet.index('&')] = 1  # para "&&"
        transition_table[0][self.alphabet.index('(')] = 1  # para "("
        transition_table[0][self.alphabet.index(')')] = 1  # para ")"
        transition_table[0][self.alphabet.index('{')] = 1  # para "{"
        transition_table[0][self.alphabet.index(']')] = 1  # para "]"
        transition_table[0][self.alphabet.index(';')] = 1  # para ";"
        
        for char in '0123456789.;*+<>&_={ñ()[]}':
            transition_table[1][self.alphabet.index(char)] = 7
        # para numerical constant
        for i in range(10):  # dígitos 0-9
            transition_table[0][self.alphabet.index(str(i))] = 3
            transition_table[3][self.alphabet.index(str(i))] = 3
        transition_table[3][self.alphabet.index('.')] = 4
        for i in range(10):
            transition_table[4][self.alphabet.index(str(i))] = 5
            transition_table[5][self.alphabet.index(str(i))] = 5
            transition_table[6][self.alphabet.index(str(i))] = 6
            transition_table[7][self.alphabet.index(str(i))] = 7 # para invalid string
        transition_table[5][self.alphabet.index('.')] = 6
        transition_table[7][self.alphabet.index('.')] = 7 # para invalid string
        # para identifier
        for letter in 'aifnputz_':
            transition_table[0][self.alphabet.index(letter)] = 2
            transition_table[2][self.alphabet.index(letter)] = 2
            transition_table[3][self.alphabet.index(letter)] = 4 # para invalid numeric string
            transition_table[4][self.alphabet.index(letter)] = 4 # para invalid numeric string
            transition_table[5][self.alphabet.index(letter)] = 6 # para invalid numeric string
            transition_table[6][self.alphabet.index(letter)] = 6 # para invalid numeric string
            transition_table[7][self.alphabet.index(letter)] = 7 # para invalid string
            for digit in '0123456789':
                transition_table[2][self.alphabet.index(digit)] = 2
            for token in '*+>&(){];':
                transition_table[2][self.alphabet.index(token)] = 7
        # para invalid string
        for letter in 'ñ':
            transition_table[0][self.alphabet.index(letter)] = 7
            transition_table[2][self.alphabet.index(letter)] = 7

        return transition_table

    def build_accepting_states(self):
        return {
            1: 'TOKEN',
            2: 'IDENTIFIER',
            3: 'NUMERICAL CONSTANT',
            4: 'INVALID STRING',
            5: 'INVALID NUMERIC STRING',
            50: 'UNEXPECTED CHARACTER',
            10: 'n',
            11: 't',
            12: '_',
            13: '',
            14: 'n',
            15: 't',
            16: '_',
            17: '',
            18: '',
            19: ''
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
                    if state == 1:
                        tokens.append(('TOKEN', current_token))
                    elif state == 2:
                        if current_token in self.tokens:
                            tokens.append(('TOKEN', current_token))
                        else:
                            tokens.append(('IDENTIFIER', current_token))
                    elif state == 3 or state == 5:
                        tokens.append(('NUMERICAL CONSTANT', current_token))
                    elif state == 4 or state == 6:
                        tokens.append(('INVALID NUMERIC STRING', current_token))
                    elif state == 7 or state == 14:
                        tokens.append(('INVALID STRING', current_token))
                    elif state == 50:
                        tokens.append(('UNEXPECTED TOKEN', current_token))
                    current_token = ''
                    state = 0
                continue

            ctype = self.char_type(char)
            new_state = self.transition_table[state][ctype]

            current_token += char
            state = new_state

        if state != 0 and current_token:
            if state == 1:
                tokens.append(('TOKEN', current_token))
            elif state == 2:
                if current_token in self.tokens:
                    tokens.append(('TOKEN', current_token))
                else:
                    tokens.append(('IDENTIFIER', current_token))
            elif state == 3 or state == 5:
                tokens.append(('NUMERICAL CONSTANT', current_token))
            elif state == 4 or state == 6:
                tokens.append(('INVALID NUMERIC STRING', current_token))
            elif state == 7 or state == 14:
                tokens.append(('INVALID STRING', current_token))
            elif state == 50:
                tokens.append(('UNEXPECTED TOKEN', current_token))

        return tokens

    def analyze_file(self, input_file, output_file):
        with open(input_file, 'r') as infile:
            text = infile.read()

        tokens = self.scan(text)

        with open(output_file, 'w') as outfile:
            for token in tokens:
                outfile.write(f"{token[0]}: {token[1]}\n")


# Alfabeto y tokens definidos
alphabet = list('afinputz_0123456789.;*+<>&_={ñ()[]} ')
tokens = ['int', 'input', 'if', '*', '+', '>', '&&', '(', ')', '{', ']', ';']

# Crear una instancia del Lexer y analizar un archivo
lexer = Lexer(alphabet, tokens)
lexer.analyze_file('in.txt', 'out.txt')
