#from sage.all import *
from random import *
import sys

########################################################################################
#                           RANDOM SEARCH USING ILP                                    #
########################################################################################

# Access command-line arguments
if len(sys.argv) != 3:
    print("Usage: python3 randomILP.py N K")
    sys.exit(1)

print(sys.argv)

# Extract N and K from command-line arguments
N = int(sys.argv[1])
K = int(sys.argv[2])

# Generate a random graph
if (N * K) % 2 != 0 or N <= 0 or K <= 0 or K > N - 1:
    print('Invalid input for N and K. \n' +
          'N * K must be even \n' +
          'N and K must be positive \n' +
          'K must be less than N - 1')

def generateGraph(N, K):
    """
    Generates a connected random K-regular graph with N vertices.
    """
    G = RandomRegular(K, N)
    while not G.is_connected():
        G = RandomRegular(K, N)
    return G

def rnec(G):
    """
    ILP checks if G satisfies the Rich-neighbor edge coloring conjecture
    """	
    # Set variables and objective function
    p = MixedIntegerLinearProgram(maximization = False)
    x = p.new_variable(binary = True)
    y = p.new_variable(binary = True)
    t = p.new_variable(integer = True)
    p.set_objective(t[0])
    
    # Max number of colors allowed
    maxCol = 2*G.degree()[0] - 1
    
    # Add constraints
    # We are not interested in the smallest possible number of colors, it is only important to satisfy the conjecture
    p.add_constraint(t[0] >= maxCol)
    
    # Each edge is colored exactly one color
    for e in G.edges(labels = False):
        p.add_constraint(sum([x[Set(e), i] for i in range(1, maxCol + 1)]) == 1)
        
    # Each edge e has at least one neighboring edge that is rich 
    for u,v in G.edges(labels = False):
        p.add_constraint(sum([y[Set((u, j))] for j in G[u]]) + sum([y[Set((l, v))] for l in G[v]]) - 2*y[Set((u, v))] >= 1)
        
    # Variable t (which respresents the number of colors used) has a lower bound of the smallest color
    for e in G.edges(labels = False):
        for i in range(1, maxCol + 1):
            p.add_constraint(i * x[Set(e), i] <= t[0])
            
    # Two edges that share a vertex cannot be the same color
    for i in range(1, maxCol + 1):
        for u,v in G.edges(labels = False):
            for w in G[u]:
                if w == v:
                    continue
                p.add_constraint(x[Set((u, v)), i] + x[Set((u, w)), i] <= 1)
            for z in G[v]:
                if z == u:
                    continue
                p.add_constraint(x[Set((u, v)), i] + x[Set((v, z)), i] <= 1)
                
    # If an edge e is rich, then the neighboring vertices have to be differnet colors
    for u, v in G.edges(labels=False):
        for w in G.neighbors(u):
            for z in G.neighbors(v):
                if w == v or z == u:
                    continue
                for i in range(1, maxCol + 1):
                    p.add_constraint(x[Set((u, w)), i] + x[Set((v, z)), i] + y[Set((u, v))] <= 2)
    try: 
        p.solve()
        colors = p.get_values(x)
        richEdges = p.get_values(y)
    except ValueError:
        print(f'BINGO! The graph {G} doesnt have a rich-neighbor edge coloring! \n' +
              f'Edges:{G.edges()}; \n' + 
              f'Adjacency matix: {G.adjacency_matrix()}; \n'
              f'Neighbors: {G.neighbors()}')  
        return False, False
    return colors, richEdges


def tweak(graph):
    """
    Removes two random edges and adds two new edges while maintaining k-regularity.
    """
    G = graph.copy()
    
    # Remove two random edges 
    e1 = G.random_edge()
    print(e1)
    u1, v1, extra1 = e1
    G.delete_edge(e1)
    
    e2 = G.random_edge()
    u2, v2, extra2 = e2
    G.delete_edge(e2)

    # Add two new edges while maintaining k-regularity
    p = random()
    if p < 0.5:
        G.add_edge(u1, u2)
        G.add_edge(v1, v2)
    else:
        G.add_edge(u1, v2)
        G.add_edge(v1, u2)
    
    if not G.is_regular():
        return tweak(graph)
    return G

