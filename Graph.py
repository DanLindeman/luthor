from Parser import Parser
from Node import Node

class Graph(object):

    def __init__(self):
        parser = Parser("myFile")
        self.node_hash = parser.parse_file()
        self.nodes = []

    def convert_hash_to_graph(self):
        for node in self.node_hash:
            self.create(node, self.node_hash[node]["children"])

    def create(self, node, children):
        current_node = Node(node)

        for child in children:
            if child not in self.nodes:
                child_node = Node(child)
                current_node.add_child(child_node)
            else:
                child_node = Node(self.node_hash[child])
                current_node.add_child(child_node)

            
        print(current_node)

    def get_root(self):
        pass



if __name__ == "__main__":
    g = Graph()
    g.convert_hash_to_graph()