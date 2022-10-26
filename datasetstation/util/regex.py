def bracket(regular_expression):
    return ''.join([r'(', regular_expression, r')'])


def bracket_absence(regular_expression):
    return ''.join([r'(', regular_expression, r')?'])


def absence(regular_expression):
    return ''.join([regular_expression, r'?'])


def start_end(regular_expression):
    return ''.join([r'^', regular_expression, r'$'])