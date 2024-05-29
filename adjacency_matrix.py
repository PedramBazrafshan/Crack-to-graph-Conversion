#######################################################
"""""""""""
Python program to create crack graph from crack surface
using Shi-Tomasi corner detection algorithm
and pixel tracking algorithm
by: Pedram Bazrafshan
"""""""""""
#######################################################


#######################################################
"""""""""""
Please cite the paper below if you use this code:
Bazrafshan, P., On, T., Basereh, S., Okumus, P., & Ebrahimkhanlou, A. (2024). A graph‐based method for quantifying crack patterns on reinforced concrete shear walls. Computer‐Aided Civil and Infrastructure Engineering, 39(4), 498-517.
"""""""""""
#######################################################


import numpy as np

def adj_mat(nodes, edges_dict):
    # convert dictionary of edges to connectivity (adjacency) matrix
    adj_matrix = np.zeros((len(nodes), len(nodes)))       # initiate the connectivity matrix with zeros
    for V in edges_dict.values():
        # print("V = ", V)
        # print("eval(V[0]) = ", eval(V[0]))
        adj_matrix[eval(V[0])][eval(V[1])] = V[2]
        adj_matrix[eval(V[1])][eval(V[0])] = V[2]
    
    return adj_matrix