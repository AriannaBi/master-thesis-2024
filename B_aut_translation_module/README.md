
first run gen_AUT_spot_spin.py to generate from two formulas, tow automatas, utilizing two different translators. 

then the automatas are generated and saved as HOA files.  

Then the program test_AUTinput.cc read the HOA files and works on the automatas. The formulas are original and mutant, and the translators are two different. 


the file test_LTLinput.cc reads two formulas (original and mutant) and compare the two automatas using spot translator. 


# Automata Translation

## Description 
This project allow to translate LTL formulas into automata using Spot and Spin translators. 


## Usage
To use this project, run the following command:
```bash 
g++ -std=c++17 simplification.cc -lspot -o simplification
./simplification
> output/spot_all_options.txt
python3 test_equal_LTL.py
python3 test_equivalent_LTL.py

```

To run all this files in one go, run the executable file 
```
./execute.sh
```