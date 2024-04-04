import maude
import os.path
import numpy as np
import os

maude.init(advise=True)
maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_mutant.maude'))

m = maude.getCurrentModule()
# print('Using', m, 'module')

# deletecontent of file because we will append formulas and mutants from scratch
try_file = open('mutants.txt', 'w')
if try_file:
    try_file.close()

# Using readlines()
file_in = open('formulas.txt', 'r') #read formula
# file_out formatted as formula .. mutant .. mutant .. mutant 
file_out = open('mutants.txt', 'a') #write formula and append mutants
Lines = file_in.readlines()

for line in Lines:
    # line = Lines[85]
    # line = 'X(!(F(!("a"))))'
    # print(line, '\n')

    t = m.parseTerm(line)
    print("PHI ", t)
    file_out.write(str(t) + '..' + "" )
    pattern = m.parseTerm('M')

    i=0
    for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=2):
        # if M is not in the solution, print it
        if (str(sol).find('M') == -1):
        # if (str(sol).find('M') == -1) and str(sol) != str(t): #exclude the formula itself from the mutants
            i += 1
            print("PHI' ",sol) 
            file_out.write(str(sol) +  '..' + "")
    print('\n')
    file_out.write('\n')



file_in.close()
file_out.close()

# number_rules = a.frewrite(bound=20)
# print(a, '\t', "# equivalences: ", number_rules, '\n')
# print("-",line, "-")
# file1.write(line)


# for a in A:
#     # print(a)
#     number_rules = a.frewrite(bound=20) # (bound=-1, gas=-1) stop when there are too many repeated equivalences?
#     print(a, '\t', "# equivalences: ", number_rules, '\n')

