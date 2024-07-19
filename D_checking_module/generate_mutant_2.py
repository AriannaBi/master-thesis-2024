import maude
import os.path
import numpy as np
import os
import pandas as pd
import csv
import sys
import re
import random
import subprocess




if __name__ == "__main__":



    # read file and run prism  ------------------------------------------------------------------------------------------------------------------------
    file_in = open('output/filtered_mutants_CTL.txt', 'r') #read formula and relative mutants
    Lines = file_in.readlines()
    result_boolean = None
    n_formulas = 0
    n_mutants = 0
    for line in Lines:
        n_formulas += 1
        array_formula = line.split(' ')[:-1] #last element is \n
        array_formula = [x for x in array_formula if x] #remove empty elements ''

        # Formula with ltl2ba
        original_formula = array_formula[0]
        command_or = [
        './prism',
        'prism-examples/mdps/csma/csma2_2.nm',
        # '-pf', f'E [{elem}]',
        '-pf', f'{original_formula}']
        # '-ltl2datool', 'hoa-ltl2dstar-with-ltl2ba-for-prism',
        # '-ltl2dasyntax', 'lbt']   
        result_ba = subprocess.run(command_or, capture_output=True, text=True)
        print(result_ba)
        result_ba = re.findall(r'Result:\s*(\w+)\n\n', result_ba.stdout)
        print("original ", original_formula, result_ba)


        for elem in array_formula[1:]:
            elem.strip(' ')
            # Formula with rabinazer3
            command_mu = [
                './prism',
                'prism-examples/mdps/csma/csma2_2.nm',
                # '-pf', f'E [{elem}]',
                '-pf', f'{elem}']
                # '-ltl2datool', 'hoa-rabinizer3-dgra-for-prism',
                # '-ltl2dasyntax', 'lbt']  
            result_mu = subprocess.run(command_mu, capture_output=True, text=True)
            print(result_mu)
            result_mu = re.findall(r'Result:\s*(\w+)\n\n', result_mu.stdout)
            print("mutant ", elem, result_mu)

        print('---\n\n')
    
        if result_ba != result_mu:
            print("Error: Original formula: ", elem, "result 1 trans", result_ba, "result trans", result_mu)
            error = True
        
        # './prism files/model.pm -pf "E [ (X(F(c)))&(X(F(c))) ]" -ltl2datool hoa-ltl2dstar-with-ltl2ba-for-prism -ltl2dasyntax lbt'
            print()
        print()
