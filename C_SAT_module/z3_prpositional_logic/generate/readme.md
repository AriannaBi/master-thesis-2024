# Formula Generator

## Description 
This project allow to generate random LTL/CTL formulas, mutate them randomly, test if the mutations and the original formula are equivalent

## Pipeline
generation of the formulas -> generation of the mutants -> filtration of the mutants -> check equivalences original-mutants

## Usage
To use this project, run the following command:

```bash
python3 generate_formula.py
> generate formulas.txt
python3 generate_mutant.py
> generate mutants.txt
python3 sanity_check_LTL.py
python3 sanity_check_CTL.py
```

To run all this files in one go, run the executable file 
```
./execute_generation_pipeline.sh
```
and it executes the four files above with the atomic propositions [a,b,c] that you can change in the executable file, and depth 4 for the original formulas that you can change in the search function inside the file for generating formulas.

#### Maude folder
Contains the Maude files, which generates the random formulas:
generate_formula_LTL.maude
generate_formula_CTL.maude
generate_mutant_LTL.maude
generate_mutant_CTL.maude
