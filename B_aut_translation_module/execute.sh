# EXECUTE all the files for this module


g++ -std=c++17 test_check_equiv_isomorph.cc -lspot -o test_check_equiv_isomorph  -lbddx
./test_check_equiv_isomorph

python3 gen_spot_spin_automata.py

g++ -std=c++17 test_spot_spin_compare.cc -lspot -o test_spot_spin_compare -lbddx
./test_spot_spin_compare


