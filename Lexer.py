#!usr/bin/env python3

import re
import sys

class Character(object):

    def __init__(self, character, line_number, character_number):
        self.character = character
        self.line_number = line_number
        self.character_number = character_number


class Serializer(object):
    
    def __init__(self):
        self.multi_line_comments = re.compile("/\*.*\*/")
        self.single_line_comments = re.compile("[\/\/].*")

    def serialize(self, filename):
        as_characters = []
        current_line_number = 0
        current_character_number = 0

        with open(filename) as my_file:
            for line in my_file:
                current_line_number += 1
                current_character_number = 0
                line = self.remove_comments(line)
                for character in line:
                    current_character_number += 1
                    as_characters.append(Character(character, current_line_number, current_character_number))

        return as_characters

    def remove_comments(self, line):
        line = self.multi_line_comments.sub('', line)
        line = self.single_line_comments.sub('', line)
        return line


class Token(object):

    def __init__(self, kind, value, line_number, character_number):
        self.kind = kind
        self.value = value
        self.line_number = line_number
        self.character_number = character_number

    def __str__(self):
        return "<{0.kind}: {0.value}>".format(self)


class Lexer(object):

    def __init__(self, path_to_file):
        self.text = Serializer().serialize(path_to_file)
        self.alpha_numeric_with_underscores = re.compile("^[a-zA-Z0-9_\.\"\\\]$")
        self.id_regex = re.compile("^[a-zA-Z0-9_\.\" \\\]$")
        self.character_index = 0
        self.current_character = self.text[self.character_index]

    def consume(self):
        self.character_index += 1
        if self.character_index >= len(self.text):
            self.current_character = Character("EOF", self.current_character.line_number, self.current_character.character_number)
        else:
            self.current_character = self.text[self.character_index]

    def numeric(self, string):
        try:
            float(string)
            return True
        except:
            return False

    def next_token(self):
        while self.current_character.character != "EOF":
            if self.current_character.character in [' ', '\t', '\n', '\r']:
                self.consume()
            elif self.current_character.character == '=':
                self.consume()
                return Token("EQUALS", "=", self.current_character.line_number, self.current_character.character_number - 1)
            elif self.current_character.character == '{':
                self.consume()
                return Token("LEFT_CB","{", self.current_character.line_number, self.current_character.character_number - 1)
            elif self.current_character.character == '}':
                self.consume()
                return Token("RIGHT_CB","}", self.current_character.line_number, self.current_character.character_number - 1)
            elif self.current_character.character == ',':
                self.consume()
                return Token("COMMA",",", self.current_character.line_number, self.current_character.character_number - 1)
            elif self.current_character.character == '[':
                self.consume()
                return Token("LEFT_SB","[", self.current_character.line_number, self.current_character.character_number - 1)
            elif self.current_character.character == ']':
                self.consume()
                return Token("RIGHT_SB","]", self.current_character.line_number, self.current_character.character_number - 1)
            elif self.current_character.character == ';':
                self.consume()
                return Token("SEMICOLON",";", self.current_character.line_number, self.current_character.character_number - 1)
            elif self.current_character.character == '@':
                self.consume()
                return Token("AT","@", self.current_character.line_number, self.current_character.character_number - 1)
            elif self.current_character.character == ':':
                self.consume()
                return Token("COLON",":", self.current_character.line_number, self.current_character.character_number - 1)
            elif self.current_character.character == "\"":
                # build as if we know it's going to just be a plain-old ID
                lexeme = ""
                while (self.id_regex.match(self.current_character.character) and self.current_character.character != "EOF"):
                    lexeme += self.current_character.character
                    self.consume()
                return Token("ID", lexeme, self.current_character.line_number, self.current_character.character_number - len(lexeme))
            elif self.alpha_numeric_with_underscores.match(self.current_character.character):
                lexeme = ""
                while (self.alpha_numeric_with_underscores.match(self.current_character.character) and self.current_character.character != "EOF"):
                    lexeme += self.current_character.character
                    self.consume()
                if lexeme == "strict":
                    return Token("STRICT", 'strict', self.current_character.line_number, self.current_character.character_number - len(lexeme))
                elif lexeme == "digraph":
                    return Token("DIGRAPH", "digraph", self.current_character.line_number, self.current_character.character_number - len(lexeme))
                elif lexeme == "subgraph":
                    return Token("SUBGRAPH", "subgraph", self.current_character.line_number, self.current_character.character_number - len(lexeme))
                elif lexeme == "graph":
                    return Token("GRAPH", "graph", self.current_character.line_number, self.current_character.character_number - len(lexeme))
                elif lexeme == "node":
                    return Token("NODE", "node", self.current_character.line_number, self.current_character.character_number - len(lexeme))
                elif lexeme == "edge":
                    return Token("EDGE", "edge", self.current_character.line_number, self.current_character.character_number - len(lexeme))
                else:
                    return Token("ID", lexeme, self.current_character.line_number, self.current_character.character_number - len(lexeme))
            elif self.current_character.character == "-":
                self.consume()
                if self.current_character.character == '-':
                    self.consume()
                    return Token("UNDIRECTED_EDGE","--", self.current_character.line_number, self.current_character.character_number - 2)
                elif self.current_character.character == '>':
                    self.consume()
                    return Token("DIRECTED_EDGE","->", self.current_character.line_number, self.current_character.character_number - 2)
                else:
                    print("ERROR: - followed by an unexpected token: " + self.current_character)
                    sys.exit(1)
            else:
                raise Exception("Something went wrong")
        return Token("EOF", "EOF", self.current_character.line_number, self.current_character.character_number)


if __name__ == "__main__":
    lexer = Lexer("myFile")
    token = lexer.next_token()
    while(token.kind != "EOF"):
        print(token)
        token = lexer.next_token()
