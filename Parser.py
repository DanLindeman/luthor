from Lexer import Lexer
from Node import Node

class Parser(object):

    def __init__(self, path_to_file):
        self.lexer = Lexer(path_to_file)
        self.path_to_file = path_to_file
        self.ast_nodes = {}

    def parse_file(self):
        self.current_token = self.lexer.next_token()
        self.parse()
        return self.ast_nodes

    def print_nodes(self):
        for node in self.ast_nodes.keys():
            print(node, self.ast_nodes[node])

    def add_parent_child(self, id_node, current_token):
        self.add_node(id_node)
        self.add_node(current_token)
        if current_token not in self.ast_nodes[id_node]["children"]:
            self.ast_nodes[id_node]["children"].append(current_token)

    def add_node(self, id_node):
        if id_node not in self.ast_nodes.keys():
            self.ast_nodes[id_node] = {}
            self.ast_nodes[id_node]["children"] = []

    def parse(self):
        self.parse_strict()
        if self.current_token.kind == "DIGRAPH":
            self.parse_digraph()
        elif self.current_token.kind == "GRAPH":
            self.parse_graph()
        else:
            raise ParserException(self.current_token)

    def accept(self, token, token_kind):
        if token.kind == token_kind:
            self.current_token = self.lexer.next_token()
        else:
            raise ParserException(self.current_token)

    def parse_digraph(self):
        if self.current_token.kind == "DIGRAPH":
            self.accept(self.current_token, "DIGRAPH")
            self.parse_optional_id()
            self.accept(self.current_token, "LEFT_CB")
            self.parse_statement_list()
            self.accept(self.current_token, "RIGHT_CB")
        else:
            raise ParserException(self.current_token)

    def parse_graph(self):
        if self.current_token.kind == "GRAPH":
            self.accept(self.current_token, "GRAPH")
            self.parse_optional_id()
            self.accept(self.current_token, "LEFT_CB")
            self.parse_statement_list()
            self.accept(self.current_token, "RIGHT_CB")
        else:
            raise ParserException(self.current_token)

    def parse_statement(self):
        if (self.current_token.kind == "NODE") or (self.current_token.kind == "EDGE") or (self.current_token.kind == "GRAPH"):
            self.parse_node_statement()
        elif self.current_token.kind == "ID":
            id_node = self.current_token.value
            self.accept(self.current_token, "ID")
            if (self.current_token.kind == "DIRECTED_EDGE") or (self.current_token.kind == "UNDIRECTED_EDGE"):
                self.parse_edge_statement(id_node)
            elif self.current_token.kind == "LEFT_SB":
                self.parse_node_creation(id_node)
            elif self.current_token.kind == "EQUALS":
                self.parse_single_assignment()
        elif self.current_token.kind == "SUBGRAPH":
            self.parse_subgraph()
        else:
            raise ParserException(self.current_token)

    def parse_single_assignment(self):
        if self.current_token.kind == "EQUALS":
            self.accept(self.current_token, "EQUALS")
            self.accept(self.current_token, "ID")
        else:
            raise ParserException(self.current_token)

    def parse_subgraph(self):
        if self.current_token.kind == "SUBGRAPH":
            self.accept(self.current_token, "SUBGRAPH")
            self.parse_optional_id()
            self.accept(self.current_token, "LEFT_CB")
            self.parse_statement_list()
            self.accept(self.current_token, "RIGHT_CB")
        else:
            raise ParserException(self.current_token)

    def parse_node_creation(self, id_node):
        self.add_node(id_node)
        if self.current_token.kind == "LEFT_SB":
            self.parse_atttribute_list()
        else:
            raise ParserException(self.current_token)

    def parse_node_statement(self):
        if self.current_token.kind == "NODE":
            self.accept(self.current_token, "NODE")
            self.parse_atttribute_list()
        else:
            raise ParserException(self.current_token)

    def parse_edge_statement(self, id_node):
        self.parse_edge_type()
        if self.current_token.kind == "ID":
            self.add_parent_child(id_node, self.current_token.value)
            self.accept(self.current_token, "ID")
            self.parse_atttribute_list()
        else:
            raise ParserException(self.current_token)

    def parse_assignment(self):
        if self.current_token.kind == "ID":
            self.accept(self.current_token, "ID")
            self.accept(self.current_token, "EQUALS")
            self.accept(self.current_token, "ID")
        else:
            raise ParserException(self.current_token)

    def parse_edge_type(self):
        if self.current_token.kind == "DIRECTED_EDGE":
            self.accept(self.current_token, "DIRECTED_EDGE")
        elif self.current_token.kind == "UNDIRECTED_EDGE":
            self.accept(self.current_token, "UNDIRECTED_EDGE")
        else:
            raise ParserException(self.current_token)

    def parse_semicolon(self):
        if self.current_token.kind == "SEMICOLON":
            self.current_token = self.lexer.next_token()
        else:
            raise ParserException(self.current_token)

    def parse_atttribute_list(self):
        if self.current_token.kind == "LEFT_SB":
            self.accept(self.current_token, "LEFT_SB")
            self.parse_assignment_list()
            self.accept(self.current_token, "RIGHT_SB")

    def parse_assignment_list(self):
        self.parse_assignment()
        if self.current_token.kind == "COMMA":
            self.accept(self.current_token, "COMMA")
            self.parse_assignment_list()
        elif self.current_token.kind == "SEMICOLON":
            self.accept(self.current_token, "SEMICOLON")
            self.parse_assignment_list()

    def parse_strict(self):
        if self.current_token.kind == "STRICT":
            self.accept(self.current_token, "STRICT")

    def parse_optional_id(self):
        if self.current_token.kind == "ID":
            self.accept(self.current_token, "ID")

    def parse_statement_list(self):
        while self.current_token.kind != "RIGHT_CB":
            self.parse_statement()
            self.parse_semicolon()


class ParserException(Exception):
    def __init__(self, current_token):
        message = "\n\tUnexpected Token {0}\n\ton line: {0.line_number} \n\tcolumn: {0.character_number}".format(current_token)
        super(ParserException, self).__init__(message)


if __name__ == "__main__":
    p = Parser("myFile")
    p.parse_file()
    p.print_nodes()
