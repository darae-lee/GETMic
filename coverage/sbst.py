import argparse
import coverage
import sys
import os
import json
import pandas as pd
import platform
import ast
import time

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(root_dir, 'simulator'))

import machine

def calculate_coverage(filename, solution):
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

    cov = coverage.Coverage()

    cov.start()
    exec_code(solution)
    cov.stop()

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
    cov.erase()

    return curr_coverage

# usage: python coverage/sbst.py {filename}
if __name__ == "__main__":
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(root_dir)

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the python file to check baseline coverage")
    
    args = parser.parse_args()

    input_filename = f"sbst/result/{args.filename[:-3]}.csv"
    output_filename = f"coverage/result_sbst/{args.filename[:-3]}.csv"

    df = pd.read_csv(input_filename)

    df['genotype'] = df['genotype'].apply(lambda x: ast.literal_eval(x))
    
    for index, row in df.iterrows():
        start_time = time.time()
        df.at[index, 'coverage'] = calculate_coverage(args.filename, row['genotype'])
        end_time = time.time()
        df.at[index, 'time_taken'] += end_time - start_time

    df.to_csv(output_filename, index=False)