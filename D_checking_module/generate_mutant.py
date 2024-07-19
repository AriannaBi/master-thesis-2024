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

def insert_line_at_position(file_path, new_line, position):
    """Insert a new line at the specified position in the file."""
    # Read the file content
    lines = read_file(file_path)
    lines.pop(2)
    # Insert the new line at the specified position
    lines.insert(position, new_line + '\n')

    # Write the modified content back to the file
    write_file(file_path, lines)

def modify_maude_file_with_ap(ap):
    file_path_LTL = os.path.abspath(os.path.join(os.path.dirname(__file__), 'maude', 'generate_mutant_LTL.maude'))
    file_path_CTL = os.path.abspath(os.path.join(os.path.dirname(__file__), 'maude', 'generate_mutant_CTL.maude'))
    
    atomic_prop_string = ' '.join(ap)
    
    new_line = '   ops ' + str(atomic_prop_string) + ' : -> Formula .'
    print(file_path_LTL, new_line)
    position = 2  # Insert after the second line (0-based index)
    insert_line_at_position(file_path_LTL, new_line, position)
    insert_line_at_position(file_path_CTL, new_line, position)
####################################################################################################

# Filter the formulas in the LTL and CTL files
def filter_formulas(name_file):
    # LTL filter formulas 
    # delete lines with no mutants
    # split text into columns. Each columsn contains a formula
    name_file_filtered = name_file.replace('mutants', 'filtered_mutants') #now instead of mutants.txt is filtered_mutants.txt
    df = pd.read_csv(f'{name_file}', names=['text'])
    split_columns = df['text'].str.split(' ', expand=True)
    df_concatenated = pd.concat([df, split_columns], axis=1)
    df_concatenated.drop(columns=['text'], inplace=True) # drop text column


    # formulas with LTL equivalences
    df_filter = df_concatenated[df_concatenated[1] != '']
    print(name_file_filtered.split('/')[-1],  ": Number of formulas with mutants: {}/{}".format(len(df_filter),len(df_concatenated)))
    df_filter = df_filter.reset_index(drop=True)
    df_filter.to_csv(f'{name_file_filtered}', index=False,   header=False, sep=' ', quoting=csv.QUOTE_NONE,  escapechar='\\')
    # print(f'Generated file {name_file_filtered}')
    # name is output/filtered_mutants_CTL'
    # while in the main function is output/mutants_CTL

def fill_set_formulas(file_name_input):
    set_formulas = set()
    file_in = open(file_name_input, 'r') #read formula
    Lines = file_in.readlines()
    for line in Lines:
        line = line[:-1].strip() #remove \n and spaces
        set_formulas.add(line)
    file_in.close()
    return set_formulas

# generate mutants of LTL
def generate_mutants_LTL(ap, file_name_input, file_name_output):
    num_already_existing_mutants = 0
    # modify_maude_file_with_ap(ap)

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
        set_already_existing_formula = fill_set_formulas('output/formulas_LTL.txt')
        # put 3 spaces to separate formula and mutants
        file_out.write(str(t) + ' ' + "" )
        pattern = m.parseTerm('M')

        
        for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=1):
            # if M is not in the solution, print it
            if (str(sol).find('M') == -1) and str(sol) != str(t):
            # if (str(sol).find('M') == -1) and str(sol) != str(t): #exclude the formula itself from the mutants
                clean_sol = str(sol).strip()
                # print(clean_sol)
                if clean_sol not in set_already_existing_formula:
                    n_mutant += 1
                    # put 3 spaces to separate mutants
                    file_out.write(str(sol) +  ' ' + "")
                else:
                    num_already_existing_mutants+=1
                set_already_existing_formula.add(clean_sol)

        file_out.write('\n')

    print("LTL: Generated file output/mutants_LTL.txt with the mutants of the formulas. \n \t Number original formulas: {} \n \t Number of mutants: {} \n \t Number of duplicates: {}".format(n_formula, n_mutant, num_already_existing_mutants))

    file_in.close()
    file_out.close()

    filter_formulas(file_name_output)




# generate mutants of CTL
def generate_mutants_CTL(ap, file_name_input, file_name_output):
    num_already_existing_mutants = 0
    # modify_maude_file_with_ap(ap)
    # print('\n')
    maude.init(advise=True)
    maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_mutant_CTL.maude'))
    m = maude.getCurrentModule()
    # print('Using', m, 'module')



    # Using readlines()
    file_in = open(file_name_input, 'r') #read formula
    # file_out formatted as formula .. mutant .. mutant .. mutant 
    file_out = open(file_name_output, 'a') #write formula and append mutants
    lines = file_in.readlines()

    n_formula = 0
    n_mutant=0
    for line in lines:
        n_formula += 1
        t = m.parseTerm(line)
        set_already_existing_formula = fill_set_formulas('output/formulas_CTL.txt')
        # put 3 spaces to separate formula and mutants
        file_out.write(str(t) + ' ' + "" )
        pattern = m.parseTerm('M')

        for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=1):

            # if mutant is without M and if original is different from mutant
            if (str(sol).find('M') == -1) and str(sol) != str(t):
                clean_sol = str(sol).strip()
                # if mutant contains A or E 
                # if str(sol).find('A') != 1 or str(sol).find('E') != 1:
                if clean_sol not in set_already_existing_formula:
                    n_mutant += 1
                    # put 3 spaces to separate mutants
                    file_out.write(str(sol) +  ' ' + "")
                else:
                    num_already_existing_mutants+=1
                set_already_existing_formula.add(clean_sol)
        file_out.write('\n')

    print("CTL: Generated file output/mutants_CTL.txt with the mutants of the formulas. \n \t Number original formulas: ", n_formula, "\n \t Number of mutants: ", n_mutant, "\n \t Number of duplicates: ", num_already_existing_mutants)

    file_in.close()
    file_out.close()


    filter_formulas(file_name_output)



def main(ap):
    # This is taken from input std when generating the formulas.
    # ap = [a,b,c]
    # print(ab)
    file_name_input_LTL = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', 'formulas_LTL.txt'))
    file_name_input_CTL = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', 'formulas_CTL.txt'))

    file_name_output_LTL = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', 'mutants_LTL.txt'))
    file_name_output_CTL = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', 'mutants_CTL.txt'))
        
    generate_mutants_LTL(ap,file_name_input_LTL, file_name_output_LTL)
    print('\n')
    generate_mutants_CTL(ap,file_name_input_CTL, file_name_output_CTL)
    




def clean_file(name_file):
        try_file = open(name_file, 'w')
        if try_file:
            try_file.close()


def add_random_ap_based_on_model(model_name):
    ap = []
    label = []
    # type_prism = ["int", "bool", "enum"]
    with open(model_name, 'r', encoding='ISO-8859-1') as file:
        lines = file.readlines()
        for line in lines:
            # Find ap
            line_ap = re.findall(r'\S+\s*:\s*\[\d+\.\.\d+\]', line) #find atomic propositions s.a. s : [0..4];
            if len(line_ap) > 0:
                ap_tmp = line_ap[0].split(":")
                ap_name = ap_tmp[0].strip(' ')
                ap_value = ap_tmp[1].strip(' ').strip(';').strip('[').strip(']')
                ap_tmp = ap_name + "=" + ap_value
                
                ap.append(ap_tmp)
            
            
            # Find labels
            line_label = re.findall(r'label\s*"\S*"\s*=', line) #find labels s.a. label "A" = a;
            if len(line_label) > 0:
                line_label = re.findall(r'"\S*"', line_label[0])
                label.append(line_label[0])

    generated_ap = []
    prova_1 = 0
    prova_2 = 0
    for elem in ap:
        print("elem", elem)
        elem = elem.split("=")
        range = elem[1].split("..")

        name = elem[0]
        print("name", name)
        min_val = int(range[0])
        max_val = int(range[1])
        prova_1 = min_val
        prova_2 = max_val
        while prova_1 <= prova_2:
            generated_ap.append(name + "=" + str(prova_1))
            prova_1 += 1

    print("list", generated_ap)
    return generated_ap

if __name__ == "__main__":

    # Change this because it is going to be a pipeline and the ap are taken from the previous step of generating the formulas
    clean_file('output/mutants_LTL.txt')
    clean_file('output/mutants_CTL.txt')
    clean_file('output/filtered_mutants_LTL.txt')
    ap = []
    

    # add_random_ap_based_on_model('files/model.pm')
    # main(ap)
    file_name_input_LTL = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', 'formulas_LTL.txt'))
    file_name_input_CTL = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', 'formulas_CTL.txt'))

    file_name_input_LTL_ap = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', 'formulas_LTL_ap.txt'))
    file_name_input_CTL_ap = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', 'formulas_CTL_ap.txt'))

    file_name_output_LTL = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', 'mutants_LTL.txt'))
    file_name_output_CTL = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', 'mutants_CTL.txt'))
        
    # before generating mutants, modify the formula ltl in the file of formula with random atomic propositions from model
    list_ap = add_random_ap_based_on_model('prism-examples/mdps/csma/csma2_2.nm')
    # print(list_ap)
    modify_maude_file_with_ap(list_ap)
# /Users/ariannabianchi/Desktop/Formula-generator/D_checking_module/

# Modify file LTL formulas file 
    modified_lines = []
    with open(file_name_input_LTL, 'r') as f:
        content = f.readlines()
        # modified_lines = [line.replace('.',random.choice(list_ap) ) for line in content]
        modified_lines = []
        for line in content:
            new_line = ''
            for char in line:
                if char == '.':
                    new_line += random.choice(list_ap)
                else:
                    new_line += char
            modified_lines.append(new_line)

    with open(file_name_input_LTL_ap, 'w') as file:
        file.writelines(modified_lines)

# Modify file CTL formulas file 
    with open(file_name_input_CTL, 'r') as f:
        content = f.readlines()
        modified_lines = []
        for line in content:
            new_line = ''
            for char in line:
                if char == '.':
                    new_line += random.choice(list_ap)
                else:
                    new_line += char
            modified_lines.append(new_line)
    with open(file_name_input_CTL_ap, 'w') as file:
        file.writelines(modified_lines)



    generate_mutants_LTL(ap, file_name_input_LTL_ap, file_name_output_LTL)
    print('\n')
    generate_mutants_CTL(ap, file_name_input_CTL_ap, file_name_output_CTL)
    

    print("\n\n")
