import random
import argparse
import coverage

import test_Button
import test_IfStatementConditional
import test_LoveOMeter
import test_StateChangeDetection
import test_SwitchCase

UI_LENGTH = 1  # TODO
MAX_RANGE = 100

file_name_dict = {"button": "test_Button.py",
                  "if": "test_IfStatementConditional.py",
                  "love": "test_LoveOMeter.py",
                  "state": "test_StateChangeDetection.py",
                  "switch": "test_SwitchCase.py"}


def calculate_coverage(target="button"):
    test_code = test_Button.exec_code   # Default
    if target == "button":
        test_code = test_Button.exec_code
    elif target == "if":
        test_code = test_IfStatementConditional.exec_code
    elif target == "love":
        test_code = test_LoveOMeter.exec_code
    elif target == "state":
        test_code = test_StateChangeDetection.exec_code
    elif target == "switch":
        test_code = test_SwitchCase.exec_code

    cov = coverage.Coverage()
    trials = 0
    target_coverage = 100.0
    curr_coverage = 0

    while curr_coverage < target_coverage:
        cov.start()
        random_interactions = [random.randint(0, MAX_RANGE) for _ in range(UI_LENGTH)]
        test_code(random_interactions)  # Execute
        cov.stop()
        trials += 1
        # curr_coverage = cov.json_report(include=f"simulator/{file_name_dict[target]}")
        curr_coverage = cov.report()  #include="simulator/test_*.py"
        # curr_coverage = cov.report(include=f"simulator/{file_name_dict[target]}")
        print(curr_coverage)
        # cov.html_report(include=file_name_dict[target])  # 어디서 나가리 되는지 볼 수 있음
        # cov.save()
        # break
    # cov.save()
    return trials

# usage: python simulator/baseline_coverage.py {button/if/love/state/switch}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="the target python file to convert for checking baseline coverage")
    args = parser.parse_args()
    trials_needed = calculate_coverage(args.target)
    print(f"Trials needed to achieve 100% coverage for {file_name_dict[args.target]}: {trials_needed}")