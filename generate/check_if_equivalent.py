# Description: Check if two formulas are equivalent
# Implemented using spot library and spot function are_equivalent
# Requirements: spot library 
# Usage: python3 check_if_equivalent.py
# I am using it with conda3 environment with spot library installed


import spot
# print(spot.version())


#############################################
# with spot, s=1, s=2 are not considered atomic porposition, hence we need to temporally replace them with p1, p2 ...
# set a dictionary s=1 -> p1, s=2 -> p2, ...
dict_atomic_proposition = {'s=' + str(i): 'repl' + str(i) for i in range(0, 9)}
dict_atomic_proposition.update({'s!=' + str(i): 'replnot' + str(i) for i in range(0, 9)})
# print(dict_atomic_proposition)


# replace atomic proposition in formula
def replace_atomic_proposition(formula):
    for key in dict_atomic_proposition:
        formula = formula.replace(key, dict_atomic_proposition[key])
    return formula

# test replace_atomic_proposition and replace_back_atomic_proposition
formula1 = replace_atomic_proposition("((s=0)U(s=1))|((s=0)U(s=3))")
formula2 = replace_atomic_proposition("((s=0)U(s=1))|((s=0)U(s=3))")
are_eq = spot.are_equivalent(formula1, formula2)
assert are_eq == True
#############################################


file_in = open('mutants.txt', 'r') #read formula and relative mutants
Lines = file_in.readlines()

n_mutants = 0
n_formulas = 0
for line in Lines:
    n_formulas += 1
    array_formula = line.split('..')[:-1] #last element is \n
    original_formula = array_formula[0]
    mutants = array_formula[1:]
    for mutant in mutants:
        n_mutants += 1
        are_eq = spot.are_equivalent(replace_atomic_proposition(original_formula), replace_atomic_proposition(mutant))
        if are_eq == False:
            print(mutant)
            print(original_formula)
            print(are_eq)

print("Read ", n_formulas, "formulas and ", n_mutants, " mutants")
            