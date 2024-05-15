import maude
import os.path
import numpy as np
import os
import pandas as pd
import csv
import sys
import re


# python3 check_if_equivalent.py

maude.init(advise=True)
maude.load(os.path.join(os.path.dirname(__file__), 'maude/check_semplification.maude'))
m = maude.getCurrentModule()




 
# give me all the subformulas
t = m.parseTerm("!(X (s U (s U t)))")
t = m.parseTerm("F(G(F(G(s))))")
pattern = m.parseTerm("N")


def print_rules(path):
    reg = re.findall(r'\[([^]]+)\]', ''.join(str(path) for path in path))
    if len(reg) > 0: 
        return reg
    

# for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=20):
#     print(sol, print_rules(path()))




new_path = []
def explore_solutions(t, pattern, path):
    has_solution = False
    for asol, asubs, apath, anrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=1):
        if len(apath()) > 1:
            new_path = path + apath()
            print("sol:", asol, print_rules(new_path))
            explore_solutions(asol, pattern, new_path)
            has_solution = True  # At least one solution found
    # Check if it is a leaf (no more solutions)
    if not has_solution:
        print("Reached leaf with path:", t, print_rules(path))

    print('\n')
    



# Call the function to explore solutions
print('\n EPLORE SOLUTIONS: ------------------------- \n')

explore_solutions(t, pattern, path = [])