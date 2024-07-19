import os
import re
import random
import numpy as np
import shutil


file_name_input_LTL = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', 'formulas_LTL.txt'))
file_name_input_CTL = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', 'formulas_CTL.txt'))

# Modify file LTL formulas file 
modified_lines = []
with open(file_name_input_LTL, 'r') as f:
    content = f.readlines()
    modified_lines = [line.replace('a', '.')
                        .replace('b', '.')
                        .replace('c', '.')
                        for line in content]
    
with open(file_name_input_LTL, 'w') as file:
    file.writelines(modified_lines)


modified_lines = []
with open(file_name_input_CTL, 'r') as f:
    content = f.readlines()
    modified_lines = [line.replace('a', '.')
                        .replace('b', '.')
                        .replace('c', '.')
                        for line in content]
    
with open(file_name_input_CTL, 'w') as file:
    file.writelines(modified_lines)