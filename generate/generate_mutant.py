import maude
import os.path
import numpy as np
import os

# deletecontent of file because we will append formulas and mutants from scratch
try_file = open('output/mutants_LTL.txt', 'w')
if try_file:
    try_file.close()

try_file = open('output/mutants_CTL.txt', 'w')
if try_file:
    try_file.close()




############################################## LTL ######################################################

maude.init(advise=True)
maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_mutant_LTL.maude'))
m = maude.getCurrentModule()
# print('Using', m, 'module')



# Using readlines()
file_in = open('output/formulas_LTL.txt', 'r') #read formula
# file_out formatted as formula .. mutant .. mutant .. mutant 
file_out = open('output/mutants_LTL.txt', 'a') #write formula and append mutants
Lines = file_in.readlines()

n_formula = 0
for line in Lines:
    n_formula += 1
    t = m.parseTerm(line)
    # print("PHI ", t)
    file_out.write(str(t) + '..' + "" )
    pattern = m.parseTerm('M')

    n_mutant=0
    for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=2):
        # if M is not in the solution, print it
        if (str(sol).find('M') == -1):
        # if (str(sol).find('M') == -1) and str(sol) != str(t): #exclude the formula itself from the mutants
            n_mutant += 1
            file_out.write(str(sol) +  '..' + "")
    file_out.write('\n')

print("Written file output/mutants_LTL.txt, Read  ", n_formula, " formulas and  ", n_mutant, " mutants")

file_in.close()
file_out.close()


############################################## CTL ######################################################

maude.init(advise=True)
maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_mutant_CTL.maude'))
m = maude.getCurrentModule()
# print('Using', m, 'module')



# Using readlines()
file_in = open('output/formulas_CTL.txt', 'r') #read formula
# file_out formatted as formula .. mutant .. mutant .. mutant 
file_out = open('output/mutants_CTL.txt', 'a') #write formula and append mutants
Lines = file_in.readlines()

n_formula = 0
for line in Lines:
    n_formula += 1
    t = m.parseTerm(line)
    file_out.write(str(t) + '..' + "" )
    pattern = m.parseTerm('M')

    n_mutant=0
    for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=2):
        # if M is not in the solution, print it
        # if it contains A or E keep it 
        if (str(sol).find('M') == -1) and (str(sol).find('A') == 1) and (str(sol).find('E') == 1):
        # if (str(sol).find('M') == -1) and str(sol) != str(t): #exclude the formula itself from the mutants
            n_mutant += 1
            file_out.write(str(sol) +  '..' + "")
    file_out.write('\n')

print("Written file output/mutants_CTL.txt, Read  ", n_formula, " formulas and  ", n_mutant, " mutants")

file_in.close()
file_out.close()