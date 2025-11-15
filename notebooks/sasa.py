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


# Create unverified context for this specific download
ssl_context = ssl._create_unverified_context()

url = 'https://calla.rnet.missouri.edu/genome3d/GSDB/Database/AX9716PF/GSE105544_ENCFF010WBP/VC/LorDG/chr1.pdb'

# Download the file
with urllib.request.urlopen(url, context=ssl_context) as response:
    with open('chr1.pdb', 'wb') as out_file:
        out_file.write(response.read())

# Load from local file
chr_str = md.load_pdb('chr1.pdb')
coords = chr_str.xyz.reshape(-1, 3)

# ==========================================================


# create overlapping spheres around every coordinate to envelop the entire chromosome
# calculate consecutive euclidian distances to calculate the radius of the spheres.
# (radius = max euclidian distance * overlapping factor) to ensure overlap between all the spheres.
#____________________________________________________________________________________________________


# calculate distances
class euc_dist:
    def __init__(self, df):
        self.df = df
        self.dists = []
        self.calulate_dist()


    def calulate_dist(self):
        for i in range(len(self.df) - 1):
            d = math.dist(self.df[i, :], self.df[i+1, :])         # >> math.dist similar to np.linalg.norm(ord=2)
            self.dists.append(d)


    def avg_dist(self):
        return np.mean(self.dists)

    def max_dist(self):
        return max(self.dists)


dd = euc_dist(coords)


oc = 1.45                           # >> overlapping coefficient
r = oc * dd.max_dist()              # >> radius of the sphere
d = 15                             # >> density of dots in the sphere

# _______________________________________________________________________________________
# create spheres around the points

def create_spheres(x, y, z, r=r, d=d):

    rad = np.linspace(0, r, int(d/2))
    phi = np.linspace(0, np.pi, d)
    theta = np.linspace(0, 2*np.pi, d, endpoint=False)

    theta, phi, rad = np.meshgrid(theta, phi, rad, indexing='ij')

    phi = phi.flatten()
    theta = theta.flatten()
    rad = rad.flatten()

    dx = rad * np.sin(phi) * np.cos(theta) + x
    dy = rad * np.sin(phi) * np.sin(theta) + y
    dz = rad * np.cos(phi) + z

    spheres = np.array([dx, dy, dz])

    return spheres

all_spheres = np.empty((3,0))

for rows in tqdm(coords, total=coords.shape[0]):
    spheres = create_spheres(rows[0], rows[1], rows[2], r, d)
    all_spheres = np.hstack([all_spheres, spheres])

all_spheres = np.array(all_spheres).T


# scaling the values to +ve
scaling_factor = abs(np.min(all_spheres) * 1.25)
all_spheres += scaling_factor

coords += scaling_factor


# create a cube and place the structure in it
# the cube is further divided into multiple bins = b


x_lim = [min(all_spheres[:,0]), max(all_spheres[:,0])]
y_lim = [min(all_spheres[:,1]), max(all_spheres[:,1])]
z_lim = [min(all_spheres[:,2]), max(all_spheres[:,2])]

edge_size = max((x_lim[1] - x_lim[0]), (y_lim[1] - y_lim[0]), (z_lim[1] - z_lim[0]))
padding = edge_size * 0.1
edge_size += padding

b = 50         # >> number of bins per side

bin_size = edge_size / b

box = np.zeros((b, b, b), dtype='float')

for row in all_spheres:
    x, y, z = row
    x_index = int(x // bin_size)
    y_index = int(y // bin_size)
    z_index = int(z // bin_size)

    if (0 <= x_index < b) and (0 <= y_index < b) and (0 <= z_index < b):
        box[x_index, y_index, z_index] = 1


# find the surface bins

# create a box to move around the entire cube
kernel = np.ones ((3, 3, 3), dtype='int')
kernel[1, 1, 1] = 0

neighbour_count = nd.convolve(box, kernel, mode='constant', cval=0)

surface_bins = (box == 1) & (neighbour_count < 26)

surface_coords = np.argwhere(surface_bins == 1)         # >> indices of bin value = 1

# coords, surface_coords

surface_coords_scaled = surface_coords * bin_size

coord_dist = []
for coord in coords:
    distances = np.linalg.norm(surface_coords_scaled - coord, axis=1)   # euc dist for all
    min_dist = np.min(distances)
    coord_dist.append([*coord, min_dist])   # unpack array using *

coord_dist = np.array(coord_dist)

# ==========================================================
#                       SAVING DATA
# ==========================================================

np.save('x_y_z_dist_surf.npy', coord_dist)
surface_coords_scaled = surface_coords * bin_size - scaling_factor
np.save('surface_coords_scaled.npy', surface_coords_scaled)

