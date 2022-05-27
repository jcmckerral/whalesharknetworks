import random 
from collections import Counter

import numpy as np

def get_degree_preserving_randomization(edges):
    '''
    Randomizes a network provided by an edge list 
    producing neither self links nor duplicate links.
    The degree sequence will stay the same.
    INPUT:
    --- edges: list or set containing node pairs (tuples or lists of two nodes)
         
    OUTPUT:
    --- new_edges: new list containing new node pairs (tuples of two nodes)
    '''
    
    # make new set copy from edgelist
    edges = set( [tuple(e) for e in edges ]) 

    # get list of stubs
    stubs = [ ]
    [ stubs.extend(e) for e in edges ]

    # get a Counter object that counts the stubs for every node
    stub_counter = Counter(stubs)

    # initialize the new edge list
    new_edges = set()

    # get available nodes (nodes that have nonzero stub count)
    nodes = np.array([ stub for stub,count in stub_counter.items() if count!=0 ])

    # loop till the number of available nodes is zero
    while len(nodes)>0:

        # initialize dummy values for new edge
        first,second = -1,-1

        # choose edges that are not self-links (only possible if len(nodes)>1)
        while first == second and len(nodes)>1:
            first,second = np.random.choice(nodes,size=(2,),replace=False)

        # if the chosen (source,target) is are not the same
        # and not yet connected 
        # and there is more than one node with available stubs
        if first!=second and \
           (first,second) not in new_edges and \
           (second,first) not in new_edges and \
           len(nodes)>1:
            new_edges.add((first,second))
            stub_counter[first] -= 1
            stub_counter[second] -= 1
        else:
            # if not, pop a random edge and put its nodes 
            # back in the stub pool
            edge = random.sample(new_edges,1)[0]
            new_edges.remove(edge)
            stub_counter[edge[0]] += 1
            stub_counter[edge[1]] += 1

        # get available nodes (nodes that have nonzero stub count)
        nodes = np.array([ stub for stub,count in stub_counter.items() if count!=0 ])

        
    return list(new_edges)