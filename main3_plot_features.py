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


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import collections
from sklearn.preprocessing import StandardScaler

FONT = {'fontname': 'Times New Roman', 'fontsize': 18}

"""
------------------
+  Load dataset  +
------------------
"""
Walls = pd.read_excel('Walls.xlsx')
# Walls = pd.read_excel('Walls_diff.xlsx')


wall_id = []
for i in range(len(Walls)):
    wall_name = str(Walls.iloc[i].to_numpy())
    wall_id.append(str(wall_name[1:3]))
  

repet = dict((x, wall_id.count(x)) for x in set(wall_id))
repet = collections.OrderedDict(sorted(repet.items()))



All_Features = pd.read_csv('All_Features.csv')
All_Features_WithDiag = pd.read_csv('All_Features_WithDiag.csv')
# all_features = pd.read_csv('All_Features_diff.csv')



i = 0
df_scaled = []
df_scaled_WithDiag = []
for key, val in repet.items():
    df_scaled[i: i+val] = StandardScaler().fit_transform(All_Features[i: i+val].copy(deep=True))
    # df_scaled[i: i+val] = (All_Features.iloc[i: i+val].to_numpy()-np.min(All_Features.iloc[i: i+val].to_numpy())) / (np.max(All_Features.iloc[i: i+val].to_numpy()) - np.min(All_Features.iloc[i: i+val].to_numpy()))
    
    df_scaled_WithDiag[i: i+val] = StandardScaler().fit_transform(All_Features_WithDiag[i: i+val].copy(deep=True))
    # df_scaled_WithoutDiag[i: i+val] = (All_Features_WithoutDiag.iloc[i: i+val].to_numpy()-np.min(All_Features_WithoutDiag.iloc[i: i+val].to_numpy())) / (np.max(All_Features_WithoutDiag.iloc[i: i+val].to_numpy()) - np.min(All_Features_WithoutDiag.iloc[i: i+val].to_numpy()))
    
    i = i + val
    
columns = ['k_avg', 'kw_avg', 't_avg', 'tw_avg', 'C', 'C_w', 'T', 'T_w', 'E', 'E_loc', 'eigvalmax', 'eigvalmin']
df_scaled = pd.DataFrame(df_scaled, columns = columns)
df_scaled_WithDiag = pd.DataFrame(df_scaled_WithDiag, columns = columns)

df_scaled.drop(['t_avg', 'tw_avg', 'C', 'C_w', 'T', 'T_w', 'E', 'E_loc', 'eigvalmax', 'eigvalmin'], axis=1, inplace=True)
df_scaled_WithDiag.drop(['t_avg', 'tw_avg', 'C', 'C_w', 'T', 'T_w', 'E', 'E_loc', 'eigvalmax', 'eigvalmin'], axis=1, inplace=True)


# # Load mechanical features
# # Mechanical features of wall 1 - north
# df_mecha = pd.read_excel(r'exp_data.xlsx')
# df_mecha = df_mecha.iloc[0:9, :10]
# # print(df_mecha.columns)
# df_mecha.columns = ['displacement', 'drift', 'lateral force', 'ED', 'redr', 'evd',
#                     'secant stiffness', 'flexural displacement', 'shear displacement', 'DI']
# selected_features = ['displacement', 'drift', 'lateral force', 'ED', 'redr', 'evd',
#                     'secant stiffness', 'flexural displacement', 'shear displacement', 'DI']
# df_mecha = df_mecha[selected_features]


"""
-------------------------
+  Plot graph features  +
-------------------------
"""

i = 0
for key, val in repet.items():
    if val > 2:
        # drift = df_mecha['drift']
        
        LS = [*range(1,val+1)]
        # fig, ax = plt.subplots(figsize=(9,6), dpi=100)
        # # plt.figure(figsize=(9,6), dpi=100)
        # plt.plot(LS, All_Features_WithDiag["k_avg"][i: i+val].to_numpy(), marker='s')
        # plt.xlabel("Load Step", **FONT)
        # plt.ylabel("k_avg(-)", **FONT)
        # # plt.legend(prop={'size': 16})
        # plt.xticks(**FONT)
        # plt.yticks(**FONT)
        # # plt.title(key)
        # # x = All_Features["k_avg"][i: i+val].to_numpy()
        # # y = All_Features["kw_avg"][i: i+val].to_numpy()
        # # text = [*range(1, val+1, 1)]
        # # for ii, txt in enumerate(text):
        # #     ax.annotate(txt, (x[ii], y[ii]), fontsize=13)
        # plt.savefig('k_avg_11.svg')
        # plt.show()
        
        
        # fig, ax = plt.subplots(figsize=(9,6), dpi=100)
        # # plt.figure(figsize=(9,6), dpi=100)
        # plt.plot(LS, All_Features_WithDiag["kw_avg"][i: i+val].to_numpy(), marker='s')
        # plt.xlabel("Load Step", **FONT)
        # plt.ylabel("kw_avg (-)", **FONT)
        # # plt.legend(prop={'size': 16})
        # plt.xticks(**FONT)
        # plt.yticks(**FONT)
        # # plt.title(key)
        # # x = All_Features["k_avg"][i: i+val].to_numpy()
        # # y = All_Features["kw_avg"][i: i+val].to_numpy()
        # # text = [*range(1, val+1, 1)]
        # # for ii, txt in enumerate(text):
        # #     ax.annotate(txt, (x[ii], y[ii]), fontsize=13)
        # plt.savefig('kw_avg_11.svg')
        # plt.show()
        
        
        kave_by_kwave = np.divide(All_Features_WithDiag["k_avg"][i: i+val].to_numpy(), All_Features_WithDiag["kw_avg"][i: i+val].to_numpy())
        fig, ax = plt.subplots(figsize=(9,6), dpi=100)
        # plt.figure(figsize=(9,6), dpi=100)
        plt.plot(LS, kave_by_kwave, marker='s')
        plt.xlabel("Load Step", **FONT)
        plt.ylabel("k_avg / kw_avg (-)", **FONT)
        # plt.legend(prop={'size': 16})
        plt.xticks(**FONT)
        plt.yticks(**FONT)
        plt.title(key)
        # x = All_Features["k_avg"][i: i+val].to_numpy()
        # y = All_Features["kw_avg"][i: i+val].to_numpy()
        # text = [*range(1, val+1, 1)]
        # for ii, txt in enumerate(text):
        #     ax.annotate(txt, (x[ii], y[ii]), fontsize=13)
        # plt.savefig(f'k_avg_kw_avg_{key}.svg')
        plt.show()
        
        
        
        # fig, ax = plt.subplots(figsize=(9,6), dpi=100)
        # # plt.figure(figsize=(9,6), dpi=100)
        # plt.plot(LS, all_features["kw_avg"][i: i+val], marker='s', label='SW1')
        # plt.xlabel("Drift (%)", **FONT)
        # plt.ylabel("Weighted average degree of network (-)", **FONT)
        # plt.legend(prop={'size': 16})
        # plt.xticks(**FONT)
        # plt.yticks(**FONT)
        # plt.title(key)
        # # text = [*range(3, 10, 1)]
        # # for i, txt in enumerate(text):
        # #     ax.annotate(txt, (drift[i], all_features["kw_avg"][i]), fontsize=13)
        # #plt.show()
        # # plt.savefig('SW1_Weighted average degree of network.svg')
        
        
        # fig, ax = plt.subplots(figsize=(9,6), dpi=100)
        # # plt.figure(figsize=(9,6), dpi=100)
        # plt.plot(LS, all_features["E"][i: i+val], marker='s', label='SW1')
        # plt.xlabel("Drift (%)", **FONT)
        # plt.ylabel("Global efficiency (-)", **FONT)
        # plt.legend(prop={'size': 16})
        # plt.xticks(**FONT)
        # plt.yticks(**FONT)
        # plt.title(key)
        # # text = [*range(3, 10, 1)]
        # # for i, txt in enumerate(text):
        # #     ax.annotate(txt, (drift[i], all_features["E"][i]), fontsize=13)
        # # plt.show()
        # # plt.savefig('SW1_Global efficiency.svg')
        
        
        # fig, ax = plt.subplots(figsize=(9,6), dpi=100)
        # # plt.figure(figsize=(9,6), dpi=100)
        # plt.plot(LS, all_features["eigvalmax"][i: i+val], marker='s', label='SW1')
        # plt.xlabel("Drift (%)", **FONT)
        # plt.ylabel("Maximum Eigenvalue (-)", **FONT)
        # plt.legend(prop={'size': 16})
        # plt.xticks(**FONT)
        # plt.yticks(**FONT)
        # plt.title(key)
        # text = [*range(3, 10, 1)]
        # for i, txt in enumerate(text):
        #     ax.annotate(txt, (drift[i], all_features["E_loc"][i]), fontsize=13)
        #plt.show()
        # plt.savefig('SW1_Local efficiency.svg')
        
        
        # fig, ax = plt.subplots(figsize=(9,6), dpi=100)
        # # plt.figure(figsize=(9,6), dpi=100)
        # plt.plot(LS, all_features["eigvalmin"][i: i+val], marker='s', label='SW1')
        # plt.xlabel("Drift (%)", **FONT)
        # plt.ylabel("Minimum Eigenvalue (-)", **FONT)
        # plt.legend(prop={'size': 16})
        # plt.xticks(**FONT)
        # plt.yticks(**FONT)
        # plt.title(key)
        # text = [*range(3, 10, 1)]
        # for i, txt in enumerate(text):
        #     ax.annotate(txt, (drift[i], all_features["E_loc"][i]), fontsize=13)
        #plt.show()
        # plt.savefig('SW1_Local efficiency.svg')
    
    i = i + val