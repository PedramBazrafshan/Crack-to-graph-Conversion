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


import cv2
import numpy as np
from functions import *

def Corner_Detection (thinned, ker_size):
    #################################### Corner Detection Using Shi-Tomasi
    nodes = cv2.goodFeaturesToTrack(thinned, 5000, 0.1, None)
    
    ###### Set the needed parameters to find the refined corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_COUNT, 40, 0.001)
    ###### Calculate the refined corner locations
    nodes = cv2.cornerSubPix(thinned, nodes, (ker_size, ker_size), (-1,-1), criteria)  # Corners will be centered within a 5by5 window
    
    nodes = np.int0(nodes)
    nodes = [xy for N_i in nodes for xy in N_i]
    
    nodes = np.asarray(nodes)
    nodes = nodes.tolist()
    
    ######## Removing duplicate nodes
    buf_node = []
    for elem in nodes:
        if elem not in buf_node:
            buf_node.append(elem)
    nodes = buf_node
    
    ########################### Are the detected corners actually within the black pixels or might be on the edge within the white pixels?
    bl_pix_fin = np.where((thinned[:,:] == 0))
    
    temp_l = []
    for i in range(len(bl_pix_fin[0])):
        temp_l.append([bl_pix_fin[1][i], bl_pix_fin[0][i]])
        
    for i in range(len(nodes)):
        if (nodes[i] not in temp_l):
            temp_l = sortByDistance(temp_l, nodes[i])
            nodes[i] = temp_l[0]

    ############ Removing extra nodes in a ker_size by ker_size window
    half = int((ker_size - 1 ) / 2)
    b = [*range(-half, half+1, 1)]
    center = int(((ker_size * ker_size) - 1) /2)
    for node_item in nodes:
        window = []
        for i in b:
            for j in b:
                window.append([node_item[0]+i, node_item[1]+j])
        
        window.remove(window[center])   # removing the center of the created window which is the node itself
        for window_item in window:
            if window_item in nodes:
                nodes.remove(window_item)
    
    nodes_dict = list2dict(nodes)
    
    return nodes, nodes_dict