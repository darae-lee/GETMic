# GETMic: Grammatical Evolution based Test case Generation for Micro-controller

CS454 Team 9 Code Repository

## Test case Generation using GE

```
python sbst/main.py [target code] --p [population size] --l [user interaction length] --r [random seed]
```
Our experimental set-up is the same as <code>generate_testcase.sh</code>

## Coverage Checking
### 1. Create codes for coverage checking
```
python coverage/convert_target_code.py [target code filepath]
```
It can be executed at once with <code>./convert_target_codes.sh</code>
### 2. Check coverage of the baseline
```
python coverage/baseline.py [target code] --t [trial limit] --l [user interaction length] --r [random seed]
```
Our experimental set-up is the same as <code>check_baseline_coverage.sh</code>
### 3. Check coverage of the GE-based test case
```
python coverage/sbst.py [target code]
```
It can be executed at once with <code>./check_sbst_coverage.sh</code>
