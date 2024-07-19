import os
import re
import random
import numpy as np
import shutil
# cd Formula-generator

# Get atomic propositions and labels string from the module file
def get_ap_and_label(module_file_name):
    ap = []
    label = []
    # type_prism = ["int", "bool", "enum"]
    with open(module_file_name, 'r', encoding='ISO-8859-1') as file:
        lines = file.readlines()
        for line in lines:
            # Find ap
            line_ap = re.findall(r'\S+\s*:\s*\[\d+\.\.\d+\];', line) #find atomic propositions s.a. s : [0..4];
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
                
    return ap, label

def random_combination_ap(name, min, max):
    return name + "=" + str(random.randint(min, max))

# function that generates atomic propositions assignments. 
def generate_ap(file_name):
    ap, label = get_ap_and_label(file_name)
    generated_ap = []

    for elem in ap:
        print(elem)
        elem = elem.split("=")
        # elem = elem[0].split("=")
        range = elem[1].split("..")

        name = elem[0]
        min = int(range[0])
        max = int(range[1])
        # print(name, min, max)
        generated_ap.append(random_combination_ap(name, min, max))
    return generated_ap, label


def contain_for_loop(file_name):
    with open(file_name, 'r', encoding='ISO-8859-1') as file:
        content = file.read()
        if "for" in content:
            return True
    return False

if __name__ == "__main__":
    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk("../prism-examples"):
        path = root.split(os.sep)
        shutil.copy("prism", root)
        os.chmod(root, 0o777)
        for name_file in files:
            # print(len(path) * '---', file)
            # model doesn't have to be modified, because it works even with probabilities
            # if file.endswith(".pm") or file.endswith(".sm") or file.endswith(".nsm") or file.endswith(".nm") or file.endswith(".prism"):
            #     file_name = os.path.join(root, file)
            #     modify_model(file_name)
            # if file.endswith(".pctl") or file.endswith(".csl") or file.endswith(".props"):
            #     file_name = os.path.join(root, file)
            #     modify_property(file_name)
            # elif file == "auto":
            #     modify_auto(root)



            # if name_file == "auto":
            #     # for now, if in the auto file there is a for loop, we skip the file.
            #     # try:
            #     with open(os.path.join(root , name_file), 'r') as file:
            #         # Read the entire file content
            #         content = file.read()
            #         # Check if the string "for" is in the content
            #         if "for" in content:
            #             print("Found 'for' in ", root)
            #     # except FileNotFoundError:
            #     #     print(f"The file {root} does not exist.")

            if name_file.endswith(".pm") or name_file.endswith(".sm") or name_file.endswith(".nsm") or name_file.endswith(".nm") or name_file.endswith(".prism"):
                # ap, label = get_ap_and_label(os.path.join(root, name_file))
                # print("file: ", os.path.join(root, name_file), "ap: ", ap, "label: ", label)
                ap = generate_ap(os.path.join(root, name_file))
                print(ap)
            print('\n\n')
