# read the file with the ltl formulas, convert them into spot formula, run the spin -f "..." and take the first two lines of 
# of the verbose output on the terminal. this is the simplified formula that Spin uses to start the model checking process.
import spot
import pandas as pd
import spot
import os
import subprocess
import re


def spot_to_spin(formula):
    formula = formula.replace('G', '[]')
    formula = formula.replace('F', '<>')
    formula = formula.replace('|', '||')
    formula = formula.replace('&', '&&')

    formula = formula.replace('V', '|')
    return formula

try_file = open('output/spin_simpl.txt', 'w')
if try_file:
    try_file.close()



f = open("output/spot_all_options.txt", "r")
lines = f.readlines()
different_formulas = 0
same_formulas = 0
with open("output/spin_simpl.txt", 'a') as file:
    for line in lines:
        formulas = line.split('   ')
        # print(formulas)
        formulas = [x for x in formulas if x] #remove empty elements ''
        for formula in formulas:
            formula = formula.strip('\n')

            spin_command = "spin -f '" + spot_to_spin(formula) + "'"


            spin_automata_HOA = subprocess.run(spin_command, shell=True, capture_output=True, text=True)
            output = spin_automata_HOA.stdout.split('\n')[:2]
            
            normaliz_formula = output[1]
            parsed_formula_spot = ""
            parsed_formula_spin = ""
            if normaliz_formula.find('(') != -1:
                normaliz_formula = re.findall(r'\(.+\)', normaliz_formula)[0].strip(' ')
                parsed_formula_spot = spot.formula(formula)
                parsed_formula_spin = spot.formula(normaliz_formula)
            else:
                normaliz_formula = "."
            # print("non parsed formulas", formula,",", normaliz_formula)
            # print("parsed formulas", parsed_formula_spot,",", parsed_formula_spin)
            
            if (parsed_formula_spin != parsed_formula_spot):
                # print("different formulas: spin ", parsed_formula_spin," and spot ", parsed_formula_spot)
                different_formulas += 1
            else:
                # print("same formulas: spin ", parsed_formula_spin," and spot ", parsed_formula_spot)
                same_formulas += 1
                
            # print("\n")

print("different formulas", different_formulas, "same formulas", same_formulas)
        