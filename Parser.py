from Lexer import Lexer

class Parser(object):

    def __init__(self, lexer):
        self.lexer = Lexer("test_assign_node")

    def parse_file(self):
        self.current_token = self.lexer.next_token()
        self.parse_node_assignment()
        # while(self.current_token.kind != "EOF"):
        #     self.current_token = self.lexer.next_token()
        #     print(self.current_token)
            # self.parse_node_assignment()

    def accept(self, token, token_kind):
        if token.kind == token_kind: 
            print("GOT IT " + token.value)
            self.current_token = self.lexer.next_token()
        else:
            raise Exception("Oh no!")

    def parse_node_assignment(self):
        if self.current_token.kind == "ID":

            self.accept(self.current_token, "ID")
            self.parse_edge_type()
            self.accept(self.current_token, "ID")
            self.parse_atttribute_list()
            self.accept(self.current_token, "SEMICOLON")


        else:
            raise Exception("Oh no!")

    def parse_atttribute_list(self):
        if self.current_token.kind == "LEFT_SB":
            self.accept(self.current_token, "LEFT_SB")
            self.parse_assignment()
            self.accept(self.current_token, "RIGHT_SB")

    # def parse_assignment_list(self):
    #     # self.accept(self.current_token, "COMMA")
    #     self.parse_assignment()


    def parse_assignment(self):
        
        self.accept(self.current_token, "ID")
        self.accept(self.current_token, "EQUALS")
        self.accept(self.current_token, "NUM")


    def parse_edge_type(self):
        if self.current_token.kind == "DIRECTED_EDGE":
            self.accept(self.current_token, "DIRECTED_EDGE")
        elif self.current_token.kind == "UNDIRECTED_EDGE":
            self.accept(self.current_token, "UNDIRECTED_EDGE")

    def parse_id(self):
        self.accept(self.current_token, "ID")


l = Lexer("test_assign_node")
p = Parser(l)
p.parse_file()


# digraph = 'digraph' ID {  statement_list }
# statement_list = statement (";" 
                                # | )



# node_assignment = ID (->|--) ID SEMICOLON
# ID = id_regex