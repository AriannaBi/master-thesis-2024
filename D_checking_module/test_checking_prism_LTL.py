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
file_in = open('output/filtered_mutants_LTL.txt', 'r') #read formula and relative mutants
Lines = file_in.readlines()
result_boolean = None
n_formulas = 0
n_mutants = 0
for line in Lines:
    n_formulas += 1
    array_formula = line.split(' ')[:-1] #last element is \n
    array_formula = [x for x in array_formula if x] #remove empty elements ''
    original_formula = array_formula[0]
    original_formula = original_formula.replace("a", "\"a\"")
    original_formula = original_formula.replace("b", "\"b\"")
    original_formula = original_formula.replace("c", "\"c\"")
    # print(original_formula)
    mutants = array_formula[1:]
    print("start")
    # Formula with ltl2ba
    command_or = [
    './prism',
    'files/model.pm',
    '-pf', f'E [{original_formula}]',
    '-ltl2datool', 'hoa-ltl2dstar-with-ltl2ba-for-prism',
    '-ltl2dasyntax', 'lbt']   
    result_ba = subprocess.run(command_or, capture_output=True, text=True)
    # print("original \n", result_ba)
    result_ba = re.findall(r'Result:\s*(\w+)\n\n', result_ba.stdout)
    print("original ", original_formula, result_ba)

    # Formula with rabinazer3
    command_mu = [
        './prism',
        'files/model.pm',
        '-pf', f'E [{mutants}]',
        '-ltl2datool', 'hoa-rabinizer3-dgra-for-prism',
        '-ltl2dasyntax', 'lbt']  
     
    result_mu = subprocess.run(command_mu, capture_output=True, text=True)
    # print("mutant \n", mutant,result_mu)
    result_mu = re.findall(r'Result:\s*(\w+)\n\n', result_mu.stdout)
    print("mutant ", mutants, result_mu)
    

    if result_ba != result_mu:
        print("Error: Original formula: ", original_formula, "mutant",mutant, "result original", result_ba, "result mutant", result_mu)
        error = True
    
    # './prism files/model.pm -pf "E [ (X(F(c)))&(X(F(c))) ]" -ltl2datool hoa-ltl2dstar-with-ltl2ba-for-prism -ltl2dasyntax lbt'
    for mutant in mutants:
        n_mutants += 1
        mutant = mutant.replace("a", "\"a\"")
        mutant = mutant.replace("b", "\"b\"")
        mutant = mutant.replace("c", "\"c\"")
        command_mu = [
        './prism',
        'files/model.pm',
        '-pf', f'E [{mutant}]',
        '-ltl2datool', 'hoa-rabinizer3-dgra-for-prism',
        '-ltl2dasyntax', 'lbt']   
        result_mu = subprocess.run(command_mu, capture_output=True, text=True)
        # print("mutant \n", mutant,result_mu)
        result_mu = re.findall(r'Result:\s*(\w+)\n\n', result_mu.stdout)
        print("mutant ", mutant, result_mu)
        if result_ba != result_mu:
            print("Error: Original formula: ", original_formula, "mutant",mutant, "result original", result_ba, "result mutant", result_mu)
        error = True
        print()
    print()



    
        # print()
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




 

