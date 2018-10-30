# TABLE OF CONTENTS
1. [PROBLEM](README.md#problem)
2. [APPROACH](README.md#approach)
3. [RUN INSTRUCTIONS](README.md#run-instructions)

# PROBLEM

The goal is to parse a csv file kept at `./input/h1b_input.csv` and aggregate the rows into the top 10 occupations and top 10 states. We store the results under `./output/top_10_occupations.csv` and `./output/top_10_states.csv` respectively. We also define several test cases to verify the result of the aggregation.

# APPROACH

To parse the csv file, a python script is provided at [`./src/h1b_counting.py`](src/h1b_counting.py). The python code uses two dicts to keep track of the counts for occupations and states. It then parses the input file line by line and checks if the status is `CERTIFIED`. If it is, it then adds 1 to the appropriate entry under each dict. Since there are a lot of duplicate names under the field `soc_name`, we take the `soc_code` and then do a lookup for the occupation name or `soc_name`. We do the lookup by using the data from [here](https://www.bls.gov/emp/documentation/crosswalks.htm).

Once it finishes reading the file entirely, it gets all the items from the dicts, sorts them according to the a custom lambda function: count (descending), key (ascending/alphabetical). Once sorted, the code writes the first 10 entries to the corresponding output file.

# RUN INSTRUCTIONS

To parse a csv file, replace [./input/h1b_input.csv](input/h1b_input.csv) with the new csv file and then run `./run.sh`.

To run all the testcases,
  `cd insight_testsuite`
  `./run_tests.sh`
