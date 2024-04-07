import maude
import os.path
import numpy as np
import os
import pandas as pd
import csv

# deletecontent of file because we will append formulas and mutants from scratch
try_file = open('output/mutants_LTL.txt', 'w')
if try_file:
    try_file.close()

try_file = open('output/mutants_CTL.txt', 'w')
if try_file:
    try_file.close()

try_file = open('output.txt', 'w')
if try_file:
    try_file.close()




############################################## LTL ######################################################

maude.init(advise=True)
maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_mutant_LTL.maude'))
m = maude.getCurrentModule()
# print('Using', m, 'module')



file_in = open('output/formulas_LTL.txt', 'r') #read formula
# file_out formatted as formula .. mutant .. mutant .. mutant 
file_out = open('output/mutants_LTL.txt', 'a') #write formula and append mutants
Lines = file_in.readlines()

n_formula = 0
n_mutant=0
for line in Lines:
    n_formula += 1
    t = m.parseTerm(line)
    file_out.write(str(t) + ' ' + "" )
    pattern = m.parseTerm('M')

    
    for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=2):
        # if M is not in the solution, print it
        if (str(sol).find('M') == -1) and str(sol) != str(t):
        # if (str(sol).find('M') == -1) and str(sol) != str(t): #exclude the formula itself from the mutants
            n_mutant += 1
            file_out.write(str(sol) +  ' ' + "")
    file_out.write('\n')

print("LTL: Generated file output/mutants_LTL.txt with the mutants of the formulas. \n \t Number original formulas: {} \n \t Number of mutants: {}".format(n_formula, n_mutant))

file_in.close()
file_out.close()


##################################### LTL filter formulas #############################################
# delete lines with no mutants
# split text into columns. Each columsn contains a formula
df = pd.read_csv('output/mutants_LTL.txt', names=['text'])
split_columns = df['text'].str.split(' ', expand=True)
df_concatenated = pd.concat([df, split_columns], axis=1)
df_concatenated.drop(columns=['text'], inplace=True) # drop text column



# discarded formulas because without LTL equivalences
df_filter_discarded = df_concatenated[df_concatenated[1] == '']
df_filter_discarded.to_csv('output/discarded_mutants_LTL.txt', index=False,   header=False, sep=' ', quoting=csv.QUOTE_NONE)
print("LTL: Number of discarded formulas because without mutants: {}/{}".format(len(df_filter_discarded), len(df_concatenated)))



# formulas with LTL equivalences
df_filter = df_concatenated[df_concatenated[1] != '']
print("LTL: Number of formulas with mutants: {}/{}".format(len(df_filter),len(df_concatenated)))
df_filter = df_filter.reset_index(drop=True)
df_filter.to_csv('output/filtered_mutants_LTL.txt', index=False,   header=False, sep=' ', quoting=csv.QUOTE_NONE)




############################################## CTL ######################################################
print('\n')
maude.init(advise=True)
maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_mutant_CTL.maude'))
m = maude.getCurrentModule()
# print('Using', m, 'module')



# Using readlines()
file_in = open('output/formulas_CTL.txt', 'r') #read formula
# file_out formatted as formula .. mutant .. mutant .. mutant 
file_out = open('output/mutants_CTL.txt', 'a') #write formula and append mutants
Lines = file_in.readlines()

n_formula = 0
for line in Lines:
    n_formula += 1
    t = m.parseTerm(line)
    file_out.write(str(t) + ' ' + "" )
    pattern = m.parseTerm('M')

    n_mutant=0
    for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=2):
        # if M is not in the solution, print it
        # if it contains A or E keep it 
        if (str(sol).find('M') == -1) and (str(sol).find('A') == 1) and (str(sol).find('E') == 1):
        # if (str(sol).find('M') == -1) and str(sol) != str(t): #exclude the formula itself from the mutants
            n_mutant += 1
            file_out.write(str(sol) +  ' ' + "")
    file_out.write('\n')

print("CTL: Generated file output/mutants_CTL.txt with the mutants of the formulas. \n \t Number original formulas: ", n_formula, "\n \t Number of mutants: ", n_mutant)

file_in.close()
file_out.close()