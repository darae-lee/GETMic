import grammar
import random
import argparse
import ast
import os

class codeNodes:
    def __init__(self):
        self.target_ids = []
        self.target_types = []
        self.infos = [] #(target_ids, target_types)
        self.values = [] #(al, bd)

    def travel_and_update(self, node, prev_ids, prev_types):
        my_idx = id(node)

        if isinstance(node, ast.If) or isinstance(node, ast.While):
            reverse = False
            # if문 안의 if
            # if isinstance(node.test, ast.IfExp):
            #     test_true = eval(ast.unparse(node.test.body))
            #     test_false = eval(ast.unparse(node.test.orelse))
            #     if (bool(test_true) is True) and (bool(test_false) is False):
            #         setattr(node, 'test', node.test.test)
            #     elif (bool(test_true) is True) and (bool(test_false) is False):
            #         reverse = True
            #         setattr(node, 'test', node.test.test)

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
                    self.values.append([1000,1000])
        return node

'''
for GA
'''

class Evaluator:
    def __init__(self, setup_content, loop_content, productions, loop_count, local_count):
        self.setup_content = setup_content
        self.loop_content = loop_content
        self.productions = productions
        self.productions_length = len(productions)
        self.loop_count = loop_count
        self.local_count = local_count

    def get_phenotype(self, codon: int) -> str:
        return self.productions[codon % self.productions_length]

    def fill_user_interactions(self, codons: list):
        interactions = [self.get_phenotype(codon) for codon in codons]
        idx = 0  # idx of interactions
        new_lines = []
        # start_insert = False
        lines = self.loop_content.split("\n")
        for line in lines:
            # if start_insert:
            if line.strip().startswith("else") or line.strip().startswith("elif"):
                new_lines.append(indentation + interactions[idx] + '\n')
                idx += 1
            else:
                indentation = line[:len(line) - len(line.lstrip())]
                new_lines.append(indentation + interactions[idx] + '\n')
                idx += 1
            # elif line.strip().startswith("if True"):
            #     start_insert = True
            new_lines.append(line + '\n')
        last_line = lines[-1]
        indentation = last_line[:len(last_line) - len(last_line.lstrip())]
        new_lines.append(indentation + interactions[idx] + '\n')
        return "".join(new_lines)

    def evaluate(self, codons):
        exec(self.setup_content, globals())

        fitness = [float('inf')] * target_cnt
        for loop_idx in range(self.loop_count):
            local_codons = codons[loop_idx*self.local_count : (loop_idx+1)*self.local_count]
            local_code = self.fill_user_interactions(local_codons)
            
            exec(local_code, globals())

            for index, f in enumerate(values):
                al, bd = f[0], f[1]
                fitness_i = al + (1 - 1.001 ** (-bd))
                if fitness_i < fitness[index]:
                    fitness[index] = fitness_i

        return sum(fitness)


class Solution:
    def __init__(self, sol):
        self.sol = sol
        self.fitness = 0

    def __str__(self) -> str:
        return f"{', '.join([str(x) for x in self.sol])} with {self.fitness}"


def random_codons(codons_length, num_range) -> list:
    sol = []
    for i in range(codons_length):
        sol.append(random.randint(num_range[0], num_range[1]))
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
            s.sol = s.sol[:i] + [random.randint(num_range[0], num_range[1])] + s.sol[i + 1:]
    return s


def select(k, population):
    # we randomly sample k solutions from the population
    participants = random.sample(population, k)
    return sorted(participants, key=lambda x: x.fitness, reverse=False)[0]


def ga(loop_number, space_number, evaluator):
    population = []
    MAX_NUM = 2048  # TODO: 최대값 정하기
    for i in range(100):
        s = Solution(random_codons(loop_number*space_number, (0, MAX_NUM)))
        s.fitness = evaluator.evaluate(s.sol)
        population.append(s)
    count = 0
    budget = 100  # number of generations
    best_solution = population[0]
    while count < budget and best_solution.fitness > 0:
        next_gen = []
        while len(next_gen) < len(population):
            # selecting the fitter parents
            p1 = select(20, population)
            p2 = select(20, population)

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
        population = sorted(population, key=lambda x: x.fitness, reverse=False)
        population = population[:50]  # regardless of generation, keep top 50s
        best_solution = population[0]
        count += 1
    return best_solution


'''
branch condition functions
'''
k = 1

def testeq(l, r, node_idx, ret_bd=False):
    global values
    for index in range(target_cnt):
        al, bd = values[index]
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            values[index][0] = al
            if direction == 0:
                bd = abs(l - r)
            else:
                bd = -abs(l - r)
        values[index][1] = bd
    return l == r

def testin(l, r, node_idx, ret_bd=False):
    global values
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            values[index][0] = al
            dists = [abs(l - ref) for ref in r]
            if direction == 0:
                bd = min(dists)
            else:
                bd = -min(dists)
        values[index][1] = bd
    return l in r

def testne(l, r, node_idx, ret_bd=False):
    global values
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            values[index][0] = al
            if direction == 0:
                bd = -abs(l - r)
            else:
                bd = abs(l - r)
        values[index][1] = bd
    return l != r

def testgte(l, r, node_idx, ret_bd=False):
    global values
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            values[index][0] = al
            if direction == 0:
                bd = r - l + k
            else:
                bd = l - r + k
        values[index][1] = bd
    return l >= r

def testlte(l, r, node_idx, ret_bd=False):
    global values
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            values[index][0] = al
            if direction == 0:
                bd = l - r + k
            else:
                bd = r - l + k
        values[index][1] = bd
    return l <= r

def testgt(l, r, node_idx, ret_bd=False):
    global values
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            values[index][0] = al
            if direction == 0:
                bd = r - l + k
            else:
                bd = l - r + k
        values[index][1] = bd
    return l > r

def testlt(l, r, node_idx, ret_bd=False):
    global values
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            values[index][0] = al
            if direction == 0:
                bd = l - r + k
            else:
                bd = r - l + k
        values[index][1] = bd
    return l < r

def testand(l_info, r_info, node_idx):
    global values
    for index in range(target_cnt):
        l, l_bd = l_info
        r, r_bd = r_info
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            if direction == 0:
                # should be all true
                bd = max(l_bd, 0) + max(r_bd, 0)
                # max(l_bd, r_bd)
            else:
                # at least one false
                bd = min(l_bd, r_bd)
            values[index][1] = bd
            return l and r
        else:
            return l and r

def testor(l_info, r_info, node_idx):
    global values
    for index in range(target_cnt):
        l, l_bd = l_info
        r, r_bd = r_info
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            if direction == 0:
                # should be at least one true
                bd = min(l_bd, r_bd)
                # max(l_bd, r_bd)
            else:
                # should be all false
                bd = max(l_bd, 0) + max(r_bd, 0)
            values[index][1] = bd
            return l or r
        else:
            return l or r


def erase_sleep(code):
    lines = []
    for line in code.split("\n"):
        if line == "import utime" or line.strip().startswith("utime.sleep"):
            continue
        else:
            lines.append(line)
    return "\n".join(lines) + "\n"

'''
Count # of space where user interaction can be inserted
'''
def count_space(code):
    inside_while = False
    inside_comment = False
    space_count = 0
    for line in code.split("\n"):
        if inside_while:
            stripped_line = line.strip()
            if stripped_line.startswith("'''") or stripped_line.startswith('"""'):
                inside_comment = not inside_comment
            if not (stripped_line.startswith('#') or stripped_line == '') and not inside_comment:
                space_count += 1
        elif line.strip().startswith("while True"):
            inside_while = 1
            continue
    space_count += 1
    return space_count

# usage: python sbst.py target_codes/{}.py
if __name__ == "__main__":
    global values
    global al, bd
    random.seed(0)
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="the target python file to generate unit tests for")
    args = parser.parse_args()

    with open(args.target, "r") as f:
        code = f.read()
    
    code = erase_sleep(code)  # sleep하는 코드 지우기
    space_number = count_space(code)  # codons의 길이 계산
    tree = ast.parse(code)

    '''
    Get targets & Testcase generation for each target with GA
    '''

    # setup, loop 분리
    initial_tree = ast.parse("")
    setup_tree = ast.parse("")
    loop_tree = ast.parse("")

    for index, node in enumerate(tree.body):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            initial_tree.body.append(node)
        else:
            break
    
    initial_tree.body.append(ast.Import(names=[ast.alias(name='machine')]))
    initial_tree.body.append(ast.ImportFrom(module='machine', names=[ast.alias(name='UserInteract')], level=0))
    load_board_node = ast.Expr(
                        value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id='machine', ctx=ast.Load()),
                                attr='load_board',
                                ctx=ast.Load()),
                            args=[
                                ast.Name(id="\""+args.target+"\"", ctx=ast.Load())],
                            keywords=[]))
    
    interactor_node = ast.Assign(
                        targets=[
                            ast.Name(id='interactor', ctx=ast.Store())],
                        value=ast.Call(
                            func=ast.Name(id='UserInteract', ctx=ast.Load()),
                            args=[],
                            keywords=[])
                        )
    ast.fix_missing_locations(load_board_node)
    initial_tree.body.append(load_board_node)
    ast.fix_missing_locations(interactor_node)
    initial_tree.body.append(interactor_node)

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

    print(f"nodes.infos: {nodes.infos}")
    print(f"nodes.target_ids: {nodes.target_ids}")
    print(f"nodes.target_types: {nodes.target_types}")
    print(f"nodes.values: {nodes.values}")
    values = nodes.values # list of [al, bd]

    setup_content = f'''
target_cnt = {len(nodes.target_ids)}
target_ids = {nodes.target_ids}
target_types = {nodes.target_types}
'''
    setup_content += ast.unparse(setup_tree)

    initial_content = ast.unparse(initial_tree)
    loop_content = ast.unparse(loop_tree)

    #
    exec(initial_content, globals())

    exec(setup_content, globals())

    # 가능한 user interaction 가져오기
    user_interactions = interactor.codes
    interaction_cnt = len(user_interactions)
    productions = [f"interactor.interact({num})" for num in range(interaction_cnt)]
    loop_count = 3
    print("user interaction cnt: ", interaction_cnt)
    print("------------")
    print("setup content: ", setup_content)
    print("------------")
    print("loop content: ", ast.unparse(loop_tree))
    print("------------")
    print("productions: ", productions)
    print("============")

    evaluator = Evaluator(
                    setup_content=setup_content,
                    loop_content=loop_content,
                    productions=productions,
                    loop_count=loop_count, # loop 몇 번 돌건지
                    local_count=space_number, # local action 개수
    )
    
    result = ga(loop_count, space_number, evaluator)
    print("result: ", result, "done.")
