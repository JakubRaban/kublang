import helpers
import optimize
from parse import parser
import lex
import names


def execute(code):
    if len(code) > 1:
        # lex.process_tokens(code)
        root = parser.parse(code)
        optimize.simplify_while_statements(root)
        print(root)
        root.evaluate(names.NameTable())


choice = 0
while choice not in (1, 2):
    print('Choose how you provide input: ')
    print('[1] From console')
    print('[2] From file')
    try:
        choice = int(input('Choice: '))
    except ValueError: print()

if choice == 1:
    while True:
        program = ''
        while line := input('>>> '):
            program += line + '\n'
        execute(program)
else:
    filename = input('Type filename (or leave blank to load examples/collatz.orl): ') or 'examples/collatz.orl'
    with open(filename, 'r') as file:
        program = file.read()
    execute(program)
