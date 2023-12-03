import random
import argparse
import coverage
import json
import sys
import os
import time

# add parent directory (Gaeguri) to sys path
parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(parent_dir)

UI_LENGTH = 1  # TODO
MAX_RANGE = 2000
CLOCK_TIME = 10  # TODO

# file_name_dict = {"button": "Button.py",
#                   "if": "IfStatementConditional.py",
#                   "love": "LoveOMeter.py",
#                   "state": "StateChangeDetection.py",
#                   "switch": "SwitchCase.py"}


def calculate_coverage(target="Button.py"):
    cov = coverage.Coverage()

    target_coverage = 100.0
    curr_coverage = 0
    trials = 0

    # Keep testing until the coverage reaches 100%
    while curr_coverage < target_coverage:
        cov.start()  # Start measuring coverage
        random_interaction_seq = [[random.randint(0, MAX_RANGE), random.randint(0, MAX_RANGE)] for _ in range(UI_LENGTH)]

        if target == "Button.py":
            from converted_codes import Button
            Button.exec_code(random_interaction_seq, CLOCK_TIME)
        elif target == "IfStatementConditional.py":
            from converted_codes import IfStatementConditional
            IfStatementConditional.exec_code(random_interaction_seq, CLOCK_TIME)
        elif target == "LoveOMeter.py":
            from converted_codes import LoveOMeter
            LoveOMeter.exec_code(random_interaction_seq, CLOCK_TIME)
        elif target == "StateChangeDetection.py":
            from converted_codes import StateChangeDetection
            StateChangeDetection.exec_code(random_interaction_seq, CLOCK_TIME)
        elif target == "SwitchCase.py":
            from converted_codes import SwitchCase
            SwitchCase.exec_code(random_interaction_seq, CLOCK_TIME)
        else:  # Defualt: button
            from converted_codes import Button
            Button.exec_code(random_interaction_seq, CLOCK_TIME)

        cov.stop()  # Stop measuring coverage

        trials += 1

        cov.json_report(outfile="coverage/report.json")
        with open("coverage/report.json", 'r') as file:
            json_data = json.load(file)
        curr_coverage = float(json_data["files"][f"converted_codes/{target}"]["summary"]["percent_covered"])
        os.remove("coverage/report.json")

        print(f"Trial {trials}: {curr_coverage}%")
        # cov.html_report() # 어디서 fail 하는지 index.html에서 볼 수 있음
    # cov.save()
    return trials

# usage: python simulator/baseline_coverage.py {button/if/love/state/switch}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="the target python file to convert for checking baseline coverage")
    args = parser.parse_args()

    start = time.time()
    trials_needed = calculate_coverage(args.target)
    end = time.time()

    with open("coverage/result.txt", 'a') as file:
        file.write(f"Trials needed to achieve 100% coverage for {args.target}: {trials_needed}\n Execution Time: {end - start:.5f} sec\n")

    print(f"Trials needed to achieve 100% coverage for {args.target}: {trials_needed}")
    print(f"Execution Time: {end - start:.5f} sec")