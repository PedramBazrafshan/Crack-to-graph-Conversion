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
from Corner_Connection import *
import numpy as np

def arch_match (nodes_dict, img_base, nodes, edges_dict, edges, img3):
    # Search parameters
    actions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    margin = 1
    
    nodes_to_add = []
    for item in edges.values():
        # print('item = ', item)
        point = item[0]      # item[1] is the coordinates in the dictionary format like [947,598] in nodes_dict = {'0': [947,598]}
        goal = item[1]
        frontier = [[0,[],point]]
        explored = []
        
        found = False
        entry_number = 1
        while not found and len(frontier)>0:
            frontier.reverse()
            candidate = frontier.pop()
            frontier.reverse()
            previous_loc = candidate[1]
            candidate_loc = candidate[2]
            explored.append([previous_loc,candidate_loc])
            if candidate_loc == goal:
                found = True
            for action in actions:
                next_loc = [candidate_loc[0]+action[0],candidate_loc[1]+action[1]]
                if img_base.shape[0] - margin > next_loc[1] > 0 + margin and img_base.shape[1] - margin > next_loc[0] > 0 + margin:
                    if img_base[next_loc[1]][next_loc[0]] != 255:
                        frontier_loc = [item[2] for item in frontier]
                        explored_loc = [item[1] for item in explored]
                        if next_loc not in explored_loc and next_loc not in frontier_loc:
                            frontier.append([entry_number,candidate_loc,next_loc])
                            entry_number =+ 1
    
        if found:
            # print('found')
            path = [explored[-1][1]]
            previous = explored[-1][0]
            explored_loc = [item[1] for item in explored]
            while previous:
                path.append(previous)
                previous_index = explored_loc.index(previous)
                previous = explored[previous_index][0]
            path.reverse()
            if point not in path:
                path.append(point)
            if goal not in path:
                path.append(goal)
        else:
            print('not found')
        
        ## For each edge, the algorithm calculates the length of the edge and the length of the crack pattern.
        ## The algorithm checks to see if the length of the crack pattern is more than the length of the edge based on a threshold.
        ## The perpendicular ditance between the edge and the crack pattern is calculated pixel by pixel. The pixel with the greater distance
        ## is selected to add a corner there, and reconnect the edges to refine the graph representation.
        arch = 0
        for i in range(len(path)):
            if i == (len(path)-1):
                break
            arch = arch + np.sqrt(np.square(path[i][0] - path[i+1][0]) + np.square(path[i][1] - path[i+1][1]))
            
        straight = distance(point, goal)
        
        perpendicular_dist = []
        dif_goal_point = [point[0]-goal[0], point[1]-goal[1]]
        for item_pix in path:
            dif_point_pix = [point[0]-item_pix[0], point[1]-item_pix[1]]
            perpendicular_dist.append(np.linalg.norm(np.cross(dif_goal_point, dif_point_pix))/np.linalg.norm(dif_goal_point))
        
        if (straight <= 0.92 * arch and straight >= min(0.05*img_base.shape[0], 0.05*img_base.shape[1]))\
            or (max(perpendicular_dist) >= min(0.02*img_base.shape[0], 0.02*img_base.shape[1])):
            
            nodes_to_add.append(path[perpendicular_dist.index(max(perpendicular_dist))])
            
    
    nodes.extend(nodes_to_add)
    nodes_dict = list2dict(nodes)
    edges_dict, edges, nodes_dict, nodes = Corner_Connection(nodes_dict, img_base, nodes)

    return edges_dict, edges, nodes_dict, nodes