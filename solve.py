from z3 import *
from pprint import pprint
import operator

operations = {
        '=='  : operator.eq,
        '!=' : operator.ne,
        '<'  : operator.lt,
        '<=' : operator.le,
        '>'  : operator.gt,
        '>=' : operator.ge,
}


builtins = {
        'distinct': Distinct,
        'assert': lambda x: x,
        'noteq': lambda x: x,
}

class BinOp:
    def __init__(self, operator, operand1, operand2):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2

def make_board_constraint(z3board, board):
    return [ If(board[i][j] == 0,
                True,
                z3board[i][j] == board[i][j])
            for i in range(9) for j in range(9)]

def get_point_lists(offsets, start_point=None):
    if start_point:
        point_list = [start_point]
        for offset in offsets:
            x = start_point[0] + offset[0]
            y = start_point[1] + offset[1]
            if 0 <= x < 9 and 0 <= y < 9:
                point_list.append((start_point[0]+offset[0], start_point[1]+offset[1]))
        return [point_list]

    point_lists = []
    points = [(x,y) for x in range(9) for y in range(9)]
    for point in points:
        point_list = [point]
        for offset in offsets:
            x = point[0] + offset[0]
            y = point[1] + offset[1]
            if 0 <= x < 9 and 0 <= y < 9:
                point_list.append((point[0]+offset[0], point[1]+offset[1]))
        point_lists.append(point_list)
    return point_lists

def apply_point_list(board, point_list):
    z3list = []
    for point in point_list:
        z3list.append(board[point[0]][point[1]])
    return z3list

def get_binop_constraint(board, groups, variables, function, group):
    op1 = group.operand1
    op2 = group.operand2
    op = operations[group.operator]

    assert (op1 in groups) ^ (op2 in groups)

    if op1 in groups:
        func = lambda x: map(lambda y: op(y, op2), x)
        offsets = groups[op1]
    else:
        func = lambda x: map(lambda y: op(op1, y), x)
        offsets = groups[op2]

    start_point = None
    if isinstance(offsets, tuple):
        start_point = offsets[0]
        offsets = offsets[1]
    point_lists = get_point_lists(offsets, start_point)

    constraints = []

    for pl in point_lists:
        pl = apply_point_list(board, pl)
        pl = func(pl)
        if isinstance(pl, map):
            pl = list(pl)
        constraints.append(pl)
    return constraints

def get_noteq_constraint(board, groups, variables, function, group):
    offsets = groups[group]
    start_point = None
    if isinstance(offsets, tuple):
        start_point = offsets[0]
        offsets = offsets[1]

    point_lists = get_point_lists(offsets, start_point)

    constraints = []

    for pl in point_lists:
        pl = apply_point_list(board, pl)
        point = pl[0]
        points = pl[1:]
        pl = map(lambda x: x != point, points)
        if isinstance(pl, map):
            pl = list(pl)
        constraints.append(pl)
    return constraints

def solve(groups, variables, script_constraints):
    #print("In solve")

    instance = variables['instance']
    x,y = len(instance[0]), len(instance)
    board = [[Int(f'x_{i}_{j}') for j in range(x)] for i in range(y)]
    board_constraint = make_board_constraint(board, variables['instance'])

    constraints = []

    for function, group in script_constraints:
        #print(f"Applying {function} to {group}")
        if isinstance(group, BinOp):
            binop_constraint = get_binop_constraint(board, groups, variables, function, group)
            constraints += binop_constraint
            continue

        if function == "noteq":
            noteq_constraint = get_noteq_constraint(board, groups, variables, function, group)
            constraints += noteq_constraint
            continue

        func = builtins[function]
        offsets = groups[group]
        start_point = None
        if type(offsets) == tuple:
            start_point = offsets[0]
            offsets = offsets[1]
        point_lists = get_point_lists(offsets, start_point)
        for pl in point_lists:
            pl = apply_point_list(board, pl)
            pl = func(pl)
            if type(pl) == map:
                pl = list(pl)
            constraints.append(pl)

    s = Solver()
    s.add(board_constraint)
    for c in constraints:
        s.add(c)

    if s.check() == sat:
        m = s.model()
        r = [[m.evaluate(board[i][j]) for j in range(9)] for i in range(9)]
        pprint(r)
    else:
        print("Unsat")
