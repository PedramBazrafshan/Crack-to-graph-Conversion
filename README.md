### **A graph-based method for quantifying crack patterns on reinforced concrete shear walls**
---


### **Overview**
---
This is the official repository of the Research Article _A graph-based method for quantifying crack patterns on reinforced concrete shear walls_ by Pedram Bazrafshan et al.,
https://doi.org/10.1111/mice.13009  
This research article is featured as the cover paper of the Journal of Computer-Aided Civil and Infrastructure Engineering (CACAIE)'s special issue on computational concrete engineering.


### **Get Started**
---
1. The sketches of the crack patterns are prepared in images with .bmp format. This paper used manual sketched crack patterns.

2. The images of the crack patterns are named with the following format:    The name contains 9 digits: first three digits are for the wall ID, the second three digits are for aspect ratio of the wall (height / width), and the last three digits show the drift at which the crack image was taken.
    imagename (000000000) = wallID(000) + h/l(0.00 * 100) + drift(0.00% * 100)

3. The names of the images are added to an excel file named "Walls.xlsx"

4. The file named "requirements.txt" contains all the libraries of an environment in which the algorithm runs. To install the compatible versions of the libraries used, execute:  
```
pip install -r requirements.txt
```

5. To run the code, the Python file named "main0_all_img.py" should be run.

6. The outputs are 1) an image showing the crack pattern with the graph representation overlayed on the crack pattern in a .svg format, 2) A .csv file named "imagename_nodes" which contains the node numbers and their coordinates, 3) A .csv file named "imagename_edges" which contains the edges numbers, the nodes that are connected together, and the length between them, and 4) a .csv file named "imagename_features" which contains the graph features (i.e., the average and weighted average degree of the network, global and local clustering coefficients, eigenvalues, etc.) extracted from the graph representation.


### **Input Sample**
---
![Image](https://github.com/users/PedramBazrafshan/projects/1/assets/83833578/1be81dd0-0e56-4378-bba0-291f73155b51)


### **Output Sample**
---
![Image](https://github.com/users/PedramBazrafshan/projects/1/assets/83833578/4253cb9b-7383-493e-86b2-55efe5e7e292)


### **Citation**
---
If you find our work useful in your research, please consider citing:  
Bazrafshan, P., On, T., Basereh, S., Okumus, P., & Ebrahimkhanlou, A. (2024). A graph‐based method for quantifying crack patterns on reinforced concrete shear walls. Computer‐Aided Civil and Infrastructure Engineering, 39(4), 498-517.
```
@article{bazrafshan2024graph,
  title={A graph-based method for quantifying crack patterns on reinforced concrete shear walls},
  author={Bazrafshan, Pedram and On, Thinh and Basereh, Sina and Okumus, Pinar and Ebrahimkhanlou, Arvin},
  journal={Computer-Aided Civil and Infrastructure Engineering},
  volume={39},
  number={4},
  pages={498--517},
  year={2024},
  publisher={Wiley Online Library}
}
```

### **Developers**
---
The core of the files named "CornerConnection.py" and "functions.py" have previously been developed as a course project by Thinh On and later were developed and finalized by Pedram Bazrafshan. The rest of the files have been developed by Pedram Bazrafshan.

### **License**
---
Licensed under a [Creative Commons Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/) for Non-commercial use only. Any commercial use should get formal permission first.


### **Inquiries**
---
For inquiries, please contact:  
pb669@drexel.edu
