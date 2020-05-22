import solve
import operator

groups = {}
variables = {}
constraints = []

def flatten(L):
    if len(L) < 2: return L
    return [L[0]] + flatten(L[1])

def apply_func(func, param):
    constraints.append((func, param))

def execute(ast):
    if not isinstance(ast, tuple):
        return ast

    if ast[0] == 'Statements':
        execute(ast[1])
        return execute(ast[2])

    if ast[0] == 'Statement':
        return execute(ast[1])

    if ast[0] == 'List':
        return flatten(execute(ast[1]))

    if ast[0] == 'ListItems':
        return [execute(ast[1]), execute(ast[2])]

    if ast[0] == 'ListItem':
        return [execute(ast[1])]

    if ast[0] == 'NullListItem':
        return []

    if ast[0] == 'Group':
        groups[ast[1]] = execute(ast[2])
        return groups[ast[1]]

    if ast[0] == 'Point':
        return (ast[1], ast[2])

    if ast[0] == 'GroupListWithPoint':
        return (execute(ast[1]), flatten(execute(ast[2])))

    if ast[0] == 'GroupListWithoutPoint':
        return flatten(execute(ast[1]))

    if ast[0] == 'GroupItems':
        return [execute(ast[1]), execute(ast[2])]

    if ast[0] == 'GroupItem':
        return (ast[1], ast[2])

    if ast[0] == 'NullGroupItem':
        return []

    if ast[0] == 'NumToExpr':
        return int(ast[1])

    if ast[0] == 'Assign':
        variables[ast[1]] = execute(ast[2])
        return variables[ast[1]]

    if ast[0] == 'IDToExpr':
        return execute(ast[1])

    if ast[0] == 'BinOp':
        operator = ast[1]
        operand1 = execute(ast[2])
        operand2 = execute(ast[3])
        return solve.BinOp(operator, operand1, operand2)

    if ast[0] == 'FunctionCall':
        return apply_func(ast[1], execute(ast[2]))

    if ast[0] == 'Solve':
        # print("Solving")
        # print(groups)
        # print(variables)
        # print(constraints)
        solve.solve(groups, variables, constraints)
        return

    print(f"Unexpected node {ast}")
