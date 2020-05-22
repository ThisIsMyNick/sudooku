from tokens import tokens

# def p_state_expr(p):
#     '''statement : expression'''
#     p[0] = ('Statement', p[1])

def p_state_state(p):
    '''statement : statement statement'''
    p[0] = ('Statements', p[1], p[2])

#Lists

def p_expr_list(p):
    '''expression : LBRACKET list-items RBRACKET'''
    p[0] = ('List', p[2])

def p_listitems(p):
    '''list-items : expression COMMA list-items'''
    p[0] = ('ListItems', p[1], p[3])

def p_listitem(p):
    '''list-items : expression'''
    p[0] = ('ListItem', p[1])

def p_listitems_null(p):
    '''list-items : '''
    p[0] = ('NullListItems',)

# def p_expr_listindex(p):
#     '''expression : expression LBRACKET expression RBRACKET'''
#     p[0] = ('ListIndex', p[1], p[3])

#Definitions

def p_define_group(p):
    '''statement : EQ ID group-list'''
    p[0] = ('Group', p[2], p[3])

def p_group_list(p):
    '''group-list : LBRACE group-items RBRACE
                  | LBRACE point COLON group-items RBRACE'''
    if p[3] == ':':
        p[0] = ('GroupListWithPoint', p[2], p[4])
    else:
        p[0] = ('GroupListWithoutPoint', p[2])

def p_group_point(p):
    '''point : NUM COMMA NUM'''
    p[0] = ('Point', p[1], p[3])

def p_group_items(p):
    '''group-items : group-item COMMA group-items'''
    p[0] = ('GroupItems', p[1], p[3])

def p_group_item(p):
    '''group-item : PLUS NUM DOT PLUS NUM
                  | PLUS NUM DOT MINUS NUM
                  | MINUS NUM DOT PLUS NUM
                  | MINUS NUM DOT MINUS NUM'''
    num1 = p[2]
    num2 = p[5]
    if p[1] == '-': num1 = -num1
    if p[4] == '-': num2 = -num2
    p[0] = ('GroupItem', num1, num2)

def p_group_item_null(p):
    '''group-items : '''
    p[0] = ('NullGroupItem',)

#Constraints

def p_add_constraint(p):
    '''statement : PLUS ID LPAREN expression RPAREN'''
    p[0] = ('FunctionCall', p[2], p[4])

def p_expr_id(p):
    '''expression : ID'''
    p[0] = ('IDToExpr', p[1])

#Binary

def p_expr_binop(p):
    '''expression : expression DEQ expression
                  | expression NE expression
                  | expression GT expression
                  | expression GE expression
                  | expression LT expression
                  | expression LE expression'''
    p[0] = ('BinOp', p[2], p[1], p[3])

#General

def p_expr_num(p):
    '''expression : NUM'''
    p[0] = ('NumToExpr', p[1])

def p_assign(p):
    '''statement : ID EQ expression'''
    p[0] = ('Assign', p[1], p[3])

def p_solve(p):
    '''statement : SOLVE'''
    p[0] = ('Solve',)

#Error

def p_error(p):
    if p:
        print(f'Syntax error at {p.value} in line {p.lineno}')
