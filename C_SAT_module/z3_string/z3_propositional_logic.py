# check if two expressions are equivalent, by checking if the negation of their equivalence is unsatisfiable. 
# for example !(f <=> g) is UNSAT then f and g are equivalent

from z3 import *
import os
import sys

    
def are_equivalent(expr1, expr2):
    a = Bool('a')
    b = Bool('b')
    c = Bool('c')
    # Create a solver instance
    solver = Solver()
    
    # Add the negation of the equivalence to the solver
    solver.add(expr1 != expr2)
    
    # Check satisfiability of the negation of the equivalence
    if solver.check() == unsat:
        return True
    else:
        return False



a = Bool('a')
b = Bool('b')
c = Bool('c')

# Create a dictionary for variable resolution
variables = {
    'a': a,
    'b': b,
    'c': c,
    'And': And,
    'Or': Or,
    'Not': Not,
    'Implies': Implies,
    'Xor': Xor,
    'If': If
}

# (from versions: 4.4.2.1, 4.4.2.1.post1, 4.5.1.0, 4.5.1.0.post1, 4.5.1.0.post2, 4.8.0.0.post1, 4.8.5.0, 4.8.6.0, 4.8.7.0, 4.8.8.0, 4.8.9.0, 4.8.10.0, 4.8.11.0, 4.8.12.0, 4.8.13.0, 4.8.14.0, 4.8.15.0, 4.8.16.0, 4.8.17.0, 4.9.0.0, 4.9.1.0, 4.10.0.0, 4.10.1.0, 4.10.2.0, 4.11.0.0, 4.11.1.0, 4.11.2.0, 4.12.0.0, 4.12.1.0, 4.12.2.0, 4.12.3.0, 4.12.4.0, 4.12.5.0, 4.12.6.0, 4.13.0.0)

file_in = open('generate/output/mutants_LTL.txt', 'r') #read formula and relative mutants
file_out_12 = open('generate/output/z3_4_12.txt', 'w') 
# file_out_8 = open('generate/output/z3_4_8.txt', 'w') 

Lines = file_in.readlines()
n_mutants = 0
n_formulas = 0
for line in Lines:
    n_formulas += 1
    array_formula = line.split('   ')[:-1] #last element is \n
    array_formula = [x for x in array_formula if x] #remove empty elements ''
    original_formula = array_formula[0]
    mutants = array_formula[1:]

    solver = Solver()
    expr1 = eval(original_formula, variables)
    solver.add(expr1)
    original_formula_sat = False
    if solver.check() == sat:
        original_formula_sat = True

    # write the sat value of the original formula in the file 
    file_out_12.write(str(original_formula_sat) + '\n')
    for mutant in mutants:
        n_mutants += 1
        solver.reset()
        solver = Solver()
        expr2 = eval(mutant, variables)
        solver.add(expr1)
        mutant_formula_sat = False
        if solver.check() == sat:
            mutant_formula_sat = True
        
        file_out_12.write(str(mutant_formula_sat) + '\n')

        if original_formula_sat != mutant_formula_sat:
            print("The original formula ", original_formula, " is ", original_formula_sat, " and the mutant ", mutant, " is ", mutant_formula_sat)
        





        # # EQUIVALENCE original formula and mutant
        # if not are_equivalent(expr1, expr2):
        #     print("The expressions are NOT equivalent: ", original_formula, " and ", mutant)
        # else:
        #     print("The expressions are equivalent: ", original_formula, " and ", mutant)
        
    


        # # SYNTACTICALLY EQUAL
        # if class of expr1 is bool then convert it to BoolVal
        # if type(expr1) == bool: #False value is bool instead of booref
        #     expr1 = BoolVal(expr1)
        # if type(expr2) == bool:
        #     expr2 = BoolVal(expr2)

        # simplify_expr1 = simplify(expr1)
        # simplify_expr2 = simplify(expr2)
        # print("The expressions simplified ", simplify_expr1, " and ", simplify_expr2)
        # if not (simplify_expr1 == simplify_expr2):
        #     print("The expressions are NOT syntactically equal after simplification: ", original_formula, " and ", mutant)

