'''
Convert target code for checking baseline coverage
'''

import argparse
import os

INDENT = " "*4

# seperate the whole code -> import / setup / loop
def separate_code(code):
    import_end_lineno = 0
    loop_start_lineno = 0
    for i, line in enumerate(code):
        sline = line.strip()
        if sline.startswith("from") or sline.startswith("import"):
            import_end_lineno = i
        elif sline.startswith("while True:"):
            loop_start_lineno = i
    return import_end_lineno, loop_start_lineno


def convert_import_code(code):
    import_code = ["import os\n",
                   "import sys\n",
                   "parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))\n",
                   "sys.path.append(os.path.join(parent_dir, 'simulator'))\n"]
    machine_flag = 0
    for line in code:
        import_code.append(line)
        if line.strip() == "import machine":
            machine_flag = 1
    if machine_flag==0:
        import_code.append("import machine\n")
    import_code.append("\n")
    return import_code


def convert_setup_code(code):
    body_code = ["def exec_code(random_interaction_seq: list):\n",
                 INDENT + "machine.load_board(__file__)\n"]
    for line in code:
        body_code.append(INDENT + line)
    body_code.extend([INDENT + "interactor = machine.UserInteract(random_interaction_seq)\n",
                      INDENT + "interactor.start()\n",
                      "\n"])
    return body_code


def convert_loop_code(code):
    loop_code = []
    for line in code:
        loop_code.append(INDENT + line)
    loop_code.extend([INDENT*2 + "if not interactor.is_alive():\n",
                      INDENT*3 + "break\n"])
    return loop_code

def add_no_coverage(code):
    no_cov_code = []
    for line in code:
        sline = line.strip()
        if sline and not sline.startswith("def exec_code") and not sline.startswith("#"):
            no_cov_code.append(line.rstrip() + "  # pragma: no cover\n")
        else:
            no_cov_code.append(line)
    return no_cov_code


def convert_code(code):
    import_end_lineno, loop_start_lineno = separate_code(code)
    # set indent
    global INDENT
    line_next_to_while = code[loop_start_lineno+1]
    INDENT = " " * (len(line_next_to_while) - len(line_next_to_while.lstrip()))
    # convert
    import_code = convert_import_code(code[:import_end_lineno + 1])
    setup_code = convert_setup_code(code[import_end_lineno + 1:loop_start_lineno])
    loop_code = convert_loop_code(code[loop_start_lineno:])
    above_loop_code = add_no_coverage(import_code + setup_code)

    return above_loop_code + loop_code


# usage: python simulator/convert_target_code.py target_codes/{}.py
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="the target python file to convert for checking baseline coverage")
    args = parser.parse_args()

    with open(args.target, "r") as f:
        code = f.readlines()

    new_code = convert_code(code)

    current_file_path = os.path.dirname(os.path.abspath(__file__))
    parent_file_path = os.path.abspath(os.path.join(current_file_path, os.pardir))
    test_file_name = os.path.join(parent_file_path, "converted_codes", os.path.basename(args.target))

    with open(test_file_name, 'w') as f:
        f.write("".join(new_code))
