import unittest
from Parser import Parser
from Lexer import Lexer
from Lexer import Token

class TestParser(unittest.TestCase):

    def setUp(self):
        lexer = Lexer("myFile")
        self.parser = Parser(lexer)

    def test_parse_id(self):
        self.parser.current_token = Token("ID", "test_val", 0, 0)
        self.assertTrue(self.parser.current_token.kind  == "ID")



if __name__ =="__main__":
    unittest.main()