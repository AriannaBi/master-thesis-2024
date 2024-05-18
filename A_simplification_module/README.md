
first run test_simplif.cc
g++ -std=c++17 test_simplif.cc -lspot -o test_simplif
./test_simplif

it creates a file in output/ with the formulas simplified.


then sanity_check_eq_LTL.py
python3 sanity_check_eq_LTL.py