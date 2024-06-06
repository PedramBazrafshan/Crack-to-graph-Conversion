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
import matplotlib.pyplot as plt
from skimage.morphology import thin
from copy import deepcopy
import sys
sys.path.append("../../../")
from functions import *
import numpy as np
import csv
from Corner_Detection import *
from Corner_Connection import *
from Node_remv_straight_line import *
from short_spal_edge_removal import *
from adjacency_matrix import *
from single_node_remover import *
from arch_match import *


def crack_to_graph (wall_names):
    SAVE = True
    
    img_names = []
    i = 0
    for i in range(len(wall_names)):
        img_names.append(str(wall_names[i]))
    
    
    spalless_images = []
    for img_name in img_names:
        #################################### Loading The Data Using Matplotlib
        img = cv2.imread(img_name[1:10]+".bmp")[:,:,::-1]
        # plt.imshow(img, cmap = 'gray')
        # plt.xticks([])
        # plt.yticks([])
        # plt.show()
        
        #################################### RGB2Gray Using Matplotlib
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # plt.imshow(img_gray, cmap = 'gray')
        # plt.xticks([])
        # plt.yticks([])
        # plt.show()
    
        #################################### Defining kernel and padding size
        ker_size_spal = int(np.floor(min(0.01*img_gray.shape[0], 0.01*img_gray.shape[1])))
        if ker_size_spal % 2 == 0:
            ker_size_spal += 1
            
        ker_size_spal = max(ker_size_spal, 5)
        pad_size = 3*ker_size_spal + 1
        
        #################################### Binarization
        retval, img_bin = cv2.threshold(img_gray, 230, 255, cv2.THRESH_BINARY)
        # plt.imshow(img_bin, cmap = 'gray')
        # plt.xticks([])
        # plt.yticks([])
        # plt.show()
    
        #################################### Image Padding
        if img_bin.shape[0] % 2 == 1 and img_bin.shape[1] % 2 == 1:
            img_bin = cv2.copyMakeBorder(img_bin, pad_size, pad_size+1, pad_size+1, pad_size, cv2.BORDER_CONSTANT, value=255)
        elif img_bin.shape[0] % 2 == 0 and img_bin.shape[1] % 2 == 1:
            img_bin = cv2.copyMakeBorder(img_bin, pad_size, pad_size, pad_size+1, pad_size, cv2.BORDER_CONSTANT, value=255)
        elif img_bin.shape[0] % 2 == 1 and img_bin.shape[1] % 2 == 0:
            img_bin = cv2.copyMakeBorder(img_bin, pad_size, pad_size+1, pad_size, pad_size, cv2.BORDER_CONSTANT, value=255)
        else :
            img_bin = cv2.copyMakeBorder(img_bin, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_CONSTANT, value=255)
    
        # plt.imshow(img_bin, cmap = 'gray')
        # plt.xticks([])
        # plt.yticks([])
        # plt.show()
        
        #################################### Morphological Operations / Removing The Spalling Aea
        kernel_spal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ker_size_spal,ker_size_spal))
    
        img_spal = cv2.dilate(img_bin, kernel = kernel_spal, iterations=2)
        img_spal_subtract = cv2.erode(img_spal, kernel = kernel_spal, iterations=3)
        img_spal = cv2.erode(img_spal, kernel = kernel_spal, iterations=2)
        spalless = cv2.subtract(img_spal_subtract, img_bin)
        # plt.imshow(spalless, cmap = 'gray')
        # plt.xticks([])
        # plt.yticks([])
        # plt.show()
        
        spalless_images.append(spalless)
    
    
    # plt.imshow(spalless_images[6], cmap = 'gray')
    # plt.xticks([])
    # plt.yticks([])
    # plt.show()
    
    
    ii = 0
    for img_spalless in spalless_images:
        img_name = img_names[ii]
        ii += 1
        print('Image Name = ', img_name)
        # plt.imshow(img_spalless, cmap = 'gray')
        # plt.xticks([])
        # plt.yticks([])
        # plt.show()
        #################################### Image Thinning To Have One-Pixel-Width Crack Pattern
        thinned_spalless = thin(img_spalless)    # Thinning should be done on the black background image, and white cracks
        thinned_spalless = thinned_spalless.astype(np.uint8)
        # plt.imshow(thinned_spalless, cmap = 'gray')
        # plt.xticks([])
        # plt.yticks([])
        # plt.show()
        
        ##### Where are black and white pixels
        bl_pix_spal = np.where((thinned_spalless[:,:] == 0))
        wh_pix_spal = np.where((thinned_spalless[:,:] == 1))
    
        ##### Inverting white and black pixels
        thinned_spalless[bl_pix_spal] = [255]
        thinned_spalless[wh_pix_spal] = [0]
    
        plt.imshow(thinned_spalless, cmap = 'gray')
        plt.xticks([])
        plt.yticks([])
        plt.show()
        # print("#crack pixels initial = ", len(wh_pix_spal[0]))
        
        ################################### Image Pyramids
        ##### Down sampling the image
        ##### Generate Gaussian pyramid for the gray-scale image
        G = thinned_spalless.copy()
        gp_down = [G]
        for i in range(4):
            G = cv2.pyrDown(G)       # Should be performed on white background image with black crack pixels
            gp_down.append(G)
            # plt.imshow(G, cmap = 'gray')
            # plt.xticks([])
            # plt.yticks([])
            # plt.show()
            
        ##### Up sampling the  / this makes the crack patterns smooth / the jagedness of the cracks is faded
        gp_up = []
        for i in range(4,0,-1):    # range(start, stop, step)
            GE = cv2.pyrUp(gp_down[i])
            gp_up.append(GE)
            # plt.imshow(GE, cmap = 'gray')
            # plt.xticks([])
            # plt.yticks([])
            # plt.show()
    
        ##### Thinning the up-sampled image To Have One-Pixel-Width Crack Pattern
        gp_up_thinned = []
        for pyr in gp_up:
            retval, pyr = cv2.threshold(pyr, 250, 255, cv2.THRESH_BINARY)
            
            
            bl_pix_pyr = np.where((pyr[:,:] == 0))
            wh_pix_pyr = np.where((pyr[:,:] == 255))
            pyr[bl_pix_pyr] = [255]
            pyr[wh_pix_pyr] = [0]
    
            pyr = thin(pyr)
            pyr = pyr.astype(np.uint8)
    
            bl_pix_pyrfinal = np.where((pyr[:,:] == 0))
            wh_pix_pyrfinal = np.where((pyr[:,:] == 1))
            pyr[bl_pix_pyrfinal] = [255]
            pyr[wh_pix_pyrfinal] = [0]
            
            gp_up_thinned.append(pyr)
            
    
        ################################### Morphological Operations
        ker_size_morph = int(np.floor(min(0.004*img_gray.shape[0], 0.004*img_gray.shape[1])))
        if ker_size_morph % 2 == 0:
            ker_size_morph += 1
    
        ker_size_morph = max(ker_size_morph, 5)
        kernel_morph = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ker_size_morph,ker_size_morph))
        
        
        crack_pix_init_orig = len(wh_pix_spal[0])
        crack_pix_init_smooth = len(wh_pix_pyrfinal[0])
        # change_orig_smooth = ((abs(crack_pix_init_orig - crack_pix_init_smooth)/crack_pix_init_orig) * 100)
        
        change = -1
        i = 1
        while change < 15: # limiting the crack pattern smoothing to 15 %
            ################################ Erosion and Dilation
            ##### Binarizing the image
            retval, img_bin = cv2.threshold(gp_up_thinned[3], 250, 255, cv2.THRESH_BINARY)
            # plt.imshow(img_bin, cmap = 'gray')
            # plt.xticks([])
            # plt.yticks([])
            # plt.show()
            
            ##### Eroding the image
            img_erosion = cv2.erode(img_bin, kernel = kernel_morph, iterations = i)
            # plt.imshow(img_erosion, cmap = 'gray')
            # plt.xticks([])
            # plt.yticks([])
            # plt.show()
            
            ##### Dilating the image
            img_dilation = cv2.dilate(img_erosion, kernel = kernel_morph, iterations = i-2)
            # plt.imshow(img_dilation, cmap = 'gray')
            # plt.xticks([])
            # plt.yticks([])
            # plt.show()
            
            ##### Inverting the black and white pixels for the thinning process
            bl_pix_dil = np.where((img_dilation[:,:] == 0))
            wh_pix_dil = np.where((img_dilation[:,:] == 255))
            img_dilation[bl_pix_dil] = [255]
            img_dilation[wh_pix_dil] = [0]        
            # plt.imshow(img_dilation, cmap = 'gray')
            # plt.xticks([])
            # plt.yticks([])
            # plt.show()
        
            thinned = thin(img_dilation)
            thinned = thinned.astype(np.uint8)
        
            bl_pix_final = np.where((thinned[:,:] == 0))
            wh_pix_final = np.where((thinned[:,:] == 1))
            thinned[bl_pix_final] = [255]
            thinned[wh_pix_final] = [0]
            # plt.imshow(thinned, cmap = 'gray')
            # plt.xticks([])
            # plt.yticks([])
            # plt.show()
            
            crack_pix_fin = len(wh_pix_final[0])
            # change_orig = ((abs(crack_pix_init_orig - crack_pix_fin)/crack_pix_init_orig) * 100)
            change_smooth = ((abs(crack_pix_init_smooth - crack_pix_fin)/crack_pix_init_smooth) * 100)
            
            # print("Change = %", round(change,1))
            # print("i = ", i)
            change = change_smooth
            
            if i == 5: # limiting the crack pattern smoothing to 5 cycles
                break
            
            i = i + 1
            
    
        plt.imshow(thinned, cmap = 'gray')
        plt.xticks([])
        plt.yticks([])
        plt.show()
    
        
        bl_pix_fin = np.where((thinned[:,:] == 0))
        
        ##### percentage of change in the number of crack pixels due to morphological operations
        change = ((abs(crack_pix_init_orig - len(bl_pix_fin[0]))/crack_pix_init_orig) * 100)
        print(f"Crack Pixel Change = {round(change,1)}%")
        
        #################################### Deep Copy For Final Plot
        img1 = deepcopy(thinned)
        img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2RGB)
        img2 = deepcopy(thinned)
        img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2RGB)
    
        #################################### Corner Detection Using Shi-Tomasi
        nodes, nodes_dict = Corner_Detection(thinned, ker_size_morph)
        print("Corners are detected using the Shi-Tomasi algorithm!")
        
        #################################### Connecting Corners As Edges
        ang_bet_lines = 155
        while True:
            #################################### Connecting the Detected Corners As Edges
            edges_dict, edges, nodes_dict, nodes = Corner_Connection(nodes_dict, thinned, nodes)
            len_nodes_init = len(nodes)
            
            #################################### Refining connected corners with only two edges roughly straight
            ## If two edges are connected together and their in-between angle is close to 180 degrees, it means these edges can roughly be one
            ## straight edge. Therefore, the node between these edges will be removed.
            ## This is done in a while loop so to make sure no two straight lines are left.
            nodes, nodes_dict = Node_remv_straight_line(nodes, edges_dict, edges, ang_bet_lines)
            ang_bet_lines = min(ang_bet_lines, 175)
            ang_bet_lines = ang_bet_lines + 10
            ##### convert the nodes to a dictionary
            nodes_dict = list2dict(nodes)
        
            len_nodes_new = len(nodes)
            
            if len_nodes_new == len_nodes_init:
                break
        print("The initial graph representation is created!")
        
        ####################### Removing Single Nodes
        nodes, nodes_dict = single_node_remover (nodes, edges_dict)
        edges_dict, edges, nodes_dict, nodes = Corner_Connection(nodes_dict, thinned, nodes)
        print("Single nodes are removed!")
        
        # #################### Removing single degree nodes with length shorter than a threshhold
        # nodes, nodes_dict = short_spal_edge_removal(nodes, edges_dict, edges, thinned, img_spal, kernel_spal)
        # edges_dict, edges, nodes_dict, nodes = Corner_Connection(nodes_dict, thinned, nodes)
        # print("i=4")
        
        # ####################### Removing Single Nodes
        # nodes, nodes_dict = single_node_remover (nodes, edges_dict)
        # edges_dict, edges, nodes_dict, nodes = Corner_Connection(nodes_dict, thinned, nodes)
        # print("i=5")
        
        ####################### Arch Matching
        ## There are some parts of crack patterns that forms an arch, and the corner detection algorithm cannot detect a corner when the turn is not sharp.
        ## This part tries address this issue to match the arch as much as possible.
        i = 0
        while True:
            len_nodes_init = len(nodes)
            edges_dict, edges, nodes_dict, nodes = arch_match(nodes_dict, thinned, nodes, edges_dict, edges, img2)
            i = i + 1
            len_nodes_new = len(nodes)
            
            if len_nodes_new == len_nodes_init or i == 5:
                break
        print("The archs are matched!")
        print("The final graph representation of the crack pattern is ready!")
        ##### draw circles on all nodes
        circle_thickness = max(int(np.floor(min(0.004*img_bin.shape[0], 0.004*img_bin.shape[1]))),3)
        for i in nodes:
                x, y = i[0], i[1]
                cv2.circle(img1, (x, y), circle_thickness, (0,255,0), -1)    # draw circles on the corner
    
        ##### Resulting Image
        for value in edges.values():
            cv2.line(img1, value[0], value[1], (255,0,0), thickness=1, lineType=8)
    
        fig, ax = plt.subplots()
        plt.xticks([])
        plt.yticks([])
        plt.imshow(img1, cmap = None)
        image_format = 'svg' # e.g .png, .svg, etc.
        image_name = img_name[1:10]+"_connected.svg"
        fig.savefig(image_name, format=image_format, dpi=1200)
        
        plt.imshow(img1, cmap='Greys_r')
        plt.show()
    
        ## Saving the nodes and edges of the graph representation
        ## write dictionary to csv file
        if SAVE:
            fo = open(img_name[1:10]+"_edges.csv", "w", newline="")
            w = csv.writer(fo)    # write edges to edges.csv
            for key, val in edges_dict.items():
                w.writerow([key, val])
            fo.close()
    
            po = open(img_name[1:10]+"_nodes.csv", "w", newline="")
            w = csv.writer(po)    # write nodes to nodes.csv
            for key, val in nodes_dict.items():
                w.writerow([key, val])
            po.close()
