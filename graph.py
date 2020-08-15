import pandas as pd
import numpy as np


class Graph:
    def __init__(self, data_path=None, coords_path=None):
        self.nodes = []
        self.data_path = data_path
        self.coords_path = coords_path
        self.data = None
        self.coords = None

        if self.data_path:
            if self.coords_path:
                self.coords = pd.read_csv(self.coords_path, names=['Point', 'X', 'Y'], index_col='Point', comment='#')
            self.data = pd.read_csv(self.data_path, names=['Point', 'Neighbor', 'Distance'], index_col='Point', comment='#')
            for node_name in self.data.index.unique():
                neighbor_names = self.data.at[node_name, 'Neighbor']
                neighbor_distances = self.data.at[node_name, 'Distance']

                if not isinstance(neighbor_names, np.ndarray):
                    neighbor_names = [neighbor_names]
                if not isinstance(neighbor_distances, np.ndarray):
                    neighbor_distances = [neighbor_distances]

                neighbors = list(zip(neighbor_names, neighbor_distances))

                node_x = self.coords.at[node_name, 'X'] if self.coords_path else None
                node_y = self.coords.at[node_name, 'Y'] if self.coords_path else None

                self.add(node_name, neighbors, node_x, node_y,)


    def add(self, name, neighbors=None, x=None, y=None):
        if neighbors is None:
            neighbors = []
        if not self.exists(name):
            node = GraphNode(name, neighbors, x, y)
            self.nodes.append(node)
        else:
            node = self.get(name)

        for neighbor in neighbors:
            if self.exists(neighbor[0]):
                neighbor_node = self.get(neighbor[0])
                if not neighbor_node.has_neighbor(node):
                    neighbor_node.add_neighbor((name, neighbor[1]))
                if not node.has_neighbor(neighbor_node):
                    node.add_neighbor((neighbor[0], neighbor[1]))
            else:
                neighbor_x = self.coords.at[neighbor[0], 'X'] if self.coords_path else None
                neighbor_y = self.coords.at[neighbor[0], 'Y'] if self.coords_path else None
                neighbor_node = GraphNode(neighbor[0], [(name, neighbor[1])], neighbor_x, neighbor_y)
                if not node.has_neighbor(neighbor_node):
                    node.add_neighbor((neighbor[0], neighbor[1]))
                self.nodes.append(neighbor_node)

    def get(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def get_neighbors(self, name):
        return self.get(name).get_neighbors()

    def exists(self, name):
        for node in self.nodes:
            if node.name == name:
                return True
        return False

    def __len__(self):
        return len(self.nodes)

    def __repr__(self):
        data_path_var = self.data_path if self.data_path else ""
        coords_path_var = self.coords_path if self.coords_path else ""
        sep_var = ", " if self.coords_path and self.data_path else ""
        args = f'{data_path_var}{sep_var}{coords_path_var}'
        return f'Graph({args})'

    def __str__(self):
        string = ''
        count = 0
        for node in self.nodes:
            string += str(node)
            if count != len(self) - 1:
                string += '\n'
            count += 1

        return string


class GraphNode:
    def __init__(self, name, neighbors=None, x=None, y=None):
        if neighbors is None:
            neighbors = []
        self.name = name
        self.neighbors = neighbors
        self.x = x
        self.y = y

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def get_neighbors(self):
        return self.neighbors

    def has_neighbor(self, neighbor_node):
        for neighbor in self.neighbors:
            if neighbor[0] == neighbor_node.name:
                return True
        return False

    def get_xy(self):
        return self.x, self.y

    def __repr__(self):
        return f'GraphNode("{self.name}", {self.neighbors}, {self.x}, {self.y})'

    def __str__(self):
        return f'{self.name}: {self.neighbors} -- ({self.x}, {self.y})'
