# TABLE OF CONTENTS
1. [PROBLEM](README.md#problem)
2. [APPROACH](README.md#approach)
3. [RUN INSTRUCTIONS](README.md#run-instructions)
4. [SPECIAL NOTE REGARDING SOC_CODE AND SOC_NAME](README.md#special-note-regarding-soc_code-and-soc_name)

# PROBLEM

The goal is to parse a csv file kept at `./input/h1b_input.csv` and aggregate the rows into the top 10 occupations and top 10 states. We store the results under `./output/top_10_occupations.csv` and `./output/top_10_states.csv` respectively. We also define several test cases to verify the result of the aggregation.

# APPROACH

To parse the csv file, a python script is provided at [`./src/h1b_counting.py`](src/h1b_counting.py). The python code uses two dicts to keep track of the counts for occupations and states. It then parses the input file line by line and checks if the status is `CERTIFIED`. If it is, it then adds 1 to the appropriate entry under each dict.

Once it finishes reading the file entirely, it gets all the items from the dicts, sorts them according to the a custom lambda function: count (descending), key (ascending/alphabetical). Once sorted, the code writes the first 10 entries to the corresponding output file.

# RUN INSTRUCTIONS

To parse a csv file, replace [./input/h1b_input.csv](input/h1b_input.csv) with the new csv file and then run `./run.sh`.

To run all the testcases,

  `cd insight_testsuite`
  
  `bash ./run_tests.sh`
  
# SPECIAL NOTE REGARDING SOC_CODE AND SOC_NAME

It is observed in the dataset that there are a lot of duplicate occupations under `SOC_NAME` which should all probably be the same occupation. To mitigate this I attempted to get the `SOC_CODE` and then convert that to `SOC_NAME` based on mapping defined in official documentation. But since the occupation code does not match the expected result, `test_1` failed. So I am not merging that code into the `master` but you can observe my attempt in the branch `soc_code`
