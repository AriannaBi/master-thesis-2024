This directory contains code for running the auto file of each prism folder. 

cd run_PRISM
python3 run_files_PRISM.py


Before running it, you need to modify the properties according to LTL, CTL or PCTL and generate random formulas of that to test the model.


Run 

Install:
SPOT
Spin
ltl2ba
ltl2tgba (used by SPOT)
ltl2dstar (used by PRISM)
download folder, go into src, make, and put the executable in usr/local/bin where all the alias and executables are. Now you can use ltl2dstar on the terminal as well.

```bash
./prism model.pm -pf "P=? [ G F s=1 ]" -ltl2datool ../etc/scripts/hoa/hoa-ltl2dstar-with-ltl2ba-for-prism -ltl2dasyntax lbt
```

the model checker is tested by input the same formula and translate it with two different translators, to check 