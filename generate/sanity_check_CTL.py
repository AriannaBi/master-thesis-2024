# Uses ctl-sat from https://github.com/nicolaprezza/CTLSAT

# This script generates a sanity check for the CTL model checker.

import os
# python3 sanity_check_CTL.py
# read file with formulas and relative mutants

# !(f <=> g) is UNSAT then f and g are equivalent
# Since <=> doesn't exist in CTL sat tool, we use !(f <=> g)  =  !(f -> g) ^ !(g -> f)

# Neither (Φ∧¬Ψ) nor (Ψ∧¬Φ) is satisfiable".
# Since Φ∧¬Ψ is equivalent to ¬(Φ -> Ψ) and Ψ∧¬Φ is equivalent to ¬(Ψ -> Φ), we can check if both are unsatisfiable




file_in = open('output/filtered_mutants_CTL.txt', 'r') #read formula and relative mutants
Lines = file_in.readlines()

n_mutants = 0
n_formulas = 0
for line in Lines[:20]:
    n_formulas += 1

    # line = f'"{line.strip()}"'
    
    # os.system(f"./ctl-sat {line}")
    array_formula = line.split('.')[:-1] #last element is \n
    array_formula = [x for x in array_formula if x] #remove empty elements ''
    print(array_formula)
    original_formula = array_formula[0]
    f = original_formula
    # f = f'"{original_formula.strip()}"'
    mutants = array_formula[1:]
    for mutant in mutants:
        n_mutants += 1
        g = mutant
        # g = f'"{mutant.strip()}"'
        check_UNSAT = f'"~((({f}) -> ({g})) ^ (({g}) -> ({f})))"'
        # check_UNSAT_1 = f'"~({f} -> {g})"'
        # check_UNSUT_2 = f'"~({g} -> {f}))"'
        # print(check_UNSAT)
        os.system(f"./ctl-sat {check_UNSAT}")
        # os.system(f"./ctl-sat {check_UNSUT_2}")
        # are_eq = spot.are_equivalent(replace_atomic_proposition(original_formula), replace_atomic_proposition(mutant))
        # if are_eq == False:
        #     print(mutant)
        #     print(original_formula)
        #     print(are_eq)

# print("Checked ", n_formulas, "formulas and ", n_mutants, " mutants")
# ~(((~(AF a))^(~(AF a)) -> (~(AF a))^(EG ~(a))) v ((~(AF a))^(EG ~(a)) -> (~(AF a))^(~(AF a)))


# "~(((~( ( EFEGa ^ AG(a->b) ) -> EFEGb )) -> (~( ( EFEGa ^ AG(a->b) ) -> EFEGb ))) v ((~( ( EFEGa ^ AG(a->b) ) -> EFEGb )) -> (~( ( EFEGa ^ AG(a->b) ) -> EFEGb ))))"