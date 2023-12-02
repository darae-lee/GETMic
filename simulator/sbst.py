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
        return node

'''
for GA
'''

class Evaluator:
    def __init__(self, setup_content, loop_content, loop_count):
        self.setup_content = setup_content
        self.loop_content = loop_content
        self.loop_count = loop_count

    def fill_user_interactions(self, codons: list):
        loop_content_lines = self.loop_content.strip().split('\n')
        interaction_code = f"""
interaction_seq = {codons}
interactor = UserInteract(interaction_seq)
interactor.start()

for _ in range({self.loop_count}):"""
        for line in loop_content_lines:
            interaction_code += f"""
    {line}"""
        return interaction_code

    def evaluate(self, codons):        
        exec(self.setup_content, globals())

        global fitness
        fitness = [float('inf')] * target_cnt

        global als
        als = [0] * target_cnt

        loop_code = self.fill_user_interactions(codons)
        
        exec(loop_code, globals())

        return sum([max(0, f) for f in fitness])


class Solution:
    def __init__(self, sol):
        self.sol = sol
        self.fitness = 0

    def __str__(self) -> str:
        return f"{', '.join([str(x) for x in self.sol])} with {self.fitness}"


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
    return sorted(participants, key=lambda x: x.fitness, reverse=False)[0]


def ga(codon_length, evaluator):
    population = []
    MAX_NUM = 2048  # TODO: 최대값 정하기
    for i in range(100):
        s = Solution(random_codons(codon_length, (0, MAX_NUM)))
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
        print(count, best_solution)
        count += 1
    return best_solution


'''
branch condition functions
'''
k = 1

# ret_bd=True면 and/or

def testeq(l, r, node_idx, ret_bd=False):
    global fitness
    if ret_bd:
        global als
        bds = [0] * target_cnt
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            if ret_bd:
                als[index] = al
            if direction == 0:
                bd = abs(l - r)
            else:
                bd = -abs(l - r)
            if ret_bd:
                bds[index] = bd
            else:
                fitness_i = al + (1 - 1.001 ** (-bd))
                if fitness_i < fitness[index]:
                    fitness[index] = fitness_i

    if not ret_bd:
        return l == r
    else:
        return l == r, bds

def testin(l, r, node_idx, ret_bd=False):
    global fitness
    if ret_bd:
        global als
        bds = [0] * target_cnt
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            if ret_bd:
                als[index] = al
            dists = [abs(l - ref) for ref in r]
            if direction == 0:
                bd = min(dists)
            else:
                bd = -min(dists)
            if ret_bd:
                bds[index] = bd
            else:
                fitness_i = al + (1 - 1.001 ** (-bd))
                if fitness_i < fitness[index]:
                    fitness[index] = fitness_i
    if not ret_bd:
        return l in r
    else:
        return l in r, bds

def testne(l, r, node_idx, ret_bd=False):
    global fitness
    if ret_bd:
        global als
        bds = [0] * target_cnt
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            if ret_bd:
                als[index] = al
            if direction == 0:
                bd = -abs(l - r)
            else:
                bd = abs(l - r)
            if ret_bd:
                bds[index] = bd
            else:
                fitness_i = al + (1 - 1.001 ** (-bd))
                if fitness_i < fitness[index]:
                    fitness[index] = fitness_i
    if not ret_bd:
        return l != r
    else:
        return l != r, bds

def testgte(l, r, node_idx, ret_bd=False):
    global fitness
    if ret_bd:
        global als
        bds = [0] * target_cnt
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            if ret_bd:
                als[index] = al
            if direction == 0:
                bd = r - l + k
            else:
                bd = l - r + k
            if ret_bd:
                bds[index] = bd
            else:
                fitness_i = al + (1 - 1.001 ** (-bd))
                if fitness_i < fitness[index]:
                    fitness[index] = fitness_i
    if not ret_bd:
        return l >= r
    else:
        return l >= r, bds

def testlte(l, r, node_idx, ret_bd=False):
    global fitness
    if ret_bd:
        global als
        bds = [0] * target_cnt
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            if ret_bd:
                als[index] = al
            if direction == 0:
                bd = l - r + k
            else:
                bd = r - l + k
            if ret_bd:
                bds[index] = bd
            else:
                fitness_i = al + (1 - 1.001 ** (-bd))
                if fitness_i < fitness[index]:
                    fitness[index] = fitness_i
    if not ret_bd:
        return l <= r
    else:
        return l <= r, bds

def testgt(l, r, node_idx, ret_bd=False):
    global fitness
    if ret_bd:
        global als
        bds = [0] * target_cnt
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            if ret_bd:
                als[index] = al
            if direction == 0:
                bd = r - l + k
            else:
                bd = l - r + k
            if ret_bd:
                bds[index] = bd
            else:
                fitness_i = al + (1 - 1.001 ** (-bd))
                if fitness_i < fitness[index]:
                    fitness[index] = fitness_i
    if not ret_bd:
        return l > r
    else:
        return l > r, bds

def testlt(l, r, node_idx, ret_bd=False):
    global fitness
    if ret_bd:
        global als
        bds = [0] * target_cnt
    for index in range(target_cnt):
        if node_idx in target_ids[index]:
            cur_pos = target_ids[index].index(node_idx)
            direction = target_types[index][cur_pos]
            al = len(target_ids[index]) - cur_pos - 1
            if ret_bd:
                als[index] = al
            if direction == 0:
                bd = l - r + k
            else:
                bd = r - l + k
            if ret_bd:
                bds[index] = bd
            else:
                fitness_i = al + (1 - 1.001 ** (-bd))
                if fitness_i < fitness[index]:
                    fitness[index] = fitness_i
    if not ret_bd:
        return l < r
    else:
        return l < r, bds

def testand(l_info, r_info, node_idx):
    global fitness, als
    l, l_bds = l_info
    r, r_bds = r_info
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
            fitness_i = als[index] + (1 - 1.001 ** (-bd))
            if fitness_i < fitness[index]:
                fitness[index] = fitness_i
    return l and r

def testor(l_info, r_info, node_idx):
    global fitness, als
    l, l_bds = l_info
    r, r_bds = r_info
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
            fitness_i = als[index] + (1 - 1.001 ** (-bd))
            if fitness_i < fitness[index]:
                fitness[index] = fitness_i
    return l or r

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
    global al, bd
    random.seed(0)
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="the target python file to generate unit tests for")
    args = parser.parse_args()

    with open(args.target, "r") as f:
        code = f.read()
    
    # code = erase_sleep(code)  # sleep하는 코드 지우기
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
    
    ast.fix_missing_locations(load_board_node)
    initial_tree.body.append(load_board_node)

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

    setup_content = f'''
target_cnt = {len(nodes.target_ids)}
target_ids = {nodes.target_ids}
target_types = {nodes.target_types}
'''
    setup_content += ast.unparse(setup_tree)

    initial_content = ast.unparse(initial_tree)
    loop_content = ast.unparse(loop_tree)

    print("-----initial-----")
    print(initial_content)
    print("-----setup-----")
    print(setup_content)
    print("-----loop-----")
    print(loop_content)
    print("----------")

    #
    exec(initial_content, globals())

    # 가능한 user interaction 가져오기
    objects = machine.HW_board.objects
    actions_per_object = machine.HW_board.action_per_object
    # print(objects)
    # print(actions_per_object)

    objects_cnt = len(objects)
    actions_cnt = [len(actions) for actions in actions_per_object]
    loop_count = 5

    evaluator = Evaluator(
                    setup_content=setup_content,
                    loop_content=loop_content,
                    loop_count=100 # loop 몇 번 돌건지
    )
    
    codon_length = 500
    result = ga(codon_length, evaluator)
    # result = ga(loop_count, space_number, evaluator)
    print("result: ", result, "done.")
