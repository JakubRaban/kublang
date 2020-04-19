
from parse import parser
import names


def execute(code):
    if len(code) > 1:
        root = parser.parse(code)
        print(root)
        root.evaluate(names.VariableArray())


choice = 0
while choice not in (1, 2):
    print("Wybierz sposób wczytania kodu programu: ")
    print("[1] Z konsoli")
    print('[2] Z pliku')
    choice = int(input('Wybór: '))

if choice == 1:
    while True:
        program = ''
        while line := input('>>> '):
            program += line + '\n'
        execute(program)
else:
    filename = input('Podaj nazwę pliku (pozostaw puste by załadować examples/collatz.kub): ') or 'examples/collatz.kub'
    with open(filename, 'r') as file:
        program = file.read()
    execute(program)
