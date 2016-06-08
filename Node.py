

class Node(object):

    def __init__(self, value):
        self.value = value
        self.children = []

    def __str__(self):
        return "{0.value}".format(self)

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
            

    def to_string_tree(self):
         """Build a string representing the entire tree."""
         if len(self.children) == 0:
              return str(self)
         buf = "(%s | " % str(self.value)
         for i in range(len(self.children)):
             t = self.children[i]
             if i > 0:
                 buf += " "
             buf += t.to_string_tree()
         buf += ")"
         return buf