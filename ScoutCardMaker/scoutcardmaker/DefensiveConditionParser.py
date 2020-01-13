import ply.lex as lex
import ply.yacc as yacc


class FunctionNode:
    def __init__(self, function_name, argument_list):
        self.function_name = function_name
        self.argument_list = argument_list

    def evaluate(self, function_map):
        arguments = [argument.value for argument in self.arguments]
        return function_map[self.function_name](*arguments)

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
    def __init__(self, value, literal_type):
        self.value = value
        self.literal_type = literal_type

    def evaluate(self):
        return self.value

    def __repr__(self):
        return f'{self.literal_type} literal {self.value}'


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
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'NOTEQUAL', 'LTE', 'GTE', 'EQUALS', 'LT', 'GT'),
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


def p_expression_literal_string(p):
    '''expression   : STRING '''
    p[0] = LiteralNode(p[1], 'string')

def p_expression_literal_number(p):
    '''expression   :  NUMBER'''
    p[0] = LiteralNode(p[1], 'number')

def p_expression_not(p):
    '''expression   : NOT expression'''
    p[0] = NotNode(p[1])

def p_expression_parens(p):
    '''expression   : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_misc(p):
    '''expression   : function'''
    p[0] = p[1]

def p_comparison(p):
    '''expression   : expression LTE expression
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


def p_argument_number(p):
    '''argument : NUMBER'''
    p[0] = LiteralNode(p[1], 'number')

def p_argument_string(p):
    '''argument : STRING'''
    p[0] = LiteralNode(p[1], 'number')

def p_error(p):
    raise ValueError('Parse Error')


condition_parser = yacc.yacc()


class PlacementParser:
    @staticmethod
    def parse(str_to_parse):
        if len(str_to_parse) == 0:
            return '', []
        split_str_to_parse = str_to_parse.split()
        return split_str_to_parse[0], split_str_to_parse[1:]


placement_parser = PlacementParser()


def validate_node(node, expected_evaluate_type, formation_function_info):
    if isinstance(node, FunctionNode):
        if node.function_name not in formation_function_info:
            return False, f'{node.function_name} doesn\'t exist'

        function_arguments = formation_function_info[node.function_name][1]
        if len(node.argument_list) != len(function_arguments):
            return False, f'{node.function_name} number of arguments mismatch'

        for argument_node, expected_argument_type in zip(node.argument_list, function_arguments):
            if argument_node.literal_type != expected_argument_type:
                return False, f'{node.function_name} argument mismatch'

        function_return_type = formation_function_info[node.function_name][0]
        if function_return_type != expected_evaluate_type:
            return False, f'{node.function_name} returns {function_return_type} when {expected_evaluate_type} expected'

        return True, None
    elif isinstance(node, BinaryOpNode):
        if expected_evaluate_type != 'bool':
            return False, f'{node.operation} produces bool when {expected_evaluate_type} expected'

        if node.operation in ['AND', 'OR']:
            ln_validate = validate_node(node.lvalue, 'bool', formation_function_info)
            if not ln_validate[0]:
                return ln_validate
            rn_validate = validate_node(node.rvalue, 'bool', formation_function_info)
            return rn_validate
        elif node.operation in ['LTE', 'LT', 'GTE', 'GT']:
            ln_validate = validate_node(node.lvalue, 'number', formation_function_info)
            if not ln_validate[0]:
                return ln_validate
            rn_validate = validate_node(node.rvalue, 'number', formation_function_info)
            return rn_validate
        if node.operation in ['EQUALS']:
            ln_evaluate_string = validate_node(node.lvalue, 'string', formation_function_info)
            rn_evaluate_string = validate_node(node.rvalue, 'string', formation_function_info)
            if ln_evaluate_string[0] and rn_evaluate_string[0]:
                return True, None

            ln_validate = validate_node(node.lvalue, 'number', formation_function_info)
            if not ln_validate[0]:
                return ln_validate
            rn_validate = validate_node(node.rvalue, 'number', formation_function_info)
            return rn_validate
    elif isinstance(node, LiteralNode):
        if node.literal_type != expected_evaluate_type:
            return False, f'{node.value} is {node.literal_type} when {expected_evaluate_type} expected'
        return True, None
    elif isinstance(node, NotNode):
        if expected_evaluate_type != 'bool':
            return False, f'"not" produces bool when {expected_evaluate_type} expected'
        return validate_node(node.node_to_not, 'bool')


if __name__ == '__main__':
    formation_function_info = {
        'func1': ('bool', ('number', 'string')),
        'func2': ('number', ()),
        'func3': ('string', ('number',))
    }

    root = condition_parser.parse('func2() <= 10')
    print(validate_node(root, 'bool', formation_function_info))

    root = condition_parser.parse('func2() and 10')
    print(validate_node(root, 'bool', formation_function_info))

    root = condition_parser.parse('func2()')
    print(validate_node(root, 'bool', formation_function_info))

    root = condition_parser.parse('func1() and func() > 4')
    print(validate_node(root, 'bool', formation_function_info))

    root = condition_parser.parse('func1(12, 14) and func() > 4')
    print(validate_node(root, 'bool', formation_function_info))

    root = condition_parser.parse('func3(10) = "Jimmy" and (func1(12, "bobby") or func() > 4)')
    print(validate_node(root, 'bool', formation_function_info))

