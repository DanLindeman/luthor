from Lexer import Lexer

class Parser(object):

    def __init__(self, path_to_file):
        self.lexer = Lexer(path_to_file)
        self.path_to_file = path_to_file

    def parse_file(self):
        self.current_token = self.lexer.next_token()
        self.parse()

    def parse(self):
        self.parse_strict()
        self.parse_id()
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

    def parse_strict(self):
        if self.current_token.kind == "STRICT":
            self.accept(self.current_token, "STRICT")

    def parse_id(self):
        if self.current_token.kind == "ID":
            self.accept(self.current_token, "ID")

    def parse_digraph(self):
        self.accept(self.current_token, "DIGRAPH")
        self.accept(self.current_token, "ID")
        self.accept(self.current_token, "LEFT_CB")
        self.parse_statement_list()
        self.accept(self.current_token, "RIGHT_CB")

    def parse_graph(self):
        self.accept(self.current_token, "GRAPH")
        self.accept(self.current_token, "ID")
        self.accept(self.current_token, "LEFT_CB")
        self.parse_statement_list()
        self.accept(self.current_token, "RIGHT_CB")

    def parse_statement_list(self):
        while self.current_token.kind != "RIGHT_CB":
            self.parse_statement()

    def parse_statement(self):
        if (self.current_token.kind == "NODE") or (self.current_token.kind == "EDGE") or (self.current_token.kind == "GRAPH"):
            self.parse_node_statement()
        elif self.current_token.kind == "ID":
            self.accept(self.current_token, "ID")
            if (self.current_token.kind == "DIRECTED_EDGE") or (self.current_token.kind == "UNDIRECTED_EDGE"):
                self.parse_edge_statement()
            elif self.current_token.kind == "LEFT_SB":
                self.parse_node_creation()
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
            self.parse_semicolon()
        else:
            raise ParserException(self.current_token)

    def parse_subgraph(self):
        if self.current_token.kind == "SUBGRAPH":
            self.accept(self.current_token, "SUBGRAPH")
            self.parse_id()
            self.accept(self.current_token, "LEFT_CB")
            self.parse_statement_list()
            self.accept(self.current_token, "RIGHT_CB")
        else:
            raise ParserException(self.current_token)

    def parse_node_creation(self):
        if self.current_token.kind == "LEFT_SB":
            self.accept(self.current_token, "LEFT_SB")
            self.parse_assignment_list()
            self.accept(self.current_token, "RIGHT_SB")
            self.parse_semicolon()
        else:
            raise ParserException(self.current_token)

    def parse_node_statement(self):
        if self.current_token.kind == "NODE":
            self.accept(self.current_token, "NODE")
            self.parse_atttribute_list()
            self.parse_semicolon()
        else:
            raise ParserException(self.current_token)

    def parse_edge_statement(self):
        self.parse_edge_type()
        if self.current_token.kind == "ID":
            self.accept(self.current_token, "ID")
            self.parse_atttribute_list()
            self.parse_semicolon()
        else:
            raise ParserException(self.current_token)

    def parse_semicolon(self):
        if self.current_token.kind == "SEMICOLON":
            self.current_token = self.lexer.next_token()

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

class ParserException(Exception):
    def __init__(self, current_token):
        message = "\n\tUnexpected Token {0} \n\ton line: {0.line_number} \n\tcharacter: {0.character_number}".format(current_token)
        super(ParserException, self).__init__(message)


if __name__ == "__main__":
    p = Parser("myFile")
    p.parse_file()
