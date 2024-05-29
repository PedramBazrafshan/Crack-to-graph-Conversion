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



#######################################################
"""""""""""
This is help documentation for database of pictures collected for Damage Assessment of RCSWs Using Crack Pattern.
Image Name(000000000) = wallID(000) + h/l(0.00 * 100) + drift(0.00% * 100)

"""""""""""
#######################################################

## importing libraries
import sys
sys.path.append("../../../")
from functions import *
from main1_function import *
from main2_function_FeatureExtraction import *
import pandas as pd
import collections
import time
start = time.time()


## Reading wall IDs
Walls = pd.read_excel('Walls.xlsx')

wall_id = []
for i in range(len(Walls)):
    wall_name = str(Walls.iloc[i].to_numpy())
    wall_id.append(str(wall_name[1:4]))
  

repet = dict((x, wall_id.count(x)) for x in set(wall_id))
repet = collections.OrderedDict(sorted(repet.items()))


## Calling the crack-to-graph conversion function
i = 0
for key, val in repet.items():
    crack_to_graph(Walls.iloc[i: i+val].to_numpy())
    i = i + val


## Calling the graph feature extraction function
i = 0
for i in range(len(Walls)):
    FeatureExtraction(Walls.iloc[i].to_numpy())
  
end = time.time()
total_time = end - start
print("\n"+f"Total time is {round(total_time,2)} seconds!")