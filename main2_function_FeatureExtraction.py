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


import csv
import sys
sys.path.append("../")
from functions import *
import numpy as np
from adjacency_matrix import *
import networkx as nx
from networkx.algorithms import community



def FeatureExtraction (wall_name):
    PLOT = False
    img_name = str(wall_name)

    nodes_filename = img_name[1:10]+"_nodes.csv"
    edges_filename = img_name[1:10]+"_edges.csv"
    output_filename = img_name[1:10]+"_features.csv"

    
    # read the "nodes" in the crack graph
    reader = csv.reader(open(nodes_filename, 'r'))
    nodes = dict()
    for row in reader:
       k, v = row
       nodes[k] = eval(v)
    total_nodes = int(k) + 1     # total number of nodes in the crack graph

    
    # read the "edges" dictionary exported by main_1.py
    reader = csv.reader(open(edges_filename, 'r'))
    edges = dict()
    for row in reader:
       k, v = row
       edges[k] = eval(v)
    total_edges = int(k) + 1    # total number of nodes in the crack graph

    
    #################### Making the connectivity (adjacency) matrix
    adj_matrix = adj_mat(nodes, edges)
    
    ########################### Feature 1: node degree #####################################################################
    k, k_w = nodeDegree(adj_matrix)
    k_avg = np.mean(k)
    kw_avg = np.mean(k_w)



    # ########################### Feature 2: shortest path ###################################################################
    # d_w = np.zeros((total_nodes, total_nodes), dtype=float)
    # for n_th in range(total_nodes):
    #     d_w[n_th] = dijkstra(total_nodes, adj_matrix, n_th)     # update row n-th by shortest path from Dijkstra algorithm

    ########################### Feature 3: number of triangles #############################################################
    t, t_w = triangles(adj_matrix)
    t_avg = np.mean(t)
    tw_avg = np.mean(t_w)


    ########################### Feature 4: Network's clustering coefficient ################################################
    C = clusteringCoeff(k, t)
    C_w = clusteringCoeff(k, t_w)


    ########################### Feature 5: Network's transitivity ##########################################################
    T = transitivity(k, t)
    T_w = transitivity(k, t_w)


    ########################### Feature 6: Network's global efficiency #####################################################
    ############ making the graph
    G = nx.Graph(adj_matrix, nodetype=int)
    E = nx.global_efficiency(G)
    # E = globalEff(d_w)


    ########################### Feature 7: Network's local efficiency ######################################################
    E_loc = nx.local_efficiency(G)
    # E_loc = localEff(adj_matrix, k, d_w)

    
    ########################### Feature 8: Network's Max and Min Eigenvalue ######################################################
    e = np.linalg.eigvals(adj_matrix)
    e_real = [ele.real for ele in e]
    # e_imag = [ele.imag for ele in e]
    # deg_cen = nx.degree_centrality(G)
    
    
    # write the results to csv
    w = csv.writer(open(output_filename, "w", newline=""))
    w.writerow(["k_avg", k_avg])
    w.writerow(["kw_avg", kw_avg])
    w.writerow(["t_avg", t_avg])
    w.writerow(["tw_avg", tw_avg])
    w.writerow(["C", C])
    w.writerow(["C_w", C_w])
    w.writerow(["T", T])
    w.writerow(["T_w", T_w])
    w.writerow(["E", E])
    w.writerow(["E_loc", E_loc])
    w.writerow(["eigvalmax", np.max(e_real)])
    w.writerow(["eigvalmin", np.min(e_real)])
    
