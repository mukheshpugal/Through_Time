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
        self.parent.children.remove(self)

    def get_leaves(self):
        if not self.children:
            return [self]
        leaves = []
        for child in self.children:
            leaves.extend(child.get_leaves())
        return leaves


class TreeSim:
    def __init__(self, init_state: np.array, timespan: int, actors: dict):
        self.tree = Node(init_state)
        self.timespan = timespan
        self.actors = actors
        self.nodes = {0: [self.tree]}
        self.travel_time = 5

    def run(self):
        for current_time in range(1, self.timespan + 1):
            self.nodes[current_time] = []
            # Adding
            for node in self.nodes[current_time - 1]:
                new_state = stepper(node.state, self.actors)
                self.nodes[current_time].append(node.add_child(new_state.copy()))
                if current_time < self.timespan - self.travel_time:
                    for actor_id in self.actors.keys():
                        temp_state = new_state.copy()
                        temp_state[0, 0] = actor_id
                        self.nodes[current_time].append(node.add_child(temp_state))
            # Pruning
            if current_time > self.travel_time:
                for node in self.nodes[current_time - self.travel_time]:
                    for leaf in node.get_leaves():
                        if leaf.level == current_time and leaf.state[9, 9] != node.state[0, 0]:
                            leaf.delete_node()
                            self.nodes[current_time].remove(leaf)

        # Tree cleanup
        for level in range(self.timespan - 1, 0, -1):
            unwanted_nodes = [node for node in self.nodes[level] if not node.children]
            for node in unwanted_nodes:
                node.delete_node()
                self.nodes[level].remove(node)

        return self.tree
