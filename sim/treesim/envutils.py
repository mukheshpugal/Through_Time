"""Utiliy classes and functions for the environment.
"""

import numpy as np


def stepper(state: np.array, actors: dict, verbose: bool = False):
    """Simulate one step of the environment."""
    new_state = np.zeros_like(state)
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            if state[i, j] in actors:
                dx, dy = actors[state[i, j]](state, i, j)
                if verbose:
                    print(f"Actor {state[i, j]} at ({i}, {j}) wants to move to ({i + dx}, {j + dy}) and {'will' if (i + dx, j + dy) == (9, 9) else 'will not'} travel.")
                if (i, j) != (9, 9):
                    new_state[i + dx, j + dy] = state[i, j]
    if verbose:
        print(f"New state:\n{new_state}")
    return new_state
