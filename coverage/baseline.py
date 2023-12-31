import random
import argparse
import coverage
import json
import sys
import os
import time
import platform
import csv

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(root_dir, 'simulator'))

import machine

def calculate_coverage(filename="Button.py", ui_length=10, trial_limit=1000):

    # Import target code
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
    elif filename == "SegmentDisplay.py":
        from converted_codes import SegmentDisplay
        exec_code = SegmentDisplay.exec_code
    elif filename == "WarmButton.py":
        from converted_codes import WarmButton
        exec_code = WarmButton.exec_code
    elif filename == "ButtonCounter.py":
        from converted_codes import ButtonCounter
        exec_code = ButtonCounter.exec_code
    elif filename == "ComplexButton.py":
        from converted_codes import ComplexButton
        exec_code = ComplexButton.exec_code
    else:  # Defualt: button
        from converted_codes import Button
        exec_code = Button.exec_code

    cov = coverage.Coverage(branch=True)

    target_coverage = 100.0
    curr_coverage = 0
    trials = 0
    best_seq = []

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

        system_name = platform.system()
        if system_name == 'Darwin':
            summary = json_data["files"][f"coverage/converted_codes/{filename}"]["summary"]
        elif system_name == 'Windows':
            summary = json_data["files"][f"coverage\\converted_codes\\{filename}"]["summary"]
        else:
            NotImplementedError("Only Darwin & Windows..")

        curr_coverage = min((int(summary["covered_lines"]) + 1) / int(summary['num_statements']) * 100, 100)
        os.remove("coverage/report.json")
        # cov.html_report(directory=f"coverage/html_{curr_coverage}")  # for inspection

        print(f"Trial {trials}: {curr_coverage}%")
        # cov.html_report(directory=f"coverage/html_{curr_coverage}")  # for inspection
        cov.erase()  # Initialize coverage
        if curr_coverage > max_coverage:
            max_coverage = curr_coverage
            best_seq = random_interaction_seq
        trials += 1

    return trials, max_coverage, best_seq

# usage: python coverage/baseline.py {filename} --t {trial_limit} --l {ui_length}
if __name__ == "__main__":
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(root_dir)

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the python file to check baseline coverage")
    parser.add_argument("--t", help="trial limit to execute until")
    parser.add_argument("--l", help="user interaction sequence length to randomly generate")
    parser.add_argument("--r", help="random seed")

    args = parser.parse_args()

    random.seed(int(args.r))

    start = time.time()
    # This coverage is statement level coverage(not branch level)
    trials_needed, max_coverage, best_seq = calculate_coverage(args.filename, trial_limit=int(args.t), ui_length=int(args.l))
    end = time.time()

    content_to_write = f'''
Coverage Result for {args.filename} (with ui_length = {args.l}, trial_limit = {args.t}, random_seed = {args.r})
    - Trials needed to achieve 100% coverage : { "-" if trials_needed==int(args.t) else trials_needed}
    - Max Coverage % until {args.t} trials: {max_coverage:.2f}%
    - Total Execution Time: {end - start:.5f} sec
    - Best seq: {best_seq}
    - Best seq (human): {machine.convert_seqs_to_readable(best_seq)}
        
'''

    csv_filename = f"coverage/result_baseline/{args.filename[:-3]}.csv"
    if not os.path.isfile(csv_filename):
        with open(csv_filename, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['filename', 'ui_length', 'trial_limit', 'seed', 'trials_needed', 'max_coverage', 'time_taken', 'genotype', 'phenotype'])
            csv_writer.writerow([args.filename, args.l, args.t, args.r, trials_needed, max_coverage, end - start, best_seq, machine.convert_seqs_to_readable(best_seq)])
    else:
        with open(csv_filename, 'a', newline="\n") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([args.filename, args.l, args.t, args.r, trials_needed, max_coverage, end - start, best_seq, machine.convert_seqs_to_readable(best_seq)])

    print(content_to_write)
