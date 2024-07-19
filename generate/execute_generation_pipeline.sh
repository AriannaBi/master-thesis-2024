# EXECUTE the generation of formulas, original and mutants, plus the the sanity check


python3 generate_formula.py a,b,c
python3 generate_mutant.py a,b,c
python3 sanity_check_LTL.py
python3 sanity_check_CTL.py

