# Formula Generator

## Description 
This project allow to generate random LTL/CTL formulas, mutate them randomly, test if the mutations and the original formula are equivalent


## Usage
To use this project, run the following command:

```bash
python3 generate_formula.py
> generate formulas.txt
python3 generate_mutant.py
> generate mutants.txt
python3 check_if_equivalent.py
```

#### Maude folder
Contains the Maude files, which generates the random formulas:
generate_formula.maude
generate_mutant.maude

#### Spot folder
There is also a folder with spot which still has to be implemnted. 