from __future__ import print_function
from multiprocessing.dummy.connection import families
import sys
from sage.all import *
from random import *
import time

########################################################################################
#                           COMPLETE SEARCH USING ILP                                  #
########################################################################################

def rnec(G):
    """
    ILP: G -> bool
    True if G satisfies the Rich-neighbor edge coloring conjecture,
    False otherwise.
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
    
    p.solve()
    rest = p.get_values(t)
    
    # The program returnes True, if the coloring satisfies the conjecture and False, if not
    return rest[0] <= maxCol


def cgraphs(N, K):
    """
    N, K -> None
    Checks all K-regular graphs on N vertices if they
    satisfy the Rich-neighbor edge coloring conjecture.
    """
    gen = graphs.nauty_geng(f'{N} -d{K} -D{K}')
    if not gen:
        print(f'No {K} regular graphs on {N} vertices exist.')
    for G in gen:
        if not rnec(G):
            print(f'The graph {G} doesnt have a rich-neighbor edge coloring! Hooray!')
            break
    print(f'All {K} regular graphs on {N} vertices satisfy our conjecture.')


def checkAll(N):
    """
    N -> None
    Checks all regular graphs up to N vertices if they satisfy the
    Rich-neighbor edge coloring conjecture.
    """
    for n in range(4, N + 1):
        for k in range(4, n):
            cgraphs(n, k)


########################################################################################
#                           COMPLETE SEARCH; ITERATIVE APPROACH                        #
########################################################################################

