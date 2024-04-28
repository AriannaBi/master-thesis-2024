# Description: Check if two formulas are equivalent
# Implemented using spot library and spot function are_equivalent
# Requirements: spot library 
# Usage: python3 check_if_equivalent.py
# I am using it with conda3 environment with spot library installed


import spot
import pandas as pd
import csv
# Program to check if LTL formulas are equivalent or not, after the semplification.
# The program reads the file spot_all_options.txt and checks if the original formula and the mutants are equivalent.
# If they are not equivalent, the program prints the formula and the mutant.
# The program also prints the number of formulas and mutants checked.
 
# run_semplif.cc -> check_equivalences.py





# file_in = open('output/spot_all_options.txt', 'r') #read formula and relative mutants
# Lines = file_in.readlines()

# n_mutants = 0
# n_formulas = 0
# const = False

# for idx, line in enumerate(Lines):
#     n_formulas += 1
#     array_formula = line.split("   ") #last element is \n
#     array_formula = array_formula[1:]
#     array_formula = [x.strip("\n") for x in array_formula] #remove empty elements ''
#     original_formula = array_formula[0]
#     mutants = array_formula[1:]

#     const = False
#     for mutant in mutants:
#         n_mutants += 1
#         are_eq = spot.are_equivalent(original_formula, mutant)
#         if are_eq == False:
#             print(are_eq, original_formula, mutant)
#         if original_formula != mutant:
#             const = True
#             print(idx + 1, end=' ')
#             # print(original_formula)
#             # print(mutant)
#     if const == True:
#       print('\n')
# print("Checked ", n_formulas, "formulas and ", n_mutants, " mutants")






# remove lines in which all the formulas are the same syntactically 
# Filter files 
def filter_lines(name_file):
    
 
    # delete lines with no mutants
    # split text into columns. Each columsn contains a formula
    df = pd.read_csv(name_file, names=['text'])
    split_columns = df['text'].str.split('   ', expand=True)
    df_concatenated = pd.concat([df, split_columns], axis=1)
    
    df_concatenated.drop(columns=['text'], inplace=True) # drop text column
    array_df_to_drop = []

    # print(df_concatenated)
    # Check if all values in each row are equal (excluding None values)
    # equal_values_mask = df_concatenated.apply(lambda row: len(set(row.dropna())) == 1, axis=1)
    # for each row, print the element
    df_concatenated_copy = df_concatenated.copy()
    for index, row in df_concatenated_copy.iterrows():
        # print(row)
        row_array = row.values
        filtered_list = list(filter(lambda x: x is not None, row_array))
        filtered_list = filtered_list[1:]
        for elem in filtered_list:

            if elem != filtered_list[0]:

                array_df_to_drop.append(index)
                break

    # print(len(df_concatenated))
    df_concatenated_copy = df_concatenated[df_concatenated.index.isin(array_df_to_drop)].copy()
    # print(len(df_concatenated))    
    print(df_concatenated_copy)
    df_concatenated_copy.to_csv('output/filtered_spot_all_options.txt', index=False,   header=False, sep='/', quoting=csv.QUOTE_NONE,escapechar=' ')


filter_lines("output/spot_all_options.txt")