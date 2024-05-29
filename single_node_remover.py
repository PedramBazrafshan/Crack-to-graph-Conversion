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


from functions import *
from adjacency_matrix import *


def single_node_remover (nodes, edges_dict):
    ####################### removing single nodes
    adj_matrix = adj_mat(nodes, edges_dict)
    k, k_w = nodeDegree(adj_matrix)
    node_to_remove = []
    for idx_node, item_node in enumerate(nodes):
        if k[idx_node] == 0:
            node_to_remove.append(item_node)

    for item in node_to_remove:
        nodes.remove(item)
        
    nodes_dict = list2dict(nodes)
    
    return nodes, nodes_dict