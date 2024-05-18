# Uses ctl-sat from https://github.com/nicolaprezza/CTLSAT

# This script generates a sanity check for the CTL model checker.

import os
import subprocess
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
for line in Lines:
    n_formulas += 1
    array_formula = line.split(' ')[:-1] #last element is \n
    array_formula = [x for x in array_formula if x] #remove empty elements ''
    print(array_formula)
    original_formula = array_formula[0]
    f = original_formula
    mutants = array_formula[1:]

    for mutant in mutants:
        n_mutants += 1
        g = mutant
        check_UNSAT = f'"~((({f}) -> ({g})) ^ (({g}) -> ({f})))"'
        # os.system(f"./ctl-sat {check_UNSAT}")
        command = f"./ctl-sat {check_UNSAT}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # print(result.stdout)
        if result.returncode == 0:
            # if result not contain ("is NOT satisfiable")
            if "is satisfiable" in result.stdout or "Error" in result.stdout:
                print("Error: ", result.stdout)
        else:
            # Print an error message
            print("Error executing command:", result.stderr)

