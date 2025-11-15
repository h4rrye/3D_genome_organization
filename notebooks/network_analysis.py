# ==========================================================
#                       LIBRARIES
# ==========================================================

# %pip install -q MDTraj    # leave this uncommented if running it on Google Colab
import mdtraj as md

import pandas as pd
import numpy as np
import scipy.ndimage as nd
import math
from tqdm import tqdm
from random import random

import urllib.request
import ssl
from copy import deepcopy

# ==========================================================
#                       DATA LOADING
# ==========================================================

url = 'https://calla.rnet.missouri.edu/genome3d/GSDB/Database/AX9716PF/GSE105544_ENCFF010WBP/VC/LorDG/chr1.pdb'
ssl_context = ssl._create_unverified_context()

# Download the file
with urllib.request.urlopen(url, context=ssl_context) as response:
    with open('chr1.pdb', 'wb') as out_file:
        out_file.write(response.read())

# Load from local file
chr_str = md.load_pdb('chr1.pdb')
coords = chr_str.xyz.reshape(-1, 3)

# ==========================================================
# Distance from center of mass
com = md.compute_center_of_mass(chr_str)

chr_com = []
for coord in coords:
    distances = np.linalg.norm(com - coord, axis=1)
    min_dist = np.min(distances)
    chr_com.append ([*coord, min_dist])

chr_com = np.array(chr_com)

# ==========================================================
# Rolling Mean
window_size = 50
jump = 1

smooth = []
for i in range(0, chr_com.shape[0] - window_size, jump):
    x = np.mean(chr_com[i:i + window_size, 0])
    y = np.mean(chr_com[i:i + window_size, 1])
    z = np.mean(chr_com[i:i + window_size, 2])
    smooth.append([x, y, z])

smooth = np.array(smooth)

# ==========================================================
# Distance from smooth line
chr_com_smooth = []
for coord in chr_com:
    distances = np.linalg.norm(coord[:3] - smooth, axis=1)
    min_dist = np.min(distances)

    chr_com_smooth.append([*coord, min_dist])

chr_com_smooth = np.array(chr_com_smooth)

# ==========================================================
# save file
np.save('x_y_z_dist_com_dist_rm.npy', chr_com_smooth)