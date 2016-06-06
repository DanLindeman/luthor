

class Node(object):

    def __init__(self, value):
        self.value = value
        self.children = []

    def __str__(self):
        children = "Children: ["
        for index, child in enumerate(self.children):
            if index == 0:
                children += child.value
            else:
                children += ", " + child.value
        children += ']'
        return "Node: {0.value}\n\t{1}\n".format(self, children)

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
            

