from Parser import Parser
from Node import Node

class Graph(object):

    def __init__(self):
        parser = Parser("myFile")
        self.nodes = parser.parse_file()
        self.printed_nodes = []

    def print_nodes(self):
        for node in self.nodes:
            print(node.value + "\n[")
            for child in node.children:
                print("\t" + child.value)
            print("]")

    def experiment(self):
        #Sanity check that this actually produces a connected graph.
        for node in self.nodes:
            if node.value == "main":
                main = node
        print(main.value)
        for child in main.children:
            print("\t" + child.value)
            for grandchild in child.children:
                print("\t\t" + grandchild.value)


if __name__ == "__main__":
    g = Graph()
    g.print_nodes()
    # g.experiment()