# Description: Check if two formulas are equivalent
# Implemented using spot library and spot function are_equivalent
# Requirements: spot library 
# Usage: python3 check_if_equivalent.py
# I am using it with conda3 environment with spot library installed


import spot
# print(spot.version())
print(sys.path)
# formula1 = spot.formula("s=1")
# formula2 = spot.formula("s=1")
are_eq = spot.are_equivalent("s=2", "s=2")
print("Equivalent" if are_eq else "Not equivalent")

# file_in = open('mutants.txt', 'r') #read formula and relative mutants
# Lines = file_in.readlines()

# phi = ''
# phi_prime = ''

# for line in Lines[:10]:
#     # print(line)
#     array_formula = line.split('..')[:-1] #last element is \n
#     # print(array_formula)
#     original_formula = array_formula[0]
#     mutants = array_formula[1:]
#     for mutant in mutants:
#         print(mutant)
#         are_eq = spot.are_equivalent(original_formula, mutant)
#         print(are_eq)