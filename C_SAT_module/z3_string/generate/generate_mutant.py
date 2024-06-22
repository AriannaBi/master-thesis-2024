import maude
import os.path
import numpy as np
import os
import pandas as pd
import csv
import sys

# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# print(parent_dir)
# sys.path.append(parent_dir)

# possible inputs:
# python3 generate_mutant.py -LTL
# python3 generate_mutant.py -CTL
# python3 generate_mutant.py

########### add lines for atomic propositions in the maude files######################################
def read_file(file_path):
    """Read the content of the file into a list of lines."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def write_file(file_path, lines):
    """Write a list of lines to the file."""
    with open(file_path, 'w') as file:
        file.writelines(lines)



# Filter the formulas in the LTL and CTL files
# def filter_formulas(name_file):
#     # LTL filter formulas 
#     # delete lines with no mutants
#     # split text into columns. Each columsn contains a formula
#     name_file_filtered = name_file.replace('mutants', 'filtered_mutants') #now instead of mutants.txt is filtered_mutants.txt
#     df = pd.read_csv(f'{name_file}', names=['text'])
#     split_columns = df['text'].str.split(' ', expand=True)
#     df_concatenated = pd.concat([df, split_columns], axis=1)
#     df_concatenated.drop(columns=['text'], inplace=True) # drop text column


#     # formulas with LTL equivalences
#     df_filter = df_concatenated[df_concatenated[1] != '']
#     print(name_file_filtered.split('/')[-1],  ": Number of formulas with mutants: {}/{}".format(len(df_filter),len(df_concatenated)))
#     df_filter = df_filter.reset_index(drop=True)
#     df_filter.to_csv(f'{name_file_filtered}', index=False,   header=False, sep=' ', quoting=csv.QUOTE_NONE,  escapechar='\\')
#     # print(f'Generated file {name_file_filtered}')
#     # name is output/filtered_mutants_CTL'
#     # while in the main function is output/mutants_CTL



# generate mutants of LTL
def generate_mutants_LTL(ap, file_name_input, file_name_output):

    maude.init(advise=True)
    maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_mutant_LTL.maude'))
    m = maude.getCurrentModule()



    file_in = open(file_name_input, 'r') #read formula
    # file_out formatted as formula .. mutant .. mutant .. mutant 
    file_out = open(file_name_output, 'a') #write formula and append mutants
    Lines = file_in.readlines()

    n_formula = 0
    n_mutant=0
    for line in Lines:
        n_formula += 1
        t = m.parseTerm(line)
        # put 3 spaces to separate formula and mutants
        file_out.write(str(t) + '   ' + "" )
        pattern = m.parseTerm('M')

        
        for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=1):
            # if M is not in the solution, print it
            if (str(sol).find('M') == -1) and str(sol) != str(t):
            # if (str(sol).find('M') == -1) and str(sol) != str(t): #exclude the formula itself from the mutants
                n_mutant += 1
                # put 3 spaces to separate mutants
                file_out.write(str(sol) +  '   ' + "")
        file_out.write('\n')

    print("LTL: Generated file output/mutants_LTL.txt with the mutants of the formulas. \n \t Number original formulas: {} \n \t Number of mutants: {}".format(n_formula, n_mutant))

    file_in.close()
    file_out.close()

    # filter_formulas(file_name_output)


def clean_file(name_file):
        try_file = open(name_file, 'w')
        if try_file:
            try_file.close()



if __name__ == "__main__":


    clean_file('output/mutants_LTL.txt')

    generate_mutants_LTL([], 'output/formulas_LTL.txt', 'output/mutants_LTL.txt')

    