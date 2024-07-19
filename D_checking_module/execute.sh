# EXECUTE all the files for this module


# run spin spot containment checker
g++ -std=c++17 test_contain_checking_spot.cc -lspot -o test_contain_checking_spot -lbddx
./test_contain_checking_spot
