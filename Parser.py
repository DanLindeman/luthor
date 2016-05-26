from Lexer import Lexer

class Parser(object):

    def __init__(self, lexer):
        self.lexer = Lexer("myFile")
        self.current_token = self.lexer.next_token()
        self.parse_file()

    def parse_file(self):
        while(self.current_token.kind != "EOF"):
            print(self.current_token)
            self.current_token = self.lexer.next_token()

    # def accept(self):
    #     """
    #     This is super like consume from Lexer
    #     """
    #     self.current_token = self.lexer.next_token()



    # def parse_id(self, current_token):
    #     if current_token.kind == "ID":
    #         accept(self.current_token)
    #     # if current_token == "n"
    #     #     accept(current_token)
    #     # elif current_token == "ne":
    #     #     accept(current_token)
    #     # elif current_token == "e":
    #     #     accept(current_token)
    #     # elif current_token == "se":
    #     #     accept(current_token)
    #     # elif current_token == "s":
    #     #     accept(current_token)
    #     # elif current_token == "sw":
    #     #     accept(current_token)
    #     # elif current_token == "w":
    #     #     accept(current_token)
    #     # elif current_token == "nw":
    #     #     accept(current_token)
    #     # elif current_token == "c":
    #     #     accept(current_token)
    #     # elif current_token == "_":
    #     #     accept(current_token)


    # def parse_port_angle(self, current_token):
    #     accept(current_token)
l = Lexer("myFile")
p = Parser(l)
