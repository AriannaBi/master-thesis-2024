import os
import re
import random
import numpy as np
# cd Formula-generator
# python3 generate_formula.py 

# get atomic proposition from the model file
# helper functions that retrieve the atomics propositions
def get_atomic_propositions(file_name):
    atomic_propositions = []
    type_prism = ["int", "bool", "enum"]
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
                line_ap = re.findall(r'[^\t\s]\S*\s?:\s*[^\(].*\s*;', line)

                if len(line_ap) > 0:
                    split_ap = line_ap[0].split(":")

                    if (len(split_ap) == 2):
                        if split_ap[1].strip(' ')[0] == '[':
                            atomic_propositions.append(line_ap)
                        elif split_ap[1].strip(' ').strip(';') in type_prism:
                            atomic_propositions.append(line_ap)
    return atomic_propositions



# function that generates atomic propositions assignments. 
def generate_ap(file_name):
    atomic_props = get_atomic_propositions(file_name)
    generated_ap = []
    type_prism = ["int", "bool", "enum"]
    for elem in atomic_props:
        elem = elem[0].split(":")
        
        if elem[1].strip(' ').strip(';')  in type_prism:
            # print(elem)
            created_ap = elem[0] + " = true"
            created_ap = created_ap.replace(' ', '')
            generated_ap.append(created_ap)

            created_ap = elem[0] + " = false"
            created_ap = created_ap.replace(' ', '')
            generated_ap.append(created_ap)
        else:
            # take the two numbers inside the square brakets
            start = int(re.findall(r'\d+', elem[1])[0])
            end = re.findall(r'\.\.\S*\]', elem[1])[0].strip(']').strip('..')
            # print(start)
            # print(end)
            if end.isdigit():
                # print("here")
                for i in range(start, int(end)+1):
                    created_ap = elem[0] + "=" + str(i)
                    created_ap = created_ap.replace(' ', '')
                    generated_ap.append(created_ap)
            # else:
                # add a random number for MAX or N???
            # generated_ap.append(elem[0] + " = " + str(random.randint(0, 1)))
    return generated_ap






# ap = get_atomic_propositions(file_name)
# print(ap)
# for a in ap:
#     print(a)
# print(" ")
# random_ap = generate_random_ap(ap)
# for a in random_ap:
#     print(a)




if __name__ == "__main__":
    # file_name = "../prism-examples/dtmcs/herman/herman3.pm"
    file_name = "model.pm"
    ap = generate_ap(file_name)
    print(ap)






# traverse root directory, and list directories as dirs and files as files
# for root, dirs, files in os.walk("prism-examples"):
#     path = root.split(os.sep)
#     destination = "copy-" + root    
#     shutil.copy("run_PRISM/prism", destination)
#     os.chmod(destination, 0o777)
#     # print((len(path) - 1) * '---', os.path.basename(root))
#     for file in files:
#         # print(len(path) * '---', file)
#         # model doesn't have to be modified, because it works even with probabilities
#         # if file.endswith(".pm") or file.endswith(".sm") or file.endswith(".nsm") or file.endswith(".nm") or file.endswith(".prism"):
#         #     file_name = os.path.join(root, file)
#         #     modify_model(file_name)
#         if file.endswith(".pctl") or file.endswith(".csl") or file.endswith(".props"):
#             file_name = os.path.join(root, file)
#             modify_property(file_name)
#         elif file == "auto":
#             modify_auto(root)



