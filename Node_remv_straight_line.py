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


import math
from functions import *
from adjacency_matrix import *

def Node_remv_straight_line(nodes, edges_dict, edges, ang_bet_lines):

    ######### Removing the node btween two roughly straight lines
    # convert dictionary of edges to connectivity (adjacency) matrix
    adj_matrix = adj_mat(nodes, edges_dict)
    
    k, k_w = nodeDegree(adj_matrix)
    
    twoDegree_cord = []
    for idx_node, item_node in enumerate(nodes):
        if k[idx_node] == 2:
            x1 = item_node[0]
            y1 = item_node[1]
            
            V_lst = []
            for edges_item in edges.values():
                if item_node == edges_item[0] or item_node == edges_item[1]:
                
                    if edges_item[1] != item_node:
                        x2 = edges_item[1][0]
                        y2 = edges_item[1][1]
                    else:
                        x2 = edges_item[0][0]
                        y2 = edges_item[0][1]
                    
                    V_lst.append([(x1 - x2), (y1 - y2)])
                    
            def dot(vA, vB):
                return vA[0]*vB[0]+vA[1]*vB[1]
            
            # Get vector form
            vA = V_lst[0]
            vB = V_lst[1]
            # Get dot prod
            dot_prod = dot(vA, vB)
            # Get magnitudes
            magA = dot(vA, vA)**0.5
            magB = dot(vB, vB)**0.5
            # Get cosine value
            cos_ = dot_prod/magA/magB
            # Get angle in radians and then convert to degrees
            angle = math.acos(round(cos_,3))
            # Basically doing angle <- angle mod 360
            ang_deg = math.degrees(angle)%360
        
            if ang_deg-180>=0:
                ang_deg = 360 - ang_deg
                        
            if ang_deg > ang_bet_lines:
                twoDegree_cord.append(item_node)
    
    
    for item in twoDegree_cord:
        nodes.remove(item)
        
    nodes_dict = list2dict(nodes)    

    return nodes, nodes_dict