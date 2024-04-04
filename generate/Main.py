import spot
import os


os.system("python3 generate_formula.py")
os.system("python3 generate_mutant.py")
os.system("python3 check_if_equivalent.py")
