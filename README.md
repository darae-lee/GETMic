# GETMic: Grammatical Evolution based Test case Generation for Micro-controller

CS454 Team 9 Code Repository

## Test case Generation using GE

```
python sbst/main.py [targe_code]
                    [--p population_size]
                    [--l user_interaction_length]
                    [--r random_seed]
```
Our experimental set-up is the same as <code>sbst/generate_testcase.sh</code>

## Coverage Checking
### 1. Create codes for coverage checking
```
python coverage/convert_target_code.py [target_code_filepath]
```
It can be executed at once with <code>coverage/convert_target_codes.sh</code>
### 2. Check coverage of the baseline
```
python coverage/baseline.py [target_code]
                            [--t trial_limit]
                            [--l user_interaction_length]
                            [--r random_seed]
```
Our experimental set-up is the same as <code>coverage/check_baseline_coverage.sh</code>
### 3. Check coverage of the GE-based test case
```
python coverage/sbst.py [target_code]
```
It can be executed at once with <code>coverage/check_sbst_coverage.sh</code>
