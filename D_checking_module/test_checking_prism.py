import os
import re
import get_atomic_prop as get_ap
import sys 
import subprocess

import generate.generate_formula as gen
import generate.generate_mutant as gen_mut

# cd D_checking_module
# python3 test_checking_prism.py

# File to run PRISM 

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(parent_dir)
sys.path.append(parent_dir)



# generate formulas with the atomic propositions. takes the formulas from the file in the generate folder
gen.generate_LTL(get_ap.generate_ap("model.pm"), "../generate/output/formulas_LTL.txt")

gen_mut.generate_mutants_LTL(get_ap.generate_ap("model.pm"), "formulas_LTL.txt","mutants_LTL.txt")


# read the original formula and the mutant formula.
# use PRISM to read the model.m and the formula translated with a ltl2automata tool = result original 
# use PRISM to read the model.m and the formula translated with a ltl2automata tool = result mutant
# compare result original = result mutant? 
 

formula = "G s=0"
# read file 
file_in = open('filtered_mutants_LTL.txt', 'r') #read formula and relative mutants
lines = file_in.readlines()
result_boolean = None
for line in lines:
    array_formula = line.split(' ')[:-1] #last element is \n
    array_formula = [x for x in array_formula if x] #remove empty elements ''
    original_formula = array_formula[0]
    mutants = array_formula[1:]
    print(original_formula)
    command = f'./prism model.pm -pf "E [ {formula} ]" -ltl2datool hoa-ltl2dstar-with-ltl2ba-for-prism -ltl2dasyntax lbt'
    result = subprocess.run(command, shell=True,capture_output=True, text=True)
    if result.stdout.find("Result: true") != -1:
        result_boolean = True
    elif result.stdout.find("Result: false") != -1:
        result_boolean = False
    print(result_boolean)

    

    # for mutant in mutants:
    #     command = f'./prism model.pm -pf "A [ {formula} ]" -ltl2datool hoa-ltl2dstar-with-ltl2ba-for-prism -ltl2dasyntax lbt'
    #     result = subprocess.run(command, shell=True,capture_output=True, text=True)
    #     print(result)
    # run PRISM
    # command = f'./prism model.pm -pf "A [ {original_formula} ]" -ltl2datool hoa-ltl2dstar-with-ltl2ba-for-prism -ltl2dasyntax lbt'



# subprocess.run(command, shell=True)




 

