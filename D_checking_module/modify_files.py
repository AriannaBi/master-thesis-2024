import os
import re
import shutil

# cd Formula-generator
# python3 generate_formula.py 


# base_path = "./copy-prism-examples"
# if not os.path.exists(base_path):
#     os.mkdir(os.path.join(base_path))


# if it is const int ...; then I need to take the name and replace it with a number
# or i can just run it in a for loop without doing anything and working only on probabilities

# if it is const double ...; then i know it is a probability and i can just remove it. 
# actually it is better if i keep the declaration const double prob; because i just need to remove it when use it 
# like in the guard. there are some declarations like p1=p2 in which i need the declaration of p1


# given a file, modify the model by removing the probabilities and copying the file to a new file

'''
def modify_model(file_name):
    original_file = file_name

    file_name = "copy-" + file_name
    file_name_left = file_name.split('.')[0].split('/')[-1] + "." + file_name.split('.')[-1]
    file_name_right = '/'.join(file_name.split('.')[0].split('/')[:-1] )
    file_name_right = file_name_right + '/' + file_name_left

    file_out = open(file_name_right, "w")

    # read files in original folder original/brp, then remove the files in the copy folder copy/brp, 
    # and write to the copy folder copy/copy-brp
    with open(original_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # if os.path.exists(file_name):
    #     os.remove(file_name)

    modified_lines = []
    # concatenate lines until the line ends with ;
    # for idx, line in enumerate(lines):
    #     if line.find(';') == -1: #if the line does not end with ;
    #         while lines[idx+1].find(';') == -1:
    #             line = line + lines[idx+1]
    #             idx += 1

        # if 
    
    for line in lines:
        # remove comments 
        line = re.sub(r'\s*\/\/.*?$', '', line)
        #FOUND ARROW and COLON
        if line.find('->') != -1 and line.find(':') != -1: 
            line = remove_probability_model(line)
            # if previous line is not empty and does not end with ;
        # else if line matches (\s+\+) 
        # if matches white space and + 
        elif re.match(r'\s+\+', line) is not None:
            line = remove_probability_without_arrow(line)

        modified_lines.append(line)

        if line != '\n':
            file_out.write(line)

    print("Modified model in file ", file_name_right)
    # delete original file in copy folder, because now there is only the copy file (modified)
    
    file_out.close()
'''



def modify_property(file_name):
    # if filename has a name .smth 
    if file_name.split('/')[-1].split('.')[0] == '':
        print("skip ", file_name)
    else:
        
        original_file = file_name

        file_name = "copy-" + file_name
        file_name_left = file_name.split('.')[0].split('/')[-1] + "." + file_name.split('.')[-1]
        file_name_right = '/'.join(file_name.split('.')[0].split('/')[:-1] )
        file_name_right = file_name_right + '/' + file_name_left

        file_out = open(file_name_right, "w")

        with open(original_file, 'r') as file:
            lines = file.readlines()


        for line in lines:
            # remove comments 
            # line = re.sub(r'\s*\/\/.*?$', '', line)
            if line.find("P=?") != -1:
                line_copy = line
                line = line.replace("P=?", "E")
                line = line + '\n' + line_copy.replace("P=?", "A") #just create another formula with E and A 
            if line.find("R=?") != -1:
                line_copy = line
                line = line.replace("R=?", "E")
                line = line + '\n' + line_copy.replace("R=?", "A") #just create another formula with E and A 


            if line != '\n':
                file_out.write(line)

        
        # delete original file in copy folder, because now there is only the copy file (modified)
        # if os.path.exists(file_name):
        #     os.remove(file_name)
        print("Modified property in file ", file_name_right)
        file_out.close()





# stringg = "[] (s=0) -> fast : (s'=1) + slow : (s'=4);"
# file_name_destined = "copy-prism-examples/dtmcs/brp/brp.pm"
# modify_model(file_name_destined)

# read auto file from copy folder and add ./ to prism
def modify_auto(file_name):
    original = "copy-" + file_name
    file_name = "copy-" + file_name + "/auto"
    # print(file_name)
    
    # open file and read lines
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()


    # add ./ to prism and write to file
    file_out = open(file_name, "w")
    for line in lines:
        # add ./ to prism 
        # if prism is found in the line and it is not ./
        if line.find("prism") != -1 and line.find("./") == -1:
            line = line.replace("prism", "./prism", 1)

            line_array = line.split(" ")
            # insert a random char because in the loop I am excluding the last element
            line_array.insert(len(line_array), '\n')

            for idx, elem in enumerate(line_array[1:-1]):
                # elem = elem.rstrip('\n')
                # print("ELEMENT", elem )
                # print(elem, idx)
                # if the dot is found in the element
                # and if the element end with an extension
                if elem.find(".prism") != -1 or elem.find(".pepa") != -1 or elem.find(".props") != -1 or elem.find(".pm") != -1 or elem.find(".sm") != -1 or elem.find(".nsm") != -1 or elem.find(".nm") != -1 or elem.find(".pctl") != -1:
                    # print("found dot", elem, idx)
                    # print("found dot", elem, '\n')
                    argument = "../" + original + "/" + line_array[idx+1]
                    line = line.replace(line_array[idx+1], argument)


            # first_argument = "../" + original + "/" + line_array[1]
            # line = line.replace(line_array[1], first_argument)

            # second_argument = "../" + original + "/" + line_array[2]
            # line = line.replace(line_array[2], second_argument)

        
        file_out.write(line)

    os.chmod(file_name, 0o777)

    print("Modified auto in file ", file_name)
    file_out.close()



# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk("prism-examples"):
    path = root.split(os.sep)
    destination = "copy-" + root    
    shutil.copy("run_PRISM/prism", destination)
    os.chmod(destination, 0o777)
    # print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        # print(len(path) * '---', file)
        # model doesn't have to be modified, because it works even with probabilities
        # if file.endswith(".pm") or file.endswith(".sm") or file.endswith(".nsm") or file.endswith(".nm") or file.endswith(".prism"):
        #     file_name = os.path.join(root, file)
        #     modify_model(file_name)
        if file.endswith(".pctl") or file.endswith(".csl") or file.endswith(".props"):
            file_name = os.path.join(root, file)
            modify_property(file_name)
        elif file == "auto":
            modify_auto(root)



