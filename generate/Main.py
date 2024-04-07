import spot
import os

# Pipeline: generate_formula -> generate_mutant (filter mutants) -> check_if_equivalent
os.system("python3 generate_formula.py")
# else: os.system("python3 generate_formula.py -LTL")
# else: os.system("python3 generate_formula.py -CTL")

os.system("python3 generate_mutant.py")
os.system("python3 check_if_equivalent.py")
