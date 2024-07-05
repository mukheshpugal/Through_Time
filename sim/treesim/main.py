from treesim import TreeSim
import numpy as np


def simple_green_brain(state: np.array, i: int, j: int):
    """Simple brain for green actor.
    
    The green actor will move to the bottom right corner always. It will travel if there is another actor at current time. If there is no actor, it will stay put.

    Args:
        state (np.array): The current state of the environment.
        i (int): The row index of the actor.
        j (int): The column index of the actor.
    
    Returns:
        tuple: The change in x, change in y, and whether the actor should travel.
    """
    return i < state.shape[0] - 1, j < state.shape[1] - 1, i == state.shape[0] - 1 and j == state.shape[1] - 1 and np.sum(state) > 1


if __name__ == "__main__":
    # Some simple tests
    state = np.zeros((10, 10), dtype=np.int32)
    state[0, 0] = 1
    actors = {1: simple_green_brain}

    # tree_sim = TreeSim(state, 30, actors)
    # tree_sim.run()

    from envutils import stepper

    # Lonely actor
    for _ in range(30):
        state = stepper(state, actors, verbose=True)
    
    # Traveling actor
    for i in range(30):
        state = stepper(state, actors, verbose=True)
        if i % 5 == 0:
            state[0, 0] = 1
