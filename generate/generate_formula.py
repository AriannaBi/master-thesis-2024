import maude
import os.path
import numpy as np
import pandas as pd
import sys
import random

# python3 generate_formula.py -LTL


def add_random_ap(ap, formula):
    # for each a, replace it with a different random choice
    new_string = []
    for char in formula:
        if char == "a":
            # Generate a random number between 0 and 9 (inclusive)
            random_ap = np.random.choice(ap)
            new_string.append(random_ap)
        else:
            new_string.append(char)
    # formula = formula.replace("a", )
    # formula = formula.replace("a", np.random.choice(ap))
    return ''.join(new_string)

# Generate LTL
# file_name is the output file 
def generate_LTL(ap, file_name):
    maude.init(advise=True)
    maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_formula_LTL.maude'))
    m = maude.getCurrentModule()

    t = m.parseTerm('M') #before it was (M)&(M)
    pattern = m.parseTerm('M')

    with open(file_name, 'w', newline='') as file:
        i = 0
        for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=4):
            # if M is not in the solution, print it
            if (str(sol).find('M') == -1):
                i += 1
                file.write( str(sol) + '\n')


    print("Written file ",file_name, ", Total formulas: ", i)


# Generate CTL
def generate_CTL(ap, file_name):
    maude.init(advise=True)
    maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_formula_CTL.maude'))
    m = maude.getCurrentModule()

# why A M ?
    t = m.parseTerm('M')
    pattern = m.parseTerm('M')

    with open(file_name, 'w', newline='') as file:
        i = 0
        for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=4):
            # if M is not in the solution, print it
            if (str(sol).find('M') == -1):
                i += 1
                file.write(str(sol) + '\n')
                # file.write(add_random_ap(ap, str(sol)) + '\n')
                        # print(sol, subs, path())


# check if nrew and i are working properly because it seems that without any if condition they are differ.
    print("Written file ",file_name, ", Total formulas: ", i)


def main(ap):
    file_name_LTL = 'output/formulas_LTL.txt'
    file_name_CTL = 'output/formulas_CTL.txt'
    if LTL == True:
        generate_LTL(ap, file_name_LTL)
    elif CTL == True:
        generate_CTL(ap, file_name_CTL)
    else:
        generate_LTL(ap, file_name_LTL)
        generate_CTL(ap, file_name_CTL)




if __name__ == "__main__":


    # possible inputs:
    # generate_formula.py -LTL a,b,c
    # generate_formula.py -CTL a,b,c
    # generate_formula.py a,b,c


    try_file = open('output/formulas_LTL.txt', 'w')
    if try_file:
        try_file.close()

    try_file = open('output/formulas_CTL.txt', 'w')
    if try_file:
        try_file.close()


    LTL = False
    CTL = False
    ap = []

    if(len(sys.argv) > 2):
        ap = sys.argv[2].split(",")
    if sys.argv[1] == "-LTL":
        LTL = True
    elif sys.argv[1] == "-CTL":
        CTL = True
    else:
        ap = sys.argv[1].split(",")


    main(ap)
    print("\n\n")

    