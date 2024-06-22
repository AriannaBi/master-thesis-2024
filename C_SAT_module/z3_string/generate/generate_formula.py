import maude
import os.path
import numpy as np
import pandas as pd
import sys
import random

# python3 generate_formula.py 


def generate_LTL(ap, file_name):
    maude.init(advise=True)
    maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_formula_LTL.maude'))
    m = maude.getCurrentModule()

    t = m.parseTerm('M')
    pattern = m.parseTerm('M')

    with open(file_name, 'w', newline='') as file:
        i = 0
        for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=3):
            # if M is not in the solution, print it
            if (str(sol).find('M') == -1):
                i += 1
                file.write( str(sol) + '\n')


    print("Written file ",file_name, ", Total formulas: ", i)





if __name__ == "__main__":
    file_name_LTL = 'output/formulas_LTL.txt'
    try_file = open(file_name_LTL, 'w')
    if try_file:
        try_file.close()

    generate_LTL([], file_name_LTL)

