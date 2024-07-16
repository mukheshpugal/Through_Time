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
    return i < (state.shape[0] - 2 + (np.sum(state) > 1)), j < (state.shape[1] - 2 + (np.sum(state) > 1))


if __name__ == "__main__":
    # Some simple tests
    state = np.zeros((10, 10), dtype=np.int32)
    state[0, 0] = 1
    actors = {1: simple_green_brain}

    tree_sim = TreeSim(state, 8, actors)
    tree_sim.run()

    import matplotlib.pyplot as plt
    import networkx as nx
    import numpy as np

    def plot_tree(root):
        def add_edges(node, G, pos=None, x=0, y=0, layer=1):
            if pos is None:
                pos = {}
            pos[node] = (x, y)
            for i, child in enumerate(node.children):
                child_x = x - 1/(layer+1) + 2*i/(layer+1)
                child_y = y - 1
                G.add_edge(node, child)
                pos = add_edges(child, G, pos=pos, x=child_x, y=child_y, layer=layer+1)
            return pos

        G = nx.DiGraph()
        pos = add_edges(root, G)
        labels = {node: node.state for node in G.nodes}
        colors = ["green" if node.state[0, 0] else 'black' for node in G.nodes]

        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, labels=labels, with_labels=True, node_size=100, node_color=colors, font_size=10, font_color='black', font_weight='bold', edge_color='gray')
        plt.title('Tree Structure')
        plt.show()
    plot_tree(tree_sim.tree)