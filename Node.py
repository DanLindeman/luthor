

class Node(object):

    def __init__(self, value):
        self.value = value
        self.children = []

    def __str__(self):
        return "{0.value}\n\t{0.children}".format(self)

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
            

