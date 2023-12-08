from sage.all import *
from random import *
import sys

########################################################################################
#                           RANDOM SEARCH USING ILP                                    #
########################################################################################

# Access command-line arguments
if len(sys.argv) != 3:
    print("Usage: sage randomILP.py N K")
    sys.stdout.flush()
    sys.exit(1)

# Extract N and K from command-line arguments
N = int(sys.argv[1])
K = int(sys.argv[2])

# Generate a random graph
if (N * K) % 2 != 0 or N <= 0 or K <= 0 or K > N - 1:
    print('Invalid input for N and K. \n' +
          'N * K must be even \n' +
          'N and K must be positive \n' +
          'K must be less or equal to N - 1')
    sys.stdout.flush()
    
#--------------------------------------------------------------------------------------#

def generateGraph(N, K):
    """
    Generates a connected random K-regular graph with N vertices.
    """
    G = graphs.RandomRegular(K, N)
    while not G.is_connected():
        G = graphs.RandomRegular(K, N)
    return G

#--------------------------------------------------------------------------------------#

def richNeighbor(G):
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
    p.add_constraint(t[0] == maxCol)
    
    # Each edge is colored exactly one color
    for e in G.edges(labels = False):
        p.add_constraint(sum([x[Set(e), i] for i in range(1, maxCol + 1)]) == 1)
        
    # Each edge e has at least one neighboring edge that is rich 
    for u,v in G.edges(labels = False):
        p.add_constraint(sum([y[Set((u, j))] for j in G[u]]) + 
                         sum([y[Set((l, v))] for l in G[v]]) - 
                         2*y[Set((u, v))] >= 1)
        
    # Variable t (which respresents the number of colors used) 
    # has a lower bound of the smallest color
    for e in G.edges(labels = False):
        for i in range(1, maxCol + 1):
            p.add_constraint(i * x[Set(e), i] <= t[0])
            
    # Two edges that share a vertex cannot be the same color
    for i in range(1, maxCol + 1):
        for u,v in G.edges(labels = False):
            for w in G[u]:
                if w == v:
                    continue
                p.add_constraint(x[Set((u, v)), i] + 
                                 x[Set((u, w)), i] <= 1)
            for z in G[v]:
                if z == u:
                    continue
                p.add_constraint(x[Set((u, v)), i] + 
                                 x[Set((v, z)), i] <= 1)
                
    # If an edge e is rich, then the neighboring vertices have to be differnet colors
    for u, v in G.edges(labels=False):
        for w in G.neighbors(u):
            for z in G.neighbors(v):
                if w == v or z == u:
                    continue
                for i in range(1, maxCol + 1):
                    p.add_constraint(x[Set((u, w)), i] + 
                                     x[Set((v, z)), i] + 
                                     y[Set((u, v))] <= 2)
    try: 
        p.solve()
        colors = p.get_values(x)
        richEdges = p.get_values(y)
    except ValueError:
        print(f'BINGO! The graph does not have a rich-neighbor edge coloring that satisfies the conjecture! \n' +
              f'Edges:{G.edges()}; \n' + 
              f'Adjacency matix: {G.adjacency_matrix()}; \n'
              f'Neighbors: {G.neighbors()}')  
        sys.stdout.flush()
        return False, False
    return colors, richEdges

#--------------------------------------------------------------------------------------#

def tweak(graph):
    """
    Removes two random edges and adds two new edges while maintaining k-regularity.
    """
    G = graph.copy()
    
    # Remove two random edges 
    e1 = G.random_edge()
    u1, v1, extra1 = e1
    G.delete_edge(e1)
    
    e2 = G.random_edge()
    u2, v2, extra2 = e2
    G.delete_edge(e2)

    # Add two new edges while maintaining k-regularity
    p = random()
    if p < 0.5:
        try:
            G.add_edge(u1, u2)
            G.add_edge(v1, v2)
        except ValueError:
            pass
    else:
        try:
            G.add_edge(u1, v2)
            G.add_edge(v1, u2)
        except ValueError:
            pass
    
    if not G.is_connected():
        return tweak(graph)
    if not G.is_regular():
        return tweak(graph)
    return G

#--------------------------------------------------------------------------------------#

def checkColoring(G, coloring):
    """
    Checks if the coloring of the graph is a proper coloring.
    """
    # Check if the coloring is valid
    for v in G.vertices():
        col = set()
        for w in G.neighbors(v):
            for i in range(1, 2*G.degree()[0]):
                if coloring[(Set((v, w)), i)] == 1:
                    col.add(i)
        if len(col) != len(G.neighbors(v)):
            return False
    return True

#--------------------------------------------------------------------------------------#

def checkRichness(G, richEdges):
    """
    Checks if the coloring of the graph is a rich-neighbor edge coloring.
    """
    # Check for richness
    for u, v in G.edges(labels = False):
        S = 0
        for w in G.neighbors(u):
            if w == v:
                continue
            S += richEdges[Set((u, w))]
        for z in G.neighbors(v):
            if z == u:
                continue
            S += richEdges[Set((v, z))]
        if S == 0:
            return False
    return True 

#--------------------------------------------------------------------------------------#

print('start, N = ' + str(N) + ', K = ' + str(K))
sys.stdout.flush()
# Generate a random graph
G = generateGraph(N, K)

# Random search
c = 0
while True: 
    c += 1
    if c % 30 == 0:
        print(f'Number of iterations:{c}')
        sys.stdout.flush()

    # Run ILP
    colors, richEdges = richNeighbor(G)
    if colors == False:
        G = tweak(G)
        continue

    # Check if the coloring is valid
    if c % 100 == 0:
        if not checkColoring(G, colors) or not checkRichness(G, richEdges):
            print('ILP failed to find a valid coloring! \n' +
                  f'Edges:{G.edges()}; \n' + 
                  f'Adjacency matix: {G.adjacency_matrix()}; \n'
                  f'Neighbors: {G.neighbors()}')
            sys.stdout.flush()
        
    # Tweak graph
    G = tweak(G)

    if random() < 0.1/N:
        G = generateGraph(N, K)

  

