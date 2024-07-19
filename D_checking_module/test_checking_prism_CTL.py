import os
import re
import get_atomic_prop as get_ap
import sys 
import subprocess
import re

# import generate.generate_formula as gen
# import generate.generate_mutant as gen_mut

# cd D_checking_module
# python3 test_checking_prism.py

# File to run PRISM 

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(parent_dir)
sys.path.append(parent_dir)



# generate formulas with the atomic propositions. takes the formulas from the file in the generate folder
# gen.generate_LTL(get_ap.generate_ap("model.pm"), "../generate/output/formulas_LTL.txt")

# gen_mut.generate_mutants_LTL(get_ap.generate_ap("model.pm"), "formulas_LTL.txt","mutants_LTL.txt")


# read the original formula and the mutant formula.
# use PRISM to read the model.m and the formula translated with a ltl2automata tool = result original 
# use PRISM to read the model.m and the formula translated with a ltl2automata tool = result mutant
# compare result original = result mutant? 
 

def find_cell_with_keyword(array, keyword):
    for i, cell in enumerate(array):
        if keyword in cell:
            return cell
    return None

keyword = "\n\nResult:"

# read file 
file_in = open('../generate/output/filtered_mutants_CTL.txt', 'r') #read formula and relative mutants
Lines = file_in.readlines()
result_boolean = None
n_formulas = 0
n_mutants = 0
for line in Lines:
    n_formulas += 1
    array_formula = line.split(' ')[:-1] #last element is \n
    array_formula = [x for x in array_formula if x] #remove empty elements ''
    original_formula = array_formula[0]
    # replace a with "a", b with "b", etc.
    original_formula = original_formula.replace("a", "\"a\"")
    original_formula = original_formula.replace("b", "\"b\"")

    print( original_formula)
    mutants = array_formula[1:]
    command = f'./prism files/model.pm -pf "E [ s=0 ]" -ltl2datool hoa-ltl2dstar-with-ltl2ba-for-prism -ltl2dasyntax lbt'
    result_ba = subprocess.run(command, shell=True,capture_output=True, text=True)
    # print(result_ba)
    result_ba = re.findall(r'Result:\s*(\w+)\n\n', result_ba.stdout)
    print("original ", original_formula, result_ba)
    
    for mutant in mutants:
        n_mutants += 1
        command = f'./prism model.pm -pf "E [ s=0 ]" -ltl2datool hoa-ltl2dstar-with-ltl2tgba-for-prism -ltl2dasyntax lbt'
        result_tgba = subprocess.run(command, shell=True,capture_output=True, text=True)
        result_tgba = re.findall(r'Result:\s*(\w+)\n\n', result_tgba.stdout)
        print("mutant ", mutant, result_tgba)

        if result_ba != result_tgba:
            print("Original formula: ", original_formula)
            print("Mutant formula: ", mutant)
            print("Original: ", result_ba)
            print("Mutant: ", result_tgba)
            error = True
        print()
        # index, result_cell = find_cell_with_keyword(result_tgba, keyword)




    # command = f'./prism model.pm -pf "E [ {formula} ]" -ltl2datool hoa-ltl2dstar-with-ltl2ba-for-prism -ltl2dasyntax lbt'
    # result = subprocess.run(command, shell=True,capture_output=True, text=True)
    # if result.stdout.find("Result: true") != -1:
    #     result_boolean = True
    # elif result.stdout.find("Result: false") != -1:
    #     result_boolean = False
    # print(result_boolean)

    

    # for mutant in mutants:
    #     command = f'./prism model.pm -pf "A [ {formula} ]" -ltl2datool hoa-ltl2dstar-with-ltl2ba-for-prism -ltl2dasyntax lbt'
    #     result = subprocess.run(command, shell=True,capture_output=True, text=True)
    #     print(result)
    # run PRISM
    # command = f'./prism model.pm -pf "A [ {original_formula} ]" -ltl2datool hoa-ltl2dstar-with-ltl2ba-for-prism -ltl2dasyntax lbt'
if error == False:
    print("Checked ", n_formulas, "formulas and ", n_mutants, " mutants, their LTL satisfiability is consistent.")



# subprocess.run(command, shell=True)




 

