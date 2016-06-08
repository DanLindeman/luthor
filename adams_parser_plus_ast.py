#!/usr/bin/env python
"""
parser.py

A simple LL(1) parser that builds an AST.

Grammar:
    list     : '[' elements ']'
    elements : element (',' element)*
    element  : NAME | list

Tokens:
    (EOF, NAME, COMMA, LBRACK, RBRACK) = range(5)
    names = [ 'EOF', 'NAME', 'COMMA', 'LBRACK', 'RBRACK']

AST:
       (list a (list b c d (list e f g)))
"""

from adams_lexer import Lexer
from adams_lexer import Token
from adams_lexer import TokenTypes
import sys

#-----------------------------------------------------------------------------
#     _    ____ _____
#    / \  / ___|_   _|
#   / _ \ \___ \ | | 
#  / ___ \ ___) || | 
# /_/   \_\____/ |_| 
                                        
class AST(object):
    """Homogeneous AST """
    def __init__(self, token):
        """token should be of type Lexer.Token"""
        self.token = token     # node "value"
        self.children = []     # child AST nodes

    def add_child(self, t):
         self.children.append(t)

    def __str__(self):
         return str(self.token)

    def to_string_tree(self):
         """Build a string representing the entire tree."""
         if len(self.children) == 0:
              return str(self)
         buf = "(%s " % str(self.token)
         for i in range(len(self.children)):
             t = self.children[i]
             if i > 0:
                 buf += " "
             buf += t.to_string_tree()
         buf += ")"
         return buf

#-----------------------------------------------------------------------------
#  ____                         
# |  _ \ __ _ _ __ ___  ___ _ __
# | |_) / _` | '__/ __|/ _ \ '__|
# |  __/ (_| | |  \__ \  __/ |  
# |_|   \__,_|_|  |___/\___|_|  
                               
class Parser(object):
    """A parser."""
    def __init__(self, lexer):
        """lexer should be an instance of Lexer"""
        self.lexer = lexer
        self.lookahead = self.lexer.next_token()
   
    def __match(self, token):
        """Ensures the next token is of type token. token should be an
           integer from lexer.TokenTypes.
        """
        if self.lookahead.type == token:
            self.lookahead = self.lexer.next_token()
        else:
            print >> sys.stderr, "Expecting %s found %s" % (TokenTypes.names[token], self.lookahead)
            sys.exit(1)
   
    def parse_element(self):
        """Parses element  : NAME | list
           Returns an AST node."""
        if self.lookahead.type == TokenTypes.NAME:
            node = AST(self.lookahead)
            self.__match(TokenTypes.NAME)
            return node
        elif self.lookahead.type == TokenTypes.LBRACK:
            return self.parse_list()
        else:
            print >> sys.stderr, "Expecting name or list; found %s" % self.lookahead
            sys.exit(1)
           
    def parse_elements(self):
        """Parses elements : element (',' element)*
           Returns an AST node."""
        node = AST('list')
        node.add_child( self.parse_element() )
        while self.lookahead.type == TokenTypes.COMMA:
            self.__match(TokenTypes.COMMA)
            node.add_child( self.parse_element() )
        return node
           
    def parse_list(self):
        """Parses  list : '[' elements ']'
           Returns an AST node."""
        self.__match(TokenTypes.LBRACK)
        node = self.parse_elements()
        self.__match(TokenTypes.RBRACK)   
        return node

#-----------------------------------------------------------------------------
#  __  __       _      
# |  \/  | __ _(_)_ __ 
# | |\/| |/ _` | | '_ \
# | |  | | (_| | | | | |
# |_|  |_|\__,_|_|_| |_|
                      
def main():
    lexer = Lexer("[a, [b, [c,d], e], f]")
    parser = Parser(lexer)
    t = parser.parse_list()
    print t.to_string_tree()

if __name__ == "__main__":
     sys.exit(main())