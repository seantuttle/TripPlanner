import math
import queue


class State:
    def __init__(self, value, parent, start=None, end=None, end_xy=None, dist=0):
        self.children = []
        self.parent = parent
        self.value = value
        if parent:
            self.start = parent.start
            self.end = parent.end
            self.end_x = parent.end_x
            self.end_y = parent.end_y
            self.path = parent.path[:]
            self.path.append(value)
            self.dist = parent.dist + dist
        else:
            self.path = [value]
            self.start = start
            self.end = end
            self.end_x = end_xy[0]
            self.end_y = end_xy[1]
            self.dist = 0

    def run_heuristic(self, node):
        curr_x, curr_y = node.get_xy()
        euclidian_dist = math.sqrt((self.end_x - curr_x) ** 2 + (self.end_y - curr_y) ** 2)
        heuristic = self.dist + euclidian_dist
        return heuristic

    def create_children(self, node):
            if not self.children:
                self.children = [State(neighbor[0], self, dist=neighbor[1]) for neighbor in node.neighbors]


class PathFinder:
    def __init__(self, start, end, graph):
        self.start = start
        self.end = end
        self.graph = graph
        self.dist = 0
        self.path = []
        self.visited =[]
        self.unvisited = queue.PriorityQueue()

    def find_path(self):
        start_state = State(self.start, None, self.start, self.end, end_xy=self.graph.get(self.end).get_xy())

        count = 0
        self.unvisited.put((0, count, start_state))
        while(not self.path and self.unvisited.qsize()):
                closest_child = self.unvisited.get()[2]
                closest_child.create_children(self.graph.get(closest_child.value))
                self.visited.append(closest_child.value)
                for child in closest_child.children:
                   if child.value not in self.visited:
                    count += 1
                    if child.value == self.end:
                       self.path = child.path
                       self.dist = child.dist
                       break
                    self.unvisited.put((child.run_heuristic(self.graph.get(child.value)), count, child))

        if not self.path:
            raise RuntimeError('There is no valid path')

        return self.path, self.dist
