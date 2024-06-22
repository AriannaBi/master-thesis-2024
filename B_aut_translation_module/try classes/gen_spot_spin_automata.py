import spot
import os
import subprocess


# TEST CLASS for checking if the the commands are working. do not include in the thesis.

# maybe this is for the trqnslation formula, since i am testing the ltl to automata translation function to see if it produces 
# equivalent results. 


# give two equivalent formulas
spot_command = "ltl2tgba -f 'G(a U Fb)'"
spin_command = "spin -f '[] (a U <> b)' -a"

spot_command = "ltl2tgba -B '((X(b))&(X(a)))&((X(c))&(X(a)))'"
spin_command = "spin -f '((X(b))&&(X(a)))&&((X(c))&&(X(a)))' -a"


# create the automatas
spot_automata_HOA = subprocess.run(spot_command, shell=True, capture_output=True, text=True)
spin_automata_NEVER = subprocess.run(spin_command, shell=True, capture_output=True, text=True)

# save never claim automata in a file
file_name = "spin_never_claim.never"
with open(file_name, 'w') as file:
    file.write(spin_automata_NEVER.stdout)

# convert the neverclaim automata to HOA format
spin_automata_HOA = spot.automaton(file_name).to_str('hoa')
if os.path.exists(file_name):
    os.remove(file_name)
# save spin hoa automata in a file
with open("spin_automata.hoa", 'w') as file:
    file.write(spin_automata_HOA)


# save spot hoa automata in a file
with open("spot_automata.hoa", 'w') as file:
    file.write(spot_automata_HOA.stdout)