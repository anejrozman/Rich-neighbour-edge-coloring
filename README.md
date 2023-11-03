# Rich-neighbour-edge-coloring
Project for the course Financial lab

In an edge coloring, an edge $e$ is called $rich$ if all edges adjacent to $e$ have different colors. An edge coloring is called a $rich-neighbour \ edge \ coloring$ if every edge is adjacent to some rich edge. The smallest number of colors for which there exists such a coloring is denoted by $X_{rn}'(G)$. For example $X_{rn}'(K_4)=6$. 

We want to verify the following conjecture:
$$For \ every \ graph \ G \ of \ maximum \ degree \ \Delta, X_{rn}'(G) \leq 2\Delta - 1 \ holds.$$

We implement the coloring and apply the tests to verify the above conjecture fo regular graphs of degree $\Delta \geq 4$. For small graphs we do it ... , for larger graphs we apply a random search ...
For our code base we use Cocalc: https://cocalc.com/projects/bc655648-a5d9-4e01-b8f6-05c82fde0f58/files/
