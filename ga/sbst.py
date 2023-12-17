import random
import argparse
import ast
import coverage
import sys
import os
import json
import time
import platform
import csv


class codeNodes:
    def __init__(self):
        self.target_ids = []
        self.target_types = []
        self.infos = [] #(target_ids, target_types)

    def travel_and_update(self, node, prev_ids, prev_types):
        my_idx = id(node)

        if isinstance(node, ast.If) or isinstance(node, ast.While):
            reverse = False

            # Condition stmt of If
            if isinstance(node.test, ast.Compare):
                name = ""
                if isinstance(node.test.ops[0], ast.Eq):
                    name = 'testeq'
                elif isinstance(node.test.ops[0], ast.Gt):
                    name = 'testgt'
                elif isinstance(node.test.ops[0], ast.Lt):
                    name = 'testlt'
                elif isinstance(node.test.ops[0], ast.LtE):
                    name = 'testlte'
                elif isinstance(node.test.ops[0], ast.GtE):
                    name = 'testgte'
                elif isinstance(node.test.ops[0], ast.NotEq):
                    name = 'testne'
                elif isinstance(node.test.ops[0], ast.In):
                    name = 'testin'
                st = ast.Call(func=ast.Name(id=name, ctx=ast.Load()),
                              args=[node.test.left, node.test.comparators[0], ast.Constant(value=my_idx)], keywords=[])
            # Condition stmt of If - and/or/not
            elif isinstance(node.test, ast.BoolOp):
                if isinstance(node.test.op, ast.And) or isinstance(node.test.op, ast.Or):
                    if isinstance(node.test.op, ast.And):
                        big_name = 'testand'
                    elif isinstance(node.test.op, ast.Or):
                        big_name = 'testor'
                    elif isinstance(node.test.op, ast.Not):
                        reverse = True
                    else:
                        NotImplementedError
                    args = []
                    for val in node.test.values:
                        if isinstance(val.ops[0], ast.Eq):
                            name = 'testeq'
                        elif isinstance(val.ops[0], ast.Gt):
                            name = 'testgt'
                        elif isinstance(val.ops[0], ast.Lt):
                            name = 'testlt'
                        elif isinstance(val.ops[0], ast.GtE):
                            name = 'testgte'
                        elif isinstance(val.ops[0], ast.LtE):
                            name = 'testlte'
                        elif isinstance(val.ops[0], ast.NotEq):
                            name = 'testne'
                        st = ast.Call(func=ast.Name(id=name, ctx=ast.Load()),
                                      args=[val.left, val.comparators[0], ast.Constant(value=my_idx),
                                            ast.Constant(value=True)], keywords=[])
                        args.append(st)
                    if not reverse:
                        st = ast.Call(func=ast.Name(id=big_name, ctx=ast.Load()),
                                      args=[args[0], args[1], ast.Constant(value=my_idx)],
                                      keywords=[])

            setattr(node, 'test', st)
            prev_ids = prev_ids[:]
            prev_ids.append(my_idx)
            new_body = []
            trues = prev_types[:]
            if reverse:
                trues.append(1)
            else:
                trues.append(0)
            for i, el in enumerate(node.body):
                new_body.append(self.travel_and_update(el, prev_ids, trues))
            if len(new_body) != 0:
                setattr(node, 'body', new_body)
            new_else = []
            falses = prev_types[:]
            if reverse:
                trues.append(0)
            else:
                falses.append(1)
            for i, el in enumerate(node.orelse):
                new_else.append(self.travel_and_update(el, prev_ids, falses))
            if len(new_else) != 0:
                setattr(node, 'orelse', new_else)
        else:
            update = True
            for field, old_value in ast.iter_fields(node):
                if isinstance(old_value, list):
                    new_values = []
                    for value in old_value:
                        if isinstance(value, ast.AST):
                            value = self.travel_and_update(value, prev_ids, prev_types)
                            update = False
                            if value is None:
                                continue
                            elif not isinstance(value, ast.AST):
                                new_values.extend(value)
                                continue
                        new_values.append(value)
                    old_value[:] = new_values
                elif isinstance(old_value, ast.AST):
                    new_node = self.travel_and_update(old_value, prev_ids, prev_types)
                    update = False
                    if new_node is None:
                        delattr(node, field)
                    else:
                        setattr(node, field, new_node)

            if update:
                info = (prev_ids, prev_types)
                if info not in self.infos and len(prev_ids) != 0:
                    self.infos.append(info)
                    self.target_ids.append(info[0])
                    self.target_types.append(info[1])
        return node

'''
for GA
'''

class Evaluator:
    def __init__(self, setup_content, loop_content):
        self.setup_content = setup_content
        self.loop_content = loop_content

    def fill_user_interactions(self, codons: list):
        loop_content_lines = self.loop_content.strip().split('\n')
        interaction_code = f"""
interaction_seq = {codons}
interactor = machine.UserInteract(interaction_seq)
interactor.start()

while True:"""
        for line in loop_content_lines:
            interaction_code += f"""
    {line}"""
        interaction_code += """
    if not interactor.is_alive():
        break"""
        return interaction_code

    def evaluate(self, codons):
        exec(self.setup_content, globals())

        global fitness
        fitness = [float('inf')] * target_cnt

        loop_code = self.fill_user_interactions(codons)
        exec(loop_code, globals())

        return sum([max(0, f) for f in fitness])


class Solution:
    def __init__(self, sol):
        self.sol = sol
        self.fitness = 0

    def __str__(self) -> str:
        readable = machine.convert_seqs_to_readable(self.sol)
        return f"{readable} with {self.fitness}"


def random_codons(codons_length, num_range) -> list:
    sol = []
    for _ in range(codons_length):
        sol.append((random.randint(num_range[0], num_range[1]), random.randint(num_range[0], num_range[1])))
    return sol


def crossover(rate, p1, p2):
    # one point crossover
    split = random.randrange(len(p1.sol))

    if random.random() < rate:
        # swap for offspring 1
        o1 = Solution(p1.sol[:split] + p2.sol[split:])
        # swap for offspring 2
        o2 = Solution(p2.sol[:split] + p1.sol[split:])
    else:
        o1 = Solution(p1.sol[:])
        o2 = Solution(p2.sol[:])
    return o1, o2


def mutate(rate, s, num_range):
    for i in range(len(s.sol)):
        if random.random() < rate:
            s.sol = s.sol[:i] + [(random.randint(num_range[0], num_range[1]), random.randint(num_range[0], num_range[1]))] + s.sol[i + 1:]
    return s


def select(k, population):
    # we randomly sample k solutions from the population
    participants = random.sample(population, k)
    return sorted(participants, key=lambda x: (x.fitness, x.sol[0][0]), reverse=False)[0]

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
    exec_code(solution.sol)
    cov.stop()

    # Check current coverage
    cov.json_report(outfile="ga/report.json")
    with open("ga/report.json", 'r') as file:
        json_data = json.load(file)

    system_name = platform.system()
    if system_name == 'Darwin':
        summary = json_data["files"][f"converted_codes/{filename}"]["summary"]
    elif system_name == 'Windows':
        summary = json_data["files"][f"converted_codes\\{filename}"]["summary"]
    else:
        NotImplementedError("Only Darwin & Windows..")

    curr_coverage = min((int(summary["covered_lines"]) + 1) / int(summary['num_statements']) * 100, 100)
    os.remove("ga/report.json")

    cov.html_report(directory=f"ga/html_{curr_coverage}")  # for inspection
    cov.erase()

    return curr_coverage

def ga(filename, evaluator, ui_length, pp_size):
    population = []
    MAX_NUM = 2048
    for _ in range(pp_size):
        s = Solution(random_codons(ui_length, (0, MAX_NUM)))
        s.fitness = evaluator.evaluate(s.sol)
        population.append(s)
        if s.fitness == 0:
            break
    count = 0
    budget = 100  # number of generations
    population = sorted(population, key=lambda x: (x.fitness, x.sol[0][0]), reverse=False)
    best_solution = population[0]
    print(f"best sol in initial population: {best_solution}")

    while count < budget and best_solution.fitness > 0:
        next_gen = []
        while len(next_gen) < len(population):
            # selecting the fitter parents
            p1 = select(int(pp_size*0.2), population)
            p2 = select(int(pp_size*0.2), population)

            # crossover to generate a pair of offsprings
            o1, o2 = crossover(0.9, p1, p2)

            # mutate the offsprings
            o1 = mutate(0.1, o1, (0, MAX_NUM))
            o2 = mutate(0.1, o2, (0, MAX_NUM))
            o1.fitness = evaluator.evaluate(o1.sol)
            o2.fitness = evaluator.evaluate(o2.sol)
            next_gen.append(o1)
            next_gen.append(o2)

        # now we have the full next gen
        population.extend(next_gen)
        population = sorted(population, key=lambda x: (x.fitness, x.sol[0][0]), reverse=False)
        population = population[:pp_size]
        best_solution = population[0]
        print(count, best_solution)
        count += 1

    curr_coverage = calculate_coverage(filename, best_solution)

    return best_solution, count, curr_coverage


'''
branch condition functions
'''
k = 0.0000001

def testeq(l, r, node_idx, ret_bd=False):
    global fitness
    if ret_bd:
        als = [0] * target_cnt
        bds = [0] * target_cnt
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            if direction == 0:
                bd = abs(l - r)
            else:
                bd = -abs(l - r)
            if ret_bd:
                als[index] = al
                bds[index] = bd
            else:
                fitness_i = al + (1 - 1.001 ** (-bd))
                if direction != 0:
                    fitness_i += k
                if fitness_i < fitness[index]:
                    fitness[index] = fitness_i
    
    if not ret_bd:
        return l == r
    else:
        return l == r, als, bds

def testin(l, r, node_idx, ret_bd=False):
    global fitness, interactor
    if ret_bd:
        als = [0] * target_cnt
        bds = [0] * target_cnt
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            dists = [abs(l - ref) for ref in r]
            if direction == 0:
                bd = min(dists)
            else:
                bd = -min(dists)
            if ret_bd:
                als[index] = al
                bds[index] = bd
            else:
                fitness_i = al + (1 - 1.001 ** (-bd))
                if fitness_i < fitness[index]:
                    fitness[index] = fitness_i
    interactor.timer_lock.release()
    if not ret_bd:
        return l in r
    else:
        return l in r, als, bds

def testne(l, r, node_idx, ret_bd=False):
    global fitness
    if ret_bd:
        als = [0] * target_cnt
        bds = [0] * target_cnt
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            if direction == 0:
                bd = -abs(l - r)
            else:
                bd = abs(l - r)
            if ret_bd:
                als[index] = al
                bds[index] = bd
            else:
                fitness_i = al + (1 - 1.001 ** (-bd))
                if direction == 0:
                    fitness_i += k
                if fitness_i < fitness[index]:
                    fitness[index] = fitness_i
    if not ret_bd:
        return l != r
    else:
        return l != r, als, bds

def testgte(l, r, node_idx, ret_bd=False):
    global fitness
    if ret_bd:
        als = [0] * target_cnt
        bds = [0] * target_cnt
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            if direction == 0:
                bd = r - l + k
            else:
                bd = l - r + k
            if ret_bd:
                als[index] = al
                bds[index] = bd
            else:
                fitness_i = al + (1 - 1.001 ** (-bd))
                if direction != 0:
                    fitness_i += k
                if fitness_i < fitness[index]:
                    fitness[index] = fitness_i
    if not ret_bd:
        return l >= r
    else:
        return l >= r, als, bds

def testlte(l, r, node_idx, ret_bd=False):
    global fitness
    if ret_bd:
        als = [0] * target_cnt
        bds = [0] * target_cnt
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            if direction == 0:
                bd = l - r + k
            else:
                bd = r - l + k
            if ret_bd:
                als[index] = al
                bds[index] = bd
            else:
                fitness_i = al + (1 - 1.001 ** (-bd))
                if direction != 0:
                    fitness_i += k
                if fitness_i < fitness[index]:
                    fitness[index] = fitness_i
    if not ret_bd:
        return l <= r
    else:
        return l <= r, als, bds

def testgt(l, r, node_idx, ret_bd=False):
    global fitness
    if ret_bd:
        als = [0] * target_cnt
        bds = [0] * target_cnt
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            if direction == 0:
                bd = r - l + k
            else:
                bd = l - r + k
            if ret_bd:
                als[index] = al
                bds[index] = bd
            else:
                fitness_i = al + (1 - 1.001 ** (-bd))
                if direction == 0:
                    fitness_i += k
                if fitness_i < fitness[index]:
                    fitness[index] = fitness_i
    if not ret_bd:
        return l > r
    else:
        return l > r, als, bds

def testlt(l, r, node_idx, ret_bd=False):
    global fitness
    if ret_bd:
        als = [0] * target_cnt
        bds = [0] * target_cnt
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            if direction == 0:
                bd = l - r + k
            else:
                bd = r - l + k
            if ret_bd:
                als[index] = al
                bds[index] = bd
            else:
                fitness_i = al + (1 - 1.001 ** (-bd))
                if direction == 0:
                    fitness_i += k
                if fitness_i < fitness[index]:
                    fitness[index] = fitness_i
    if not ret_bd:
        return l < r
    else:
        return l < r, als, bds

def testand(l_info, r_info, node_idx):
    global fitness
    l, l_als, l_bds = l_info
    r, r_als, r_bds = r_info
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            if direction == 0:
                # should be all true
                bd = max(l_bds[index], 0) + max(r_bds[index], 0)
                # max(l_bd, r_bd)
            else:
                # at least one false
                bd = min(l_bds[index], r_bds[index])
            fitness_i = l_als[index] + (1 - 1.001 ** (-bd))
            if fitness_i < fitness[index]:
                fitness[index] = fitness_i
    return l and r

def testor(l_info, r_info, node_idx):
    global fitness
    l, l_als, l_bds = l_info
    r, r_als, r_bds = r_info
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            if direction == 0:
                # should be at least one true
                bd = min(l_bds[index], r_bds[index])
                # max(l_bd, r_bd)
            else:
                # should be all false
                bd = max(l_bds[index], 0) + max(r_bds[index], 0)
            fitness_i = l_als[index] + (1 - 1.001 ** (-bd))
            if fitness_i < fitness[index]:
                fitness[index] = fitness_i
    return l or r

'''
Seperate the whold code -> initial / setup / loop
Get GA targets
'''
def seperate_code(filename, code):
    tree = ast.parse(code)

    initial_tree = ast.parse("")
    setup_tree = ast.parse("")
    loop_tree = ast.parse("")
    
    initial_settings = f'''
import os
import sys
parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.join(parent_dir, 'simulator'))
import machine'''
    initial_tree.body.append(ast.parse(initial_settings))

    for index, node in enumerate(tree.body):
        if isinstance(node, ast.Import) and node.names[0].name == "machine":
            continue
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            initial_tree.body.append(node)
        else:
            break

    initial_content = ast.unparse(initial_tree)

    for index2, node in enumerate(tree.body[index:]):
        if isinstance(node, ast.While):
            break
        ast.copy_location(node, setup_tree)
        setup_tree.body.append(node)

    for _, node in enumerate(tree.body[index+index2:]):
        nodes = codeNodes()
        new_bodies = []
        for i, el in enumerate(node.body):
            new_bodies.append(nodes.travel_and_update(el, [], []))
        node.body = new_bodies # if문의 body에 다시 넣어주기
        # unparse_content = ast.unparse(tree)
        for inner_node in node.body:
            ast.copy_location(inner_node, loop_tree)
            loop_tree.body.append(inner_node)

    loop_content = ast.unparse(loop_tree)

    setup_content = f'''
machine.load_board("{filename}")
target_cnt = {len(nodes.target_ids)}
target_ids = {nodes.target_ids}
target_types = {nodes.target_types}
'''
    setup_content += ast.unparse(setup_tree)

    return initial_content, setup_content, loop_content

# usage: python ga/sbst.py {filename} --p {pp_size} --l {ui_length}
if __name__ == "__main__":
    parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    sys.path.append(parent_dir)

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the python file to check baseline coverage")
    parser.add_argument("--p", type=int, help="GA population size")
    parser.add_argument("--l", type=int, help="user interaction sequence length to randomly generate")
    parser.add_argument("--r", type=int, help="random seed")
    
    args = parser.parse_args()
    random.seed(args.r)

    with open(f"target_codes/{args.filename}", "r") as f:
        code = f.read()
    
    initial_content, setup_content, loop_content = seperate_code(args.filename, code)

    # save targets and target_cnt(# of target) as global variables
    exec(initial_content, globals())

    evaluator = Evaluator(
                    setup_content=setup_content,
                    loop_content=loop_content
    )

    start = time.time()
    best_solution, generations, max_coverage = ga(args.filename, evaluator, args.l, args.p)
    end = time.time()
    
    print("result: ", best_solution, "done.")

    # save coverage
    content_to_write = f'''
Coverage Result for {args.filename} (with ui_length = {args.l}, population_size = {args.p})
    - Generations needed to achieve 100% coverage : { "-" if generations==100 else generations}
    - Max Coverage % until 100 generations: {max_coverage:.2f}%
    - Total Execution Time: {end - start:.5f} sec
    - Best Test Case: {best_solution}
        
'''
    print([args.filename, args.l, args.p, args.r, generations, max_coverage, end - start])
    with open("ga/result.txt", 'a') as file:
        file.write(content_to_write)

    with open(f"ga/result_{args.filename}.csv", "a") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([args.filename, args.l, args.p, args.r, generations, max_coverage, end - start])

    print(content_to_write)
