
class TokenTypes(object):

    def __init__(self):
        self.token_types = {
        "EOF": "EOF",
        '{': "LEFT_CB",
        '}': "RIGHT_CB",
        ',': "COMMA",
        '[': "LEFT_BR",
        ']': "RIGHT_BR",
        ';': "SEMICOLON",
        '=': "EQUALS",
        '->': "DIRECTED_EDGE",
        "ID": "ID",
        '\"': "QUOTE",
        "--": "UNDIRECTED_EDGE"
        }
