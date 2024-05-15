import maude
import os.path
import numpy as np
import os
import pandas as pd
import csv
import sys

# python3 generate_mutant.py -LTL

LTL = False
CTL = False
if len(sys.argv) > 1:
    if sys.argv[1] == "-LTL":
        LTL = True
    elif sys.argv[1] == "-CTL":
        CTL = True


# deletecontent of file because we will append formulas and mutants from scratch
def clean_file(name_file):
    try_file = open(name_file, 'w')
    if try_file:
        try_file.close()

clean_file('output/mutants_LTL.txt')
clean_file('output/mutants_CTL.txt')
clean_file('output/filtered_mutants_LTL.txt')
clean_file('output/discarded_mutants_LTL.txt')




# Filter the formulas in the LTL and CTL files
def filter_formulas(name_file):
        # LTL filter formulas 
    # delete lines with no mutants
    # split text into columns. Each columsn contains a formula
    df = pd.read_csv(f'output/mutants_{name_file}.txt', names=['text'])
    split_columns = df['text'].str.split('   ', expand=True)
    df_concatenated = pd.concat([df, split_columns], axis=1)
    df_concatenated.drop(columns=['text'], inplace=True) # drop text column



    # discarded formulas because without LTL equivalences
    df_filter_discarded = df_concatenated[df_concatenated[1] == '']
    df_filter_discarded.to_csv(f'output/discarded_mutants_{name_file}.txt', index=False,   header=False, sep='.', quoting=csv.QUOTE_NONE)
    print(name_file, ": Number of discarded formulas because without mutants: {}/{}".format(len(df_filter_discarded), len(df_concatenated)))



    # formulas with LTL equivalences
    df_filter = df_concatenated[df_concatenated[1] != '']
    print(name_file,  ": Number of formulas with mutants: {}/{}".format(len(df_filter),len(df_concatenated)))
    df_filter = df_filter.reset_index(drop=True)
    df_filter.to_csv(f'output/filtered_mutants_{name_file}.txt', index=False,   header=False, sep='.', quoting=csv.QUOTE_NONE)

    



# generate mutants of LTL
def generate_mutants_LTL():

    maude.init(advise=True)
    maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_mutant_LTL.maude'))
    m = maude.getCurrentModule()



    file_in = open('output/formulas_LTL.txt', 'r') #read formula
    # file_out formatted as formula .. mutant .. mutant .. mutant 
    file_out = open('output/mutants_LTL.txt', 'a') #write formula and append mutants
    Lines = file_in.readlines()

    n_formula = 0
    n_mutant=0
    for line in Lines:
        n_formula += 1
        t = m.parseTerm(line)
        # put 3 spaces to separate formula and mutants
        file_out.write(str(t) + '   ' + "" )
        pattern = m.parseTerm('M')

        
        for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=2):
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

    filter_formulas('LTL')




# generate mutants of CTL
def generate_mutants_CTL():
    # print('\n')
    maude.init(advise=True)
    maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_mutant_CTL.maude'))
    m = maude.getCurrentModule()
    # print('Using', m, 'module')



    # Using readlines()
    file_in = open('output/formulas_CTL.txt', 'r') #read formula
    # file_out formatted as formula .. mutant .. mutant .. mutant 
    file_out = open('output/mutants_CTL.txt', 'a') #write formula and append mutants
    lines = file_in.readlines()

    n_formula = 0
    n_mutant=0
    for line in lines:
        n_formula += 1
        t = m.parseTerm(line)
        # put 3 spaces to separate formula and mutants
        file_out.write(str(t) + '   ' + "" )
        pattern = m.parseTerm('M')

        for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=1):

            # if mutant is without M and if original is different from mutant
            if (str(sol).find('M') == -1) and str(sol) != str(t):
                # if mutant contains A or E 
                if str(sol).find('A') != 1 or str(sol).find('E') != 1:
                    n_mutant += 1
                    # put 3 spaces to separate mutants
                    file_out.write(str(sol) +  '   ' + "")
        file_out.write('\n')

    print("CTL: Generated file output/mutants_CTL.txt with the mutants of the formulas. \n \t Number original formulas: ", n_formula, "\n \t Number of mutants: ", n_mutant)

    file_in.close()
    file_out.close()


    filter_formulas('CTL')





if LTL == True:
    generate_mutants_LTL()
    
elif CTL == True:
    generate_mutants_CTL()
    
else:
    generate_mutants_LTL()
    generate_mutants_CTL()
    