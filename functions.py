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

## These are some additional functions that may or may not have been used. They were developed over the course of the whole algorithm development.
## In this evolution, some functions were added, and some became redundant. But they were kept in case of future needs.


import numpy as np

def removeSingleNodes(nodes, nodes_dict, edges):
    v1 = [t[0] for t in edges.values()]
    v2 = [t[1] for t in edges.values()]

    for n in nodes:
        if (n in v1) or (n in v2):
            pass
        else:
            nodes.remove(n)
    return nodes


def DeleteSingularNode (nodes, edges):
    edges_list = list(edges.values())
    for node in nodes:
        if node not in edges_list:
            node.remove
    return nodes


def searchKeyByValue(nodes_dict, node):
    key = [k for k in nodes_dict if nodes_dict[k] == node]
    return key[0]


def loc2idx(edges_dict, nodes_dict):
    for V in edges_dict.values():
        V[0] = searchKeyByValue(nodes_dict, V[0])
        V[1] = searchKeyByValue(nodes_dict, V[1])
    return edges_dict


def sortByDistance(arr, ref):
    ''''
    sort an array by distance from a reference point
    :param arr: the unsorted array
    :param ref: the reference point
    :return: the sorted array
    '''
    arr.sort(key = lambda p: (p[0]-ref[0])**2 + (p[1]-ref[1])**2)
    return arr


def ignoreDirection(point, cand, frontier, window=5):
    """
    ignore the direction being searched by clearing frontier around the target point
    :param point: the target point (belongs to the "corners" set)
    :param frontier: current frontier
    :param window: the window of frontier deletion around "point"
    """
    actions = []
    for i in range(-window, window + 1):
        for j in range(-window, window + 1):
            actions.append([i,j])
    actions.remove([0, 0])
    for action in actions:
        new_pos = [cand[0]+action[0], cand[1]+action[1]]
        if new_pos in frontier and distance(point, new_pos) > distance(cand, new_pos):
            frontier.remove(new_pos)



def distance(p, ref, n_decimals=2):
    """
    function to calculate distance from "p" to "ref"
    :param p: point of interest
    :param ref: reference point
    :param n_decimals: decimal places
    :return: distance from "ref" to "p"
    """
    dist = np.sqrt((p[0] - ref[0]) ** 2 + (p[1] - ref[1]) ** 2)
    dist = round(dist, n_decimals)
    return dist



def list2dict(lst):
    """
    function to convert a list to a dictionary
    :param lst: list
    :return: dictionary (dic)
    """
    dic = dict()
    i = 0
    for sublst in lst:
        dic[str(i)] = sublst
        i += 1
    return dic



def getIndex(dic, point):
    for item in dic.items():
        if item[1][0] == point[0] and item[1][1] == point[1]:
            return item[0]


def isRepeated(point1, point2, edges_dic):
    repeated = False
    for v in edges_dic.values():
        if (point1 in v) and (point2 in v):
            repeated = True
            break
    return repeated


def removeDuplicate(nodes):
    dups = []
    for i in range(len(nodes) - 1):
        for j in range(i + 1, len(nodes)):
            if nodes[j] == nodes[i]:
                dups.append(nodes[j])
    for dup in dups:
        nodes.remove(dup)
    return nodes


########################################### Feature extraction #########################################################
def mat2dict(adj_matrix):
    """
    function to convert adjacency matrix to adjacency list (in terms of dictionary)
    :param adj_matrix: adjacency matrix
    :return: adjacency list (dictionary)
    """
    dic = dict()
    for i in range(adj_matrix.shape[0]):
        dic[str(i)] = []
        for j in range(adj_matrix.shape[1]):
            if adj_matrix[i,j] != 0:
                dic[str(i)].append(j)
        dic[str(i)] = tuple(dic[str(i)])
    return dic



def nodeDegree(matrix):
    """
    function to calculate degree of each node, based on the connectivity matrix
    :param matrix: connectivity matrix
    :return: degree and weighted degree of nodes
    """
    deg = np.zeros(matrix.shape[0], dtype=int)
    weighted_deg = np.zeros(matrix.shape[0])
    for i in range(matrix.shape[0]):
        deg[i] = sum(matrix[i, :] > 0)
        weighted_deg[i] = matrix[i, :].sum()
    return deg, weighted_deg



def dijkstra(total_nodes, adj_matrix, n_th):
    """
    function to calculate shortest path from node n_th to the other nodes
    :param total_nodes: total number of nodes
    :param adj_matrix: adjacency matrix
    :param n_th: node of reference
    :return: a vector of shortest path
    """
    g = mat2dict(adj_matrix)  # convert adjacency matrix to "g", adjacency list
    frontier = []
    explored = np.zeros(total_nodes, dtype=bool)
    dist = np.ones(total_nodes) * np.inf
    dist[n_th] = 0
    frontier.append([n_th, 0])
    while len(frontier) != 0:
        frontier.sort(key=lambda xy: xy[1])
        idx, minValue = frontier.pop(0)
        explored[idx] = True
        for next_node in g[str(idx)]:
            if explored[next_node]: continue
            newDist = dist[idx] + adj_matrix[idx,next_node]
            newDist = round(newDist, 2)                      # round to 2 decimal numbers
            if newDist < dist[next_node]:
                dist[next_node] = newDist
                frontier.append([next_node, newDist])
    return dist



def triangles(adj_matrix):
    """
    function to calculate number of triangles around each node
    :param adj_matrix: adjacency matrix
    :return: two vectors "tri" and "tri_w" (_w means "weighted") contains number of triangles around nodes
    """
    g = mat2dict(adj_matrix)
    total_nodes = adj_matrix.shape[0]
    tri = np.zeros(total_nodes, dtype=int)
    tri_w = np.zeros(total_nodes, dtype=float)
    for i in range(total_nodes):
        if len(g[str(i)]) == 1: continue
        next_nodes = g[str(i)]
        for j in range(len(next_nodes) - 1):
            for h in range(j+1, len(next_nodes)):
                if adj_matrix[next_nodes[j]][next_nodes[h]] != 0:
                    tri[i] += 1
                    n1 = i
                    n2 = next_nodes[j]
                    n3 = next_nodes[h]
                    tri_w[i] = (adj_matrix[n1,n2]*adj_matrix[n1,n3]*adj_matrix[n2,n3])**(1/3)
    return tri, tri_w



def clusteringCoeff(deg, tri):
    """
    function to calculate network's clustering coefficient
    :param deg: degrees of all nodes
    :param tri: num of triangles at all nodes
    :return: a value of clustering coefficient of network (C)
    """
    C = 0
    n = len(deg)
    for i in range(n):
        if deg[i] < 2: continue
        C += 2 * tri[i] / deg[i] / (deg[i]-1)
    C /= n
    return C


def transitivity(deg, tri):
    """
    function to calculate network's transitivity
    :param deg: degrees of all nodes
    :param tri: num of triangles at all nodes
    :return: a value of network's transitivity (T)
    """
    n = len(deg)
    denom = 0
    
    for i in range(n):
        if deg[i] < 2: continue
        denom += deg[i] * (deg[i]-1)
    T = 2 * sum(tri) / denom

    if np.isnan(T) == True:
        T = np.where(np.isnan(T), 0, T)
    return T


def globalEff(d):
    """
    function to calculate network's global efficiency
    :param d: shortest path matrix
    :return: a value of global efficiency of network (E)
    """
    n = d.shape[0]
    E_i = np.zeros(n)
    for i in range(n):
        for j in range(n):
            if j == i: continue
            E_i[i] += 1/d[i,j]
        E_i[i] /= (n-1)
    E = sum(E_i) / n
    return E


def localEff(adj_matrix, deg, d):
    """
    function to calculate local efficiency of the network
    :param adj_matrix: adjacency matrix
    :param deg: degress of all nodes
    :param d: shortest path matrix
    :return: a value of local efficiency (E_loc)
    """
    g = mat2dict(adj_matrix)
    n = len(deg)
    E_loc_i = np.zeros(n)
    for i in range(n):
        if deg[i] < 2: continue
        next_nodes = g[str(i)]
        for j in range(len(next_nodes) - 1):
            for h in range(j+1, len(next_nodes)):
                n1 = i
                n2 = next_nodes[j]
                n3 = next_nodes[h]
                E_loc_i[i] += adj_matrix[n1,n2] * adj_matrix[n1,n3] / d[n2,n3]
        E_loc_i[i] = E_loc_i[i] / deg[i] / (deg[i]-1)
    E_loc = sum(E_loc_i) / n
    return E_loc

