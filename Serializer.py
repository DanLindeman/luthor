import re

class Serializer(object):
    
    def __init__(self):
        self.multi_line_comments = re.compile("/\*.*\*/")
        self.single_line_comments = re.compile("[\/\/].*")

    def serialize(self, filename):
        as_characters = []
        with open(filename) as my_file:
            for line in my_file:
                line = self.remove_comments(line)
                for character in line:
                    as_characters.append(character)
        return as_characters

    def remove_comments(self, line):
        line = self.multi_line_comments.sub('', line)
        line = self.single_line_comments.sub('', line)
        return line
