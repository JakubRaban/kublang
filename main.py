
from parse import parser
import names


def execute(code):
    if len(code) > 1:
        root = parser.parse(code)
        print(root)
        root.evaluate(names.NameTable())


choice = 0
while choice not in (1, 2):
    print('Choose how you provide input: ')
    print('[1] From console')
    print('[2] From file')
    choice = int(input('Choice: '))

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
