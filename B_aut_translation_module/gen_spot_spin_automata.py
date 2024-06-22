import spot
import os
import subprocess

# Given ONE formula, generate two automatas, one using spot and the other using spin. the formula is the original and the mutant
# After that check if the two automatas:
#  are equivalent, and not isomorphic and not equal : they are going to be used in the checking module. 
#  are not equivalent : almost impossible because it means there is an error in the translator modules. 


# # give two equivalent formulas
# spot_command = "ltl2tgba -f 'G(a U Fb)'"
# spin_command = "spin -f '[] (a U <> b)' -a"


# STEPS :
# Read the formulas, either the original and mutants, but feed only one formula in the program, that is going to be used twice to generate the automatas.
# The formulas are in spot syntax, so write a simple function to conver the formulas into spin syntax. 
# Generate the automatas with the different translators and save them in files.
# Do the comparision of the automatas and report the result. 


# INPUT: FILTERED_MUTANTS_LTL.TXT
# OUTPUT: HOA_AUT.TXT

def spot_to_spin(formula):
    formula = formula.replace('G', '[]')
    formula = formula.replace('F', '<>')
    formula = formula.replace('|', '||')
    formula = formula.replace('&', '&&')
    return formula

try_file = open('files/HOA_aut.txt', 'w')
if try_file:
    try_file.close()

f = open("../generate/output/filtered_mutants_LTL.txt", "r")
lines = f.readlines()
# lines[:20]
for line in lines:
    formulas = line.split(' ')
    # let's start to do it with the original formulas. and then we can move to the mutants.
    # print(formulas)
    formulas = line.split(' ')[:-1] #last element is \n
    formulas = [x for x in formulas if x] #remove empty elements ''
    for formula in formulas:
    #     spot_command = "ltl2tgba -f '" + spot_to_spin(formula) + "'"
        spot_command = "ltl2tgba -B '" + formula + "'"
        spin_command = "spin -f '" + spot_to_spin(formula) + "' -a"

        # print(spot_command), print(spin_command)

        # create the automatas
        spot_automata_HOA = subprocess.run(spot_command, shell=True, capture_output=True, text=True)
        spin_automata_HOA = subprocess.run(spin_command, shell=True, capture_output=True, text=True)

        # save and convert the spin automata from neverclaim to hoa 
        file_name_spin = "spin_never_claim.never"
        with open(file_name_spin, 'w') as file:
            file.write(spin_automata_HOA.stdout)
        spin_automata_HOA = spot.automaton(file_name_spin).to_str('hoa')

        
        file_Hoa_aut = "files/HOA_aut.txt"
        with open(file_Hoa_aut, 'a') as file:
            file.write(spot_automata_HOA.stdout)
            file.write(".\n")
            file.write(spin_automata_HOA)
            file.write("\n~\n")


        # delete the file 
        if os.path.exists("spin_never_claim.never"):
            os.remove("spin_never_claim.never")

