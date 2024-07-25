import numpy as np

from envutils import make_movie, plot_tree
from treesim import TreeSim


class SimpleActor:
    """Template for simple actor."""
    def __init__(self, color):
        self.color = color

    def brain(self, state: np.array, i: int, j: int):
        """The actor will move to the bottom right corner always. It will travel if there is another actor at current time. If there is no actor, it will stay put.

        Args:
            state (np.array): The current state of the environment.
            i (int): The row index of the actor.
            j (int): The column index of the actor.

        Returns:
            tuple: The change in x, change in y, and whether the actor should travel.
        """
        return i < (state.shape[0] - 2 + (np.sum(state) > 1)), j < (state.shape[1] - 2 + (np.sum(state) > 1))

    def __call__(self, state: np.array, i: int, j: int):
        return self.brain(state, i, j)


if __name__ == "__main__":
    # Some simple tests
    state = np.zeros((10, 10), dtype=np.int32)
    state[1, 1] = 1
    actors = {1: SimpleActor((0, 255, 0))}

    tree_sim = TreeSim(state, 25, actors)
    tree = tree_sim.run()

    plot_tree(tree)

    make_movie(tree, actors)
