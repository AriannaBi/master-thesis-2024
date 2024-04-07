import maude
import os.path
import numpy as np
import pandas as pd

# deletecontent of file because we will append formulas and mutants from scratch
try_file = open('output/formulas_LTL.txt', 'w')
if try_file:
    try_file.close()

try_file = open('output/formulas_CTL.txt', 'w')
if try_file:
    try_file.close()




############################################# LTL #######################################################

maude.init(advise=True)
maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_formula_LTL.maude'))
m = maude.getCurrentModule()
# print('Using', m, 'module')

t = m.parseTerm('M')
pattern = m.parseTerm('M')


# for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=3):
#         # if M is not in the solution, print it
#         # if (str(sol).find('M') == -1):
#         print(sol) 


with open('output/formulas_LTL.txt', 'w', newline='') as file:
    i = 0
    for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=3):
        # if M is not in the solution, print it
        if (str(sol).find('M') == -1):
            i += 1
            # print(sol) 
            file.write(str(sol) + '\n')


print("Written file output/formulas_LTL.txt, Totale: ", nrew, "    Completed: ", i)

############################################## CTL ######################################################

maude.init(advise=True)
maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_formula_CTL.maude'))
m = maude.getModule('gen_formula_CTL')
# print('Using', m, 'module')

t = m.parseTerm('M')
pattern = m.parseTerm('M')


with open('output/formulas_CTL.txt', 'w', newline='') as file:
    i = 0
    for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=4):
        # if M is not in the solution, print it
        if (str(sol).find('M') == -1):
            if (str(sol).find('A') != -1) or (str(sol).find('E') != -1):
                i += 1
                file.write(str(sol) + '\n')


print("Written file output/formulas_CTL.txt, Totale: ", nrew, "    Completed: ", i)