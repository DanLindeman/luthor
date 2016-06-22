from Graph import Graph
from collections import deque

class TreeWalker(object):

    def __init__(self, start, end):
        self.g = Graph()
        self.node_hash = self.g.node_hash

        self.unvisited = list(self.node_hash.keys())
        self.visited = []
        self.path = []

        self.current_distances = {}
        self.previous_nodes = {}

        for node in self.unvisited:
          self.current_distances[node] = float('inf')
          self.previous_nodes[node] = ""
        self.start = start
        self.end = end
        self.current_distances[start] = 0
        self.current = self.start
        self.neighborhood = self.create_neighborhood()


    def create_neighborhood(self):
        neighborhood = {}
        for parent in self.node_hash:
            for child in self.node_hash[parent]["children"]:
                try:
                    neighborhood[parent].append(child)
                except KeyError:
                    neighborhood[parent] = [child]
                try:
                    neighborhood[child].append(parent)
                except KeyError:
                    neighborhood[child] = [parent]
        return neighborhood

    def print_path(self):
        node = self.current
        try:
            while(node != self.start):
                self.path.append(self.previous_nodes[node])
                node = self.previous_nodes[node]
        except KeyError:
            pass
        self.path.reverse()
        self.path.remove(self.start)
        print("The Shortest Path between {0.start} and {0.end} is: \n".format(self) 
            + "\t" + "{0.start} -> ".format(self) 
            + self.path.__str__() 
            + " -> {0.end}".format(self))

    def next_node(self, node):
        current_minimum = float('inf')
        closest = None
        for child in self.neighborhood[node]:
            if ((self.current_distances[child] < current_minimum) and (child in self.unvisited)):
                current_minimum = self.current_distances[child]
                closest = child
        return closest


    def update_neighbors(self, node):
        for child in self.neighborhood[node]:
            if child not in self.visited:
                dist = 1
            else:
                dist = self.current_distances[child] + 1

            if dist < self.current_distances[child]:
                self.current_distances[child] = dist
                self.previous_nodes[child] = node

    def apply_dijkstras(self):
      while (len(self.unvisited) > 0):
            self.update_neighbors(self.current)
            if self.current == self.end:
                break
            self.visited.append(self.unvisited.pop(self.unvisited.index(self.current)))
            self.current = self.next_node(self.current)
            self.apply_dijkstras()

if __name__ == "__main__":
    tw = TreeWalker('main','make_string')
    tw.apply_dijkstras()
    tw.print_path()

