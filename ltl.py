from pysat.solvers import Minisat22
from pysat.formula import CNF

def are_equivalent_sat(formula1, formula2):
    # Convert both LTL formulas to CNF
    cnf_formula1 = convert_to_cnf(formula1)
    cnf_formula2 = convert_to_cnf(formula2)

    # Combine the CNF formulas
    combined_cnf = CNF(from_clauses=cnf_formula1.clauses + cnf_formula2.clauses)

    # Use a SAT solver to check satisfiability
    solver = Minisat22()
    solver.append_formula(combined_cnf)
    if solver.solve():
        return True  # Both formulas are satisfiable, indicating equivalence
    else:
        return False  # The combined formula is unsatisfiable, indicating non-equivalence

# Example LTL formulas
formula1 = "G(a -> Xb)"
formula2 = "G(!a | Xb)"

# Test equivalence using SAT solver
equivalent = are_equivalent_sat(formula1, formula2)
if equivalent:
    print("The formulas are equivalent.")
else:
    print("The formulas are not equivalent.")
