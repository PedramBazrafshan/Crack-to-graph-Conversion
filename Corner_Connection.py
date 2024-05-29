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
import cv2
import matplotlib.pyplot as plt

def Corner_Connection (nodes_dict, img_base, nodes):
    # Search parameters
    actions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    margin = 1
    
    edges = dict()
    edges_dict = dict()
    e = 0
    for item in nodes_dict.items():
        point = item[1]      # item[1] is the coordinates in the dictionary format like [947,598] in nodes_dict = {'0': [947,598]}
        frontier = [point]
        explored = []
        while len(frontier) > 0:
            frontier.reverse()
            candidate = frontier.pop()
            frontier.reverse()
            explored.append(candidate)
            
            for action in actions:
                new_pos = [candidate[0]+action[0], candidate[1]+action[1]]
                if img_base.shape[0] - margin > new_pos[1] > 0 + margin and img_base.shape[1] - margin > new_pos[0] > 0 + margin:
                    if img_base[new_pos[1]][new_pos[0]] != 255:
                        if new_pos not in frontier and new_pos not in explored:
                            frontier.append(new_pos)
    
            if candidate in nodes and candidate != point:
                linked_index = getIndex(nodes_dict, candidate)
                if isRepeated(candidate, point, edges) == False:
                    edges[str(e)] = (point, candidate)
                    edges_dict[str(e)] = [point, candidate, distance(point, candidate)]
                    e += 1
    
                ignoreDirection(point, candidate, frontier, window=50)
                
    
    nodes_dict = list2dict(nodes)
    
    edges_dict = loc2idx(edges_dict, nodes_dict)
    return edges_dict, edges, nodes_dict, nodes