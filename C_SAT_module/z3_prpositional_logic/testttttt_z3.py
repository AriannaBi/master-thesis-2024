from z3 import *

# read file 

file_out_12 = 'generate/output/z3_4_12.txt'
file_out_8 = 'generate/output/z3_4_8.txt'

with open(file_out_12, 'r') as file1, open(file_out_8, 'r') as file2:
    line_num = 1
    while True:
        line1 = file1.readline()
        line2 = file2.readline()

        # Break the loop if both lines are empty (end of file)
        if not line1 and not line2:
            break

        # Strip newline characters for comparison
        line1 = line1.rstrip('\n')
        line2 = line2.rstrip('\n')

        if line1 != line2:
            print(f"Line {line_num} sat is different.")
            print(f"File1: {line1}")
            print(f"File2: {line2}")
        # else:
        #     print(f"Line {line_num} sat is the same.")

        line_num += 1