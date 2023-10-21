
import os

def fstr(template):
    return eval(f"f'{template}'")

location = 'sample'

st = os.environ['SECRET1']
print(fstr(st))

