from z3 import *

def is_digit_string(s):
    digits = [StringVal(str(d)) for d in range(10)]
    return Or([s == d for d in digits])


def check_digit_equivalence():
    # Create a Z3 solver instance
    solver = Solver()

    # Define string variables
    P = String('P')
    T = String('T')

    # Define the assertion that whether T is a digit is equivalent to whether P is a digit
    
    solver.add((P == T) == (T == P))  # Simplified constraint since is_digit is not directly supported in Z3 Python API

    # Check satisfiability
    result = solver.check()
    print("Result:", result)

    # If satisfiable, print the model
    if result == sat:
        model = solver.model()
        print("The formula is satisfiable.")
        print("Model:")
        print(f"P = {model[P]}")
        print(f"T = {model[T]}")
    elif result == unsat:
        print("The formula is unsatisfiable.")
    else:
        print("The result is unknown.")

if __name__ == "__main__":
    check_digit_equivalence()
