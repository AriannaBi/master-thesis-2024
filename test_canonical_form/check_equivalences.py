# Description: Check if two formulas are equivalent
# Implemented using spot library and spot function are_equivalent
# Requirements: spot library 
# Usage: python3 check_if_equivalent.py
# I am using it with conda3 environment with spot library installed


import spot


file_in = open('output/spot_no_options.txt', 'r') #read formula and relative mutants
Lines = file_in.readlines()

n_mutants = 0
n_formulas = 0
const = False

for idx, line in enumerate( Lines):
    n_formulas += 1
    array_formula = line.split("   ") #last element is \n
    array_formula = array_formula[1:]
    array_formula = [x.strip("\n") for x in array_formula] #remove empty elements ''
    original_formula = array_formula[0]
    mutants = array_formula[1:]

    const = False
    for mutant in mutants:
        n_mutants += 1
        are_eq = spot.are_equivalent(original_formula, mutant)
        if are_eq == False:
            print(are_eq, original_formula, mutant)
        if original_formula != mutant:
            const = True
            print(idx + 1, end=' ')
    if const == True:
      print('\n')
print("Checked ", n_formulas, "formulas and ", n_mutants, " mutants")