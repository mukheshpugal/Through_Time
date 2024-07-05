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


class TreeSim:
    def __init__(self, init_state: np.array, timespan: int, actors: dict):
        self.tree = Node(init_state)
        self.timespan = timespan
        self.actors = actors
        self.current_time = 0
    
    def _step(self):
        self.current_time += 1

    def run(self):
        for _ in range(self.timespan):
            self._step()
