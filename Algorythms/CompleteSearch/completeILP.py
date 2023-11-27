from sage.all import *
from random import *
import sys

########################################################################################
#                           COMPLETE SEARCH USING ILP                                  #
########################################################################################

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
    # We are not interested in the smallest possible number of colors, 
    # it is only important to satisfy the conjecture
    p.add_constraint(t[0] >= maxCol)
    
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
        print(f'BINGO! The graph {G} doesnt have a rich-neighbor edge coloring! \n' +
              f'Edges:{G.edges()}; \n' + 
              f'Adjacency matix: {G.adjacency_matrix()}; \n'
              f'Neighbors: {G.neighbors()}')  
        return False, False
    return colors, richEdges

#--------------------------------------------------------------------------------------#

def checkColoring(G, coloring, richEdges):
    """
    Checks if the coloring of the graph is a rich-neighbor edge coloring.
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
  
c = 0
for graph in sys.stdin:
        c += 1
        if c % 100 == 0:
            print(f'Graphs checked so far: {c}')

        G = Graph(graph)
        
        # Run ILP
        colors, richEdges = richNeighbor(G)
        if colors == False:
            continue

        # Check if the coloring is valid
        if c % 100 == 0:
            if not checkColoring(G, colors, richEdges):
                print('ILP failed to find a valid coloring! \n' +
                      f'Edges:{G.edges()}; \n' + 
                      f'Adjacency matix: {G.adjacency_matrix()}; \n'
                      f'Neighbors: {G.neighbors()}')





