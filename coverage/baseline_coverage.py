import random
import argparse
import coverage
import json
import sys
import os
import time


def calculate_coverage(filename="Button.py", ui_length=10, trial_limit=1000):
    if filename == "Button.py":
        from converted_codes import Button
        exec_code = Button.exec_code
    elif filename == "IfStatementConditional.py":
        from converted_codes import IfStatementConditional
        exec_code = IfStatementConditional.exec_code
    elif filename == "LoveOMeter.py":
        from converted_codes import LoveOMeter
        exec_code = LoveOMeter.exec_code
    elif filename == "StateChangeDetection.py":
        from converted_codes import StateChangeDetection
        exec_code = StateChangeDetection.exec_code
    elif filename == "SwitchCase.py":
        from converted_codes import SwitchCase
        exec_code = SwitchCase.exec_code
    else:  # Defualt: button
        from converted_codes import Button
        exec_code = Button.exec_code

    cov = coverage.Coverage()

    target_coverage = 100.0
    curr_coverage = 0
    trials = 0

    # Keep testing until the coverage reaches 100%
    max_coverage = 0
    while curr_coverage < target_coverage and trials < trial_limit:
        cov.start()  # Start measuring coverage
        random_interaction_seq = [[random.randint(0, 2048), random.randint(0, 2048)] for _ in range(ui_length)]
        exec_code(random_interaction_seq)
        cov.stop()  # Stop measuring coverage

        # Check current coverage
        cov.json_report(outfile="coverage/report.json")
        with open("coverage/report.json", 'r') as file:
            json_data = json.load(file)
        summary = json_data["files"][f"converted_codes\\{filename}"]["summary"]
        # print(summary)
        curr_coverage = min((int(summary["covered_lines"]) + 1) / int(summary['num_statements']) * 100, 100)
        os.remove("coverage/report.json")

        print(f"Trial {trials}: {curr_coverage}%")
        cov.html_report(directory=f"coverage/html_{curr_coverage}")  # for inspection
        cov.erase()  # Initialize coverage
        max_coverage = max(curr_coverage, max_coverage)
        trials += 1

    return trials, max_coverage

# usage: python simulator/baseline_coverage.py {filename} --t {trial_limit} --l {ui_length}
if __name__ == "__main__":
    # add parent directory (Gaeguri) to sys path
    parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    sys.path.append(parent_dir)

    random.seed(77)

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the python file to check baseline coverage")
    parser.add_argument("--t", help="trial limit to execute until")
    parser.add_argument("--l", help="user interaction sequence length to randomly generate")
    args = parser.parse_args()

    start = time.time()
    trials_needed, max_coverage = calculate_coverage(args.filename, trial_limit=int(args.t), ui_length=int(args.l))
    end = time.time()

    content_to_write = f'''
Coverage Result for {args.filename} (with ui_length = {args.l}, trial_limit = {args.t})
    - Trials needed to achieve 100% coverage : { "-" if trials_needed==int(args.t) else trials_needed}
    - Max Coverage % until {args.t} trials: {max_coverage:.2f}%
    - Total Execution Time: {end - start:.5f} sec
        
'''

    with open("coverage/result.txt", 'a') as file:
        file.write(content_to_write)

    print(content_to_write)
