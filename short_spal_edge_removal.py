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
import numpy as np


def short_spal_edge_removal(nodes, edges_dict, edges, thinned, img_spal, kernel_spal):
    ######### Removing the node btween two roughly straight lines
    adj_matrix = adj_mat(nodes, edges_dict)
    k, k_w = nodeDegree(adj_matrix)

    spal_pix_loc = np.where((img_spal[:,:] == 0))
    spal_pix = []
    for i in range(len(spal_pix_loc[0])):
        spal_pix.append([spal_pix_loc[1][i], spal_pix_loc[0][i]])
    
    
    node_to_remove = []
    for idx_node, item_node in enumerate(nodes):
        if item_node in spal_pix and k[idx_node] == 1:
    
            for edges_idx, edges_item in edges.items():
                if item_node == edges_item[0] or item_node == edges_item[1]:
                    if edges_item[1] != item_node:
                        x2y2 = edges_item[1]
                    else:
                        x2y2 = edges_item[0]
                    if distance(item_node, x2y2) < min(0.03*thinned.shape[0], 0.03*thinned.shape[1]) and item_node not in node_to_remove:
                    # if item_node not in node_to_remove:
                        node_to_remove.append(item_node)

    ######## Removing nodes with degree = 1
    for item in node_to_remove:
        nodes.remove(item)

    nodes_dict = list2dict(nodes)    

    return nodes, nodes_dict