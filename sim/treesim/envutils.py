"""Utiliy classes and functions for the environment.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import PIL.Image as Image
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


def state_to_image(state, actors, size=600, as_array=False):
    surface = pygame.surface.Surface((size, size))
    surface.fill((255, 255, 255))

    # Draw grid lines
    for i in range(state.shape[0] + 1):
        pygame.draw.line(surface, (200, 200, 200), (0, i * size // state.shape[0]), (size, i * size // state.shape[0]), 3)
    for i in range(state.shape[1] + 1):
        pygame.draw.line(surface, (200, 200, 200), (i * size // state.shape[1], 0), (i * size // state.shape[1], size), 3)

    # Draw portal
    pygame.draw.circle(surface, (200, 200, 200), (size - size // state.shape[1] // 2, size - size // state.shape[0] // 2), 0.6 * size // state.shape[1] // 2)
    pygame.draw.circle(surface, (0, 0, 0), (size - size // state.shape[1] // 2, size - size // state.shape[0] // 2), 0.5 * size // state.shape[1] // 2)

    # Draw actors
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            id = state[i, j]
            if id:
                center = ((j + 0.5) * size / state.shape[1], (i + 0.5) * size / state.shape[0])
                square_size = size * 0.8 // state.shape[1]
                # Draw a rounded square
                pygame.draw.rect(surface, actors[id].color, (center[0] - square_size / 2, center[1] - square_size / 2, square_size, square_size), border_radius=int(square_size / 5))
    if as_array:
        return pygame.surfarray.array3d(surface)
    return Image.fromarray(pygame.surfarray.array3d(surface))


def stepper(state: np.array, actors: dict, verbose: bool = False):
    """Simulate one step of the environment."""
    new_state = np.zeros_like(state)
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            if state[i, j] in actors:
                dx, dy = actors[state[i, j]](state, i, j)
                if verbose:
                    print(
                        f"Actor {state[i, j]} at ({i}, {j}) wants to move to ({i + dx}, {j + dy}) and {'will' if (i + dx, j + dy) == (9, 9) else 'will not'} travel."
                    )
                if (i, j) != (9, 9):
                    new_state[i + dx, j + dy] = state[i, j]
    if verbose:
        print(f"New state:\n{new_state}")
    return new_state


def get_image(state, size=5, as_array=False):
    img = 255 * np.ones((10 * size + 1, 10 * size + 1, 3), dtype=np.uint8)
    if state[0, 0] != 0 or state[9, 9] != 0:
        img[:, :] = [128, 128, 128]
        if state[0, 0]:
            img[:, :, 1] = 255
        if state[9, 9]:
            img[:, :, 0] = 255
    for i in range(11):
        img[size * i, :, :] = 0
        img[:, size * i, :] = 0

    circle = 255 * np.ones((size - 1, size - 1), dtype=np.uint8)
    center = (size - 1) // 2
    x = np.arange(size - 1)
    y = np.arange(size - 1)
    X, Y = np.meshgrid(x, y)
    distances = np.sqrt((X - center) ** 2 + (Y - center) ** 2)
    circle[distances <= center] = 0

    img[size * 0 + 1 : size * 1, size * 0 + 1 : size * 1, 0] = circle
    img[size * 0 + 1 : size * 1, size * 0 + 1 : size * 1, 2] = circle
    img[size * 9 + 1 : size * 10, size * 9 + 1 : size * 10, 1] = circle
    img[size * 9 + 1 : size * 10, size * 9 + 1 : size * 10, 2] = circle

    for i in range(10):
        for j in range(10):
            id = state[i, j]
            if id:
                img[size * i + 1 : size * (i + 1), size * j + 1 : size * (j + 1), :] = 0
    if as_array:
        return img
    return Image.fromarray(img)


def plot_tree(root):
    def add_edges(node, G, pos=None, x=0, y=0, layer=1):
        if pos is None:
            pos = {}
        pos[node] = (x, y)
        for i, child in zip(np.linspace(-1, 1, len(node.children)), node.children):
            child_x = x + (0 if len(node.children) == 1 else i)  / 10#/ (layer + 1)
            child_y = y - 1
            G.add_edge(node, child)
            pos = add_edges(child, G, pos=pos, x=child_x, y=child_y, layer=layer + 1)
        return pos

    G = nx.DiGraph()
    pos = add_edges(root, G)
    fig, ax = plt.subplots()
    nx.draw_networkx_edges(G, pos=pos, ax=ax, arrows=True, arrowstyle="-", min_source_margin=15, min_target_margin=15)
    icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.03
    icon_center = icon_size / 2.0
    for node in G.nodes:
        xf, yf = ax.transData.transform(pos[node])
        xa, ya = fig.transFigure.inverted().transform((xf, yf))
        a = plt.axes([xa - icon_center, ya - icon_center, icon_size, icon_size])
        a.imshow(get_image(node.state, 5))
        a.axis("off")
    ax.set_title("Timeline tree")
    ax.axis("off")
    plt.show()


def make_movie(tree, actors):
    import cv2

    for i, node in enumerate(tree.get_leaves()):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        Path("outputs").mkdir(exist_ok=True)
        out = cv2.VideoWriter(f"outputs/path_{i+1}.mp4", fourcc, 1, (600, 600))
        images = []
        while node is not None:
            img = state_to_image(node.state, actors, as_array=True)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            images.append(img)
            node = node.parent
        [out.write(img) for img in images[::-1]]
        out.release()
