# Tree simulator

The tree simulator produces valid non-paradoxical solutions (if any exists) for the provided combinantion of actor characteristics, initial state and time travel rules.

## Brief overview

The simulator produces a "tree" where each node represents a state of the world and the children of the node are the possible states that result from the branching of the timeline due to time travel. The tree will be expanded level by level until the simulation timespan is reached. Each new node formed, when subjected to the laws of the environment, may confirm/disprove the existence of an ancestor node thus pruning the tree from forming paradoxical paths. Each path from the root of the final tree to the leaves represents a valid non-paradoxical solution.
