import ply.lex as lex
import ply.yacc as yacc


class FunctionNode:
    def __init__(self, function_name, argument_list):
        self.function_name = function_name
        self.argument_list = argument_list

    def evaluate(self, function_map):
        return function_map[self.function_name](*self.argument_list)

    def __repr__(self):
        return f'func {self.function_name} {self.argument_list}'


class BinaryOpNode:
    def __init__(self, lvalue, operation, rvalue):
        self.lvalue = lvalue
        self.operation = operation
        self.rvalue = rvalue

    def evaluate(self):
        lvalue = self.lvalue.evaluate()
        rvalue = self.rvale.evaluate()

        if self.operation == 'AND':
            return lvalue and rvalue
        elif self.operation == 'OR':
            return lvalue or rvalue
        elif self.operation == 'LTE':
            return lvalue <= rvalue
        elif self.operation == 'GTE':
            return lvalue >= rvalue
        elif self.operation == 'EQUALS':
            return lvalue == rvalue
        elif self.operation == 'LT':
            return lvalue < rvalue
        elif self.operation == 'GT':
            return lvalue > rvalue

    def __repr__(self):
        return f'op {self.operation} ({self.lvalue} , {self.rvalue})'

class LiteralNode:
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def __repr__(self):
        return f'literal {self.value}'

class NotNode:
    def __init__(self, node_to_not):
        self.node_to_not = node_to_not

    def evaluate(self):
        return not self.node_to_not.evaluate()

    def __repr__(self):
        return f'not ({self.node_to_not})'

tokens = [
    'LPAREN',
    'RPAREN',
    'NUMBER',
    'STRING',
    'AND',
    'OR',
    'NOT',
    'NAME',
    'NOTEQUAL',
    'LTE',
    'GTE',
    'EQUALS',
    'LT',
    'GT',
    'COMMA'
]

def t_AND(t):
    r'and'
    return t

def t_OR(t):
    r'or'
    return t

def t_NOT(t):
    r'not'
    return t

def t_STRING(t):
    r'"[a-zA-Z0-9_]*"'
    t.value = t.value[1:-1]
    return t

t_ignore = ' \t'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NOTEQUAL = r'!='
t_LTE = r'<='
t_GTE = r'>='
t_EQUALS = r'='
t_LT = r'<'
t_GT = r'>'
t_COMMA = r','

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print('Invalid Token:', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('nonassoc', 'NOTEQUAL', 'LTE', 'GTE', 'EQUALS', 'LT', 'GT'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'NOT')
)

token_value_bin_op_map = {
    'and': 'AND',
    'or': 'OR',
    '<=': 'LTE',
    '>=': 'GTE',
    '=': 'EQUALS',
    '<': 'LT',
    '>': 'GT',
}

def p_expression_bin(p):
    '''expression   : expression AND expression
                    | expression OR expression'''
    p[0] = BinaryOpNode(p[1], token_value_bin_op_map[p[2]], p[3])


def p_expression_literal(p):
    '''expression   : STRING
                    | NUMBER'''
    p[0] = LiteralNode(p[1])

def p_expression_not(p):
    '''expression   : NOT expression'''
    p[0] = NotNode(p[1])

def p_expression_parens(p):
    '''expression   : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_misc(p):
    '''expression   : function
                    | comparison'''
    p[0] = p[1]

def p_comparison(p):
    '''comparison   : expression LTE expression
                    | expression GTE expression
                    | expression EQUALS expression
                    | expression LT expression
                    | expression GT expression
                    | expression NOTEQUAL expression'''
    p[0] = BinaryOpNode(p[1], token_value_bin_op_map[p[2]], p[3])

def p_func_args(p):
    '''function     : NAME LPAREN argumentList RPAREN'''
    p[0] = FunctionNode(p[1], p[3])

def p_func_noargs(p):
    '''function     : NAME LPAREN RPAREN'''
    p[0] = FunctionNode(p[1], [])

def p_arg_list(p):
    '''argumentList : argument
                    | argumentList COMMA argument'''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_argument(p):
    '''argument : NUMBER
                | STRING'''
    p[0] = p[1]

def p_error(p):
    print("Parse error: " + str(p))


condition_parser = yacc.yacc()


class PlacementParser:
    def parse(self, str_to_parse):
        if len(str_to_parse) == 0:
            return ('', [])
        split_str_to_parse = str_to_parse.split()
        return (split_str_to_parse[0], split_str_to_parse[1:])

placement_parser = PlacementParser()