import os
import re

# cd run_PRISM
# python3 run_files_PRISM.py



# base_path = "./copy-prism-examples"
# if not os.path.exists(base_path):
#     os.mkdir(os.path.join(base_path))




def run_all_files():
    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk("../copy-prism-examples"):
        path = root.split(os.sep)
        # print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            if file == "auto":
                print(root, file)
                # print(".././" + os.path.join(root, file))
                os.system("./" + os.path.join(root, file))


def run_file(name):
    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk("../copy-prism-examples"):
        path = root.split(os.sep)
        if root.split('/')[-1] == name:
            for file in files:
                if file == "auto":
                    print(root, file)
                    # print(".././" + os.path.join(root, file))
                    os.system("./" + os.path.join(root, file))



run_file("brp")





