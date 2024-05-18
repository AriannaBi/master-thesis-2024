# Description: Check if two formulas are EQUAL and EQUIVALENT
# Implemented using spot library and spot function are_equivalent
# Requirements: spot library 
# Usage: python3 check_if_equivalent.py
# I am using it with conda3 environment with spot library installed


import spot
import pandas as pd
import csv
# Program to check if LTL formulas are EQUAL and EQUIVALENT or not, after the semplification.
# The program reads the file spot_all_options.txt and checks if the original formula and the mutants are EQUAL.
# If they are not EQUAL, the program prints the formula and the mutant.
# The program also prints the number of formulas and mutants checked.
 
# run_semplif.cc -> check_equivalences.py



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
    # for each row, print the element
    df_concatenated_copy = df_concatenated.copy()

    for index, row in df_concatenated_copy.iterrows():
        # print(row)
        row_array = row.values
        filtered_list = list(filter(lambda x: x is not None, row_array))
        filtered_list = filtered_list[1:]
        for elem in filtered_list:
            # If i want to check if thet are equivalent, use spot.are_equivalent.
            # Now I am checking that they are equal
            if elem != filtered_list[0]:

                array_df_to_drop.append(index)
                print("The two formulas are not equal [", elem, "] [", filtered_list[0], "]")
                break

    df_concatenated_copy = df_concatenated[df_concatenated.index.isin(array_df_to_drop)].copy()
    
    # remove white spaces in each formulas
    for col in df_concatenated_copy.columns:
        df_concatenated_copy[col] = df_concatenated_copy[col].map(lambda x: x.strip().replace(' ', '') if isinstance(x, str) else x)

    df_concatenated_copy.to_csv('output/not_equal_simplif_all_options.txt', index=False,   header=False, sep=' ', quoting=csv.QUOTE_NONE,escapechar=' ')
    if len(array_df_to_drop) == 0:
        print("All formulas are equal!")
    else:
        print("The non equal formulas are saved in output/not_equal_simplif_all_options.txt")

filter_lines("output/spot_all_options.txt")