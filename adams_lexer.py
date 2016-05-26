#!/usr/bin/env python
"""
lexer.py 

A simple hand-crafted lexer. See the TokenTypes class for a list of tokens
this lexer recognizes. 
"""

import sys

class TokenTypes(object):
    """A singleton to represent all token types."""
    (EOF, NAME, COMMA, LBRACK, RBRACK) = range(5)
    names = [ 'EOF', 'NAME', 'COMMA', 'LBRACK', 'RBRACK']

class Token(object):
    """An abstract token."""

    def __init__(self, type, text):
        """Constructor.
           type is a numeric token type from TokenTypes
           text is the lexeme
        """
        self.type = type
        self.text = text

    def __str__(self):
        return "<'%s', %s>" % (self.text, TokenTypes.names[self.type])

class Lexer(object):
    """My custom lexer."""

    def __init__(self, str):
        """Constructor.
           str is the input to the lexer
        """
        self.input = str            # input string
        self.p = 0                  # index of current character
        self.c = self.input[self.p] # current character itself

    def __consume(self):
        """Advance to the next character of input, or EOF."""
        self.p += 1
        if self.p >= len(self.input):
            self.c = TokenTypes.EOF
        else:
            self.c = self.input[self.p]

    def next_token(self):
        """Return the next Token in the input stream, ignoring whitespace."""
        while self.c != TokenTypes.EOF:
            if self.c in [' ', '\t', '\n', '\r']:
                self.__consume()
            elif self.c == ',':
                self.__consume()
                return Token(TokenTypes.COMMA, ',')
            elif self.c == '[':
                self.__consume()
                return Token(TokenTypes.LBRACK, '[')
            elif self.c == ']':
                self.__consume()
                return Token(TokenTypes.RBRACK, ']')
            elif self.c.isalpha():
                # Consume all contiguous alphabetic characters.
                lexeme = ""
                while self.c != TokenTypes.EOF and self.c.isalpha():
                    lexeme += self.c
                    self.__consume()
                t = Token(TokenTypes.NAME, lexeme)
                return t
            else:
                print >> sys.stderr, "Invalid character %c." % self.c
                sys.exit(1)
        return Token(TokenTypes.EOF, "<EOF>")

def main():
    lexer = Lexer("  this, [is]\ta\ntest ")
    t = lexer.next_token()
    while (t.type != TokenTypes.EOF):
        print t
        t = lexer.next_token()

if __name__ == "__main__":
    sys.exit(main())


