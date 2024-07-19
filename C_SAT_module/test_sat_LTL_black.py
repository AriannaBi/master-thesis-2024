import spot
import sys
import subprocess

# CHECK THE SATISFIABILITY OF A LTL FORMULA, by checking if the satisfiability of the formula.
# If the automaton is empty it is unsat, else it is sat. 

def spot_to_spin(formula):
    formula = formula.replace('G', '[]')
    formula = formula.replace('F', '<>')
    formula = formula.replace('|', '||')
    formula = formula.replace('&', '&&')
    return formula

def check_satisfiability_spot(formula_str):
    # Parse the LTL formula
    formula = spot.formula(formula_str)
    
    # Print the formula
    # print(f"Checking satisfiability for formula: {formula}")

    # Translate the formula to a Buchi automaton
    aut = spot.translate(formula, "det")

    # Print the automaton. IT IS A BUCHI Automaton
    # print(f"Buchi automaton: {aut}")

    # Check if the automaton is empty
    is_satisfiable = not aut.is_empty()

    if is_satisfiable:
        return 0
    else:
        return 1




def read_formulas_compute_sat(read_file):
    error = False
    file_in = open(read_file, 'r') #read formula and relative mutants
    Lines = file_in.readlines()
    n_mutants = 0
    n_formulas = 0

    for line in Lines:
        n_formulas += 1
        array_formula = line.split(' ')[:-1] #last element is \n
        array_formula = [x for x in array_formula if x] #remove empty elements ''
        original_formula = array_formula[0]
        mutants = array_formula[1:]
        for mutant in mutants:
            n_mutants += 1
            ff = f'"{original_formula}"'
            command = f"black solve -f {ff}"
            is_sat_original = subprocess.run(command, shell=True, capture_output=True, text=True)
            # print("Original ", is_sat_original.stdout)

            gg = f'"{mutant}"'
            command = f"black solve -f {gg}"
            is_sat_mutant = subprocess.run(command, shell=True, capture_output=True, text=True)
            # print("Mutant ", is_sat_mutant.stdout)

            # print("Number of formulas: ", n_formulas, "Number of mutants: ", n_mutants)
            # print("Original ", is_sat_original.stdout, " end")
            # print("Mutant ", is_sat_mutant.stdout, " end")
            if (is_sat_original.stdout != is_sat_mutant.stdout):
                print("Original formula: ", original_formula)
                print("Mutant formula: ", mutant)
                # print("Original: ", is_sat_original.stdout)
                # print("Mutant: ", is_sat_mutant.stdout)
                # error = True
            # if "error" in is_sat_original.stdout or "error" in is_sat_mutant.stdout:
            #     print("Error: ", is_sat_original.stdout)
            #     error = True
            # elif "is satisfable" in is_sat_original.stdout and "is NOT satisfable" in is_sat_mutant.stdout:
            #     print("The original formula is sat ", f,"and the mutant is unsat", g, ".")
            #     error = True
            # elif "is NOT satisfable" in is_sat_original.stdout and "is satisfable" in is_sat_mutant.stdout:
            #     print("The original formula is unsat ", f,"and the mutant is sat", g, ".")
            #     error = True


            # if is_sat_original != is_sat_mutant:
            #     print(mutant)
            #     print(original_formula)
            #     print(is_sat_original)
            #     print(is_sat_mutant)
            #     error = True

    # if error == False:
    #     print("Checked ", n_formulas, "formulas and ", n_mutants, " mutants, their LTL satisfiability is consistent.")

if __name__ == "__main__":
    # check_satisfiability("Ga")
    read_formulas_compute_sat('../generate/output/filtered_mutants_LTL.txt')
