#!/usr/bin/env python
"""
parser.py

A simple LL(1) parser.

Grammar:
(NB: The definition for elements isn’t kosher BNF, but matches the algorithm. The BNF version would read
     elements : element elements'
     elements’ : ‘,’ elements | ε
)

    list     : '[' elements ']'
    elements : element (',’ elements)*
    element  : NAME | list

"""

from lexer import Lexer
from lexer import TokenTypes
import sys
  
class Parser(object):
    """A parser."""
    def __init__(self, lexer):
        """lexer should be an instance of Lexer"""
        self.lexer = lexer
        self.lookahead = self.lexer.next_token()
       
    def __consume(self):
        """Moves to the next token."""
        self.lookahead = self.lexer.next_token()
       
    def __match(self, token):
        """Ensures the next token is of type token. token should be an
           integer from lexer.TokenTypes.
        """
        if self.lookahead.type == token:
            self.__consume()
        else:
            print >> sys.stderr, "Expecting %s found %s" % (TokenTypes.names[token], self.lookahead)
   
    def parse_element(self):
        """Parses element."""
        if self.lookahead.type == TokenTypes.NAME:
            self.__match(TokenTypes.NAME)
        elif self.lookahead.type == TokenTypes.LBRACK:
            self.parse_list()
        else:
            print >> sys.stderr, "Expecting name or list; found %s" % self.lookahead
       
    def parse_elements(self):
        """Parses elements."""
        self.parse_element()
        while self.lookahead.type == TokenTypes.COMMA:
            self.__match(TokenTypes.COMMA)
            self.parse_element()
       
    def parse_list(self):
        """Parses a list."""
        self.__match(TokenTypes.LBRACK)
        self.parse_elements()
        self.__match(TokenTypes.RBRACK)
       
def main():
    lexer = Lexer("[foo, [bar, goo]]")
    parser = Parser(lexer)
    t = parser.parse_list()

if __name__ == "__main__":
     sys.exit(main())