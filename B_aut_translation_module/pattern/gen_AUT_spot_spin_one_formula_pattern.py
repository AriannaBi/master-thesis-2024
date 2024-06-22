import spot
import os
import subprocess
import time
import matplotlib.pyplot as plt


# does the same things but the patterns are different because we are reading formulas from http://www.daxc.de/eth/atva07/index.html#firstexp
# maybe this is for the trqnslation formula, since i am testing the ltl to automata translation function to see if it produces 
# equivalent results. 

# Given one formula, generate two automatas, one using spot and the other using spin.
# After that check if the two automatas:
#  are equivalent, and not isomorphic and not equal : they are going to be used in the checking module. 
#  are not equivalent : almost impossible because it means there is an error in the translator modules. 



# # give two equivalent formulas
# spot_command = "ltl2tgba -f 'G(a U Fb)'"
# spin_command = "spin -f '[] (a U <> b)' -a"


# # create the automatas
# spot_automata_HOA = subprocess.run(spot_command, shell=True, capture_output=True, text=True)
# spin_automata_NEVER = subprocess.run(spin_command, shell=True, capture_output=True, text=True)

# # save never claim automata in a file
# file_name = "spin_never_claim.never"
# with open(file_name, 'w') as file:
#     file.write(spin_automata_NEVER.stdout)

# # convert the neverclaim automata to HOA format
# spin_automata_HOA = spot.automaton(file_name).to_str('hoa')
# if os.path.exists(file_name):
#     os.remove(file_name)
# # save spin hoa automata in a file
# with open("spin_automata.hoa", 'w') as file:
#     file.write(spin_automata_HOA)


# # save spot hoa automata in a file
# with open("spot_automata.hoa", 'w') as file:
#     file.write(spot_automata_HOA.stdout)



# STEPS :
# Read the formulas, either the original and mutants, but feed only one formula in the program, that is going to be used twice to generate the automatas.
# The formulas are in spot syntax, so write a simple function to conver the formulas into spin syntax. 
# Generate the automatas with the different translators and save them in files.
# Do the comparision of the automatas and report the result. 


def spot_to_spin(formula):
    formula = formula.replace('G', '[]')
    formula = formula.replace('F', '<>')
    formula = formula.replace('|', '||')
    formula = formula.replace('&', '&&')
    return formula

def spin_to_spot(formula):
    # print(formula)
    symbol_or = '\\/'
    symbol_and = r'/' + r'\\'
    formula = formula.replace('[]', 'G')
    formula = formula.replace('<>', 'F')
    formula = formula.replace(symbol_or, '|')
    formula = formula.replace(symbol_and, '&')
    # print(formula)
    return formula

try_file = open('HOA_aut.txt', 'w')
if try_file:
    try_file.close()

# f = open("../generate/output/filtered_mutants_LTL.txt", "r")
f = open("patterns40_spin.txt", "r")
lines = f.readlines()
# lines[:20]
elapsed_time_spot = []
elapsed_time_spin = []
for line in lines:

    try:
        spot_command = "ltl2tgba -B '" + spin_to_spot(line) + "'"
        spin_command = "spin -f '" + line + "' -a"


        # start_time = time.time()
        spin_automata_HOA = subprocess.run(spin_command, shell=True, capture_output=True, text=True, timeout=5)  # Timeout in seconds)
        # end_time = time.time()
        # elapsed_time_spin.append(end_time - start_time)

        # create the automatas
        # start_time = time.time()
        spot_automata_HOA = subprocess.run(spot_command, shell=True, capture_output=True, text=True)
        # end_time = time.time()
        # elapsed_time_spot.append(end_time - start_time)

        
        # print( "For formula: ", line, " time elapsed for spot: ", elapsed_time_spot, " time elapsed for spin: ", elapsed_time_spin) 

        # save and convert the spin automata from neverclaim to hoa 
        file_name_spin = "spin_never_claim.never"
        with open(file_name_spin, 'w') as file:
            file.write(spin_automata_HOA.stdout)
        spin_automata_HOA = spot.automaton(file_name_spin).to_str('hoa')


        file_Hoa_aut = "HOA_aut.txt"
        with open(file_Hoa_aut, 'a') as file:
            file.write(spot_automata_HOA.stdout)
            file.write(".\n")
            file.write(spin_automata_HOA)
            file.write("\n~\n")


        # delete the file 
        if os.path.exists("spin_never_claim.never"):
            os.remove("spin_never_claim.never")

    except subprocess.TimeoutExpired:
        print("Process took too long and was skipped for formula: ", line)  


