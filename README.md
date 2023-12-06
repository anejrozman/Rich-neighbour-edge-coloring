# Rich-neighbour-edge-coloring
Project for the course Financial lab

In an edge coloring, an edge $e$ is called $rich$ if all edges adjacent to $e$ have different colors. An edge coloring is called a $rich-neighbour \ edge \ coloring$ if every edge is adjacent to some rich edge. The smallest number of colors for which there exists such a coloring is denoted by $X_{rn}'(G)$. For example $X_{rn}'(K_4)=6$. 

We want to verify the following conjecture:
$$For \ every \ graph \ G \ of \ maximum \ degree \ \Delta, X_{rn}'(G) \leq 2\Delta - 1 \ holds.$$

In our paper we implement an integer linear program for verifying the above conjecture for $K$-regular graphs on $N$ vertices where $N > K\geq 4$. 

## Main files:
- `LongPresentation.pdf` is a paper which explains the algorthms used for checking the validity of the rich-neighbor edge coloring conjecture and interprets our results. 

- `completeILP.py` is a SageMath file where we implemented our algorythms for checking specific classes of graphs for exapmple all 4-regular graphs on 10 vertices.

- `randomILP.py` is a SageMath file where we implemented our algorythms for randomly checking larger graphs where it is impossible to check each one individually.

## Instructions for use
To run our files you need `SageMath 9.3`. Link for installation: [Download SageMath](https://www.sagemath.org/)

- `completeILP.py` The file requires an input in the form of a .txt file that contains a sage graph object in each line (see example files in folder `exampleFiles`). It then iterates over the file and:
    - if it finds a counterexample for the rich-neighbor edge coloring conjecture it outputs "BINGO" and the graph's adjacency matrix and its representation as a list of neighbors.
    - if a counterexapmle isn't found it outputs "done" when it finishes checking all the graphs in the input file

Command for runnign in terminal: `sage completeILP.py inputFile.txt`

- `randomILP.py` The file requires an input in the form of two numbers $N$ and $K$ for the number of vertices and the regularity of the graph it generate at the start of its iteration. The file contains an infinite loop where it continually checks a graph and randomly tweaks it.
    - if it finds a counterexapmle it outputs "BINGO" and the graph's adjacency matrix and its representation as a list of neighbors.
    - To stop the execution of the file you have to manually interrupt it

Command for running in terminal: `sage randomILP.py N K`


## Authors
Anej Rozman and Tanja Luštrek

## Advisers
Assistant Professor Janoš Vidali and Professor Riste Škrekovski



