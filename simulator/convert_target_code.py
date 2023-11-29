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
    import_code = []
    for line in code:
        if line.strip() != "import utime":
            import_code.append(line.rstrip() + "  # pragma: no cover\n")
    import_code.extend(["from machine import UserInteract  # pragma: no cover\n", "import random  # pragma: no cover\n"])

    return import_code


def convert_loop_code(code):
    loop_code = ["for interaction in random_interactions:\n",
                 INDENT + "timing_of_interaction = random.randint(0, space_num + 1)\n",
                 INDENT + "interaction_gen[timing_of_interaction] = interaction % interactions_type_num\n",
                 INDENT + "interactor.interact(interaction_gen[0])\n"]
    interaction_idx = 1
    need_indent = 0
    indentation_before = INDENT
    # 기존 코드 추가 후, interaction 코드 추가
    for i, line in enumerate(code):
        sline = line.strip()
        first_word = sline.split(" ")[0]
        if i == 0 or sline.startswith("utime.sleep") or sline == "":  # skip While True:
            continue
        loop_code.append(line)
        if first_word in ["if", "elif", "else:"]:  # TODO: for, while 넣을 필요 있을까용
            indentation_before = line[:len(line) - len(line.lstrip())] + INDENT
            loop_code.append(indentation_before + f"interactor.interact(interaction_gen[{interaction_idx}])\n")
            need_indent = 1
        # elif need_indent:
        #     indentation_before = INDENT + indentation_before
        #     loop_code.append(indentation_before + f"interactor.interact(interaction_gen[{interaction_idx}])\n")
        #     need_indent = 0
        else:
            indentation_before = line[:len(line) - len(line.lstrip())]
            loop_code.append(indentation_before + f"interactor.interact(interaction_gen[{interaction_idx}])\n")
        interaction_idx += 1
    loop_code.append(INDENT + "interaction_gen[timing_of_interaction] = 0\n")

    return loop_code, interaction_idx


def add_def(code, space_cnt):
    body_code = ["def exec_code(random_interactions: list):  # pragma: no cover\n",
                 INDENT + "interactor = UserInteract()\n",
                 INDENT + "interactions_type_num = len(interactor.codes)\n",
                 INDENT + f"space_num = {space_cnt}\n",
                 INDENT + "interaction_gen = {}\n",
                 INDENT + "for idx in range(space_num):\n",
                 INDENT*2 + "interaction_gen[idx] = 0\n"]
    for line in code:
        body_code.append(INDENT + line)
    return body_code


def convert_code(code):
    import_end_lineno, loop_start_lineno = separate_code(code)
    # set indent
    global INDENT
    line_next_to_while = code[loop_start_lineno+1]
    INDENT = " " * (len(line_next_to_while) - len(line_next_to_while.lstrip()))
    # convert
    import_code = convert_import_code(code[:import_end_lineno + 1])
    loop_code, space_cnt = convert_loop_code(code[loop_start_lineno:])
    body_code = add_def(code[import_end_lineno + 1:loop_start_lineno] + loop_code, space_cnt)  # import 부분 빼고 모두
    return import_code + body_code


# usage: python simulator/convert_target_code.py target_codes/{}.py
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="the target python file to convert for checking baseline coverage")
    args = parser.parse_args()

    with open(args.target, "r") as f:
        code = f.readlines()

    new_code = convert_code(code)
    test_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_" + os.path.basename(args.target))
    # test_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "baseline_target_codes", "test_" + os.path.basename(args.target))
    with open(test_file_name, 'w') as f:
        f.write("".join(new_code))
