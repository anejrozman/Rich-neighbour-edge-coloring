# Rich-neighbour-edge-coloring
Project for the course Financial lab

In an edge coloring, an edge $e$ is called $rich$ if all edges adjacent to $e$ have different colors. An edge coloring is called a $rich-neighbour \ edge \ coloring$ if every edge is adjacent to some rich edge. The smallest number of colors for which there exists such a coloring is denoted by $X_{rn}'(G)$. For example $X_{rn}'(K_4)=6$. 

We want to verify the following conjecture:
$$For \ every \ graph \ G \ of \ maximum \ degree \ \Delta, X_{rn}'(G) \leq 2\Delta - 1 \ holds.$$

In our paper we implement an integer linear program for verifying the above conjecture for $K$-regular graphs on $N$ vertices where $N > K\geq 4$. 

## Main documents:
- `completeILP.py` is a specific sage file that takes a .txt file as its input and expects that each line in said file contains a sage graph object. It then iterates over the file and checks each graph if it has a rich-neighbor edge coloring, in case it finds a counterexample it outputs "BINGO" and the graph's adjacency matrix in the terminal.

- `randomILP.py` is a sage file that takes in two inputs, K for graph regularity, and N for the number of vertices. It then generates a random K-regular graph on N vertices and ...

