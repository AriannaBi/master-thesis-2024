import maude
import os.path
import numpy as np
import pandas as pd
import sys

# python3 generate_formula.py -LTL

# deletecontent of file because we will append formulas and mutants from scratch
try_file = open('output/formulas_LTL.txt', 'w')
if try_file:
    try_file.close()

try_file = open('output/formulas_CTL.txt', 'w')
if try_file:
    try_file.close()

LTL = False
CTL = False
if len(sys.argv) > 1:
    if sys.argv[1] == "-LTL":
        LTL = True
    elif sys.argv[1] == "-CTL":
        CTL = True





# Generate LTL
def generate_LTL():
    maude.init(advise=True)
    maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_formula_LTL.maude'))
    m = maude.getCurrentModule()

    t = m.parseTerm('M')
    pattern = m.parseTerm('M')

    with open('output/formulas_LTL.txt', 'w', newline='') as file:
        i = 0
        for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=2):
            # if M is not in the solution, print it
            if (str(sol).find('M') == -1):
                i += 1
                # print(sol) 
                file.write(str(sol) + '\n')


    print("Written file output/formulas_LTL.txt, Totale: ", nrew, "    Completed: ", i)


# Generate CTL
def generate_CTL():
    maude.init(advise=True)
    maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_formula_CTL.maude'))
    m = maude.getCurrentModule()

# why A M ?
    t = m.parseTerm('M')
    pattern = m.parseTerm('M')

    with open('output/formulas_CTL.txt', 'w', newline='') as file:
        i = 0
        for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=4):
            # if M is not in the solution, print it
            if (str(sol).find('M') == -1):
                # if (str(sol).find('A A') == -1) and (str(sol).find('E E') == -1) and (str(sol).find('E A') == -1) and (str(sol).find('A E') == -1) and (str(sol).find("A a") == -1) and (str(sol).find("A (a)") == -1):
                    # if (str(sol).find('A') != -1) or (str(sol).find('E') != -1):
                i += 1
                file.write(str(sol) + '\n')
                        # print(sol, subs, path())


# check if nrew and i are working properly because it seems that without any if condition they are differ.
    print("Written file output/formulas_CTL.txt, Totale: ", nrew, "    Completed: ", i)




if LTL == True:
    generate_LTL()
elif CTL == True:
    generate_CTL()
else:
    generate_LTL()
    generate_CTL()