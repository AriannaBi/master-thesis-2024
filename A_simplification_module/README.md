
# Formula Simplification

## Description 
This project allow to simplify the formulas we previously generated in the pipeline. We work on LTL only. 


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