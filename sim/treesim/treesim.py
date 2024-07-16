"""The tree simulator.
"""

import numpy as np

from envutils import stepper


class Node:
    def __init__(self, state: np.array, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.level = 0 if parent is None else parent.level + 1
    
    def add_child(self, state: np.array):
        child = Node(state, parent=self)
        self.children.append(child)
        return child
    
    def delete_node(self):
        for child in self.children:
            child.delete_node()
        self.parent.children.remove(self)


class TreeSim:
    @staticmethod
    def remove(node: Node, value, level, nodes):
        if not node.children:
            if node.state[9][9] != value:
                node.delete_node()
                nodes[level].remove(node)
                return
        for child in node.children:
            TreeSim.remove(child, value, level + 1, nodes)
        for child in node.children:
            if not child.children:
                child.delete_node()
                nodes[level+1].remove(child)
        
    def __init__(self, init_state: np.array, timespan: int, actors: dict):
        self.tree = Node(init_state)
        self.timespan = timespan
        self.actors = actors
        self.current_time = 0
        self.nodes = {0: [self.tree]}

    def _step(self):
        self.current_time += 1
        self.nodes[self.current_time] = []
        for node in self.nodes[self.current_time-1]:
            new_state = stepper(node.state, self.actors)
            self.nodes[self.current_time].append(node.add_child(new_state.copy()))
            for actor_id in self.actors.keys():
                temp_state = new_state.copy()
                temp_state[0][0] = actor_id
                self.nodes[self.current_time].append(node.add_child(temp_state))
        if self.current_time >= 5:
            for node in self.nodes[self.current_time - 5]:
                self.remove(node, node.state[0, 0] and (np.sum(node.state) > 1), self.current_time - 5, self.nodes)

    def run(self):
        for _ in range(self.timespan):
            self._step()
