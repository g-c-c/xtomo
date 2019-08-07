#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 20:57:52 2019

@author: anu
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 19:14:36 2019

@author: anu
"""

import gridrec
import numpy as np
import matplotlib.pyplot as plt
import tomopy
import h5py
import dxchange
import sys
from scipy import special
import time
from sklearn.metrics import mean_squared_error


start_time = time.time()

np.set_printoptions(threshold=sys.maxsize)

k_r = 2

base_folder = gridrec.create_unique_folder("shepp_logan")

size = 128

num_slices = size
num_angles = size
#num_angles = 512
num_rays   = size

true_obj_shape = (num_slices, num_rays, num_rays)

true_obj = gridrec.generate_Shepp_Logan(true_obj_shape)

pad_1D = 200
padding_array = ((0,0), (pad_1D, pad_1D), (pad_1D, pad_1D))

num_rays = num_rays + pad_1D*2

print("True obj shape", true_obj.shape)

gridrec.save_cube(true_obj, base_folder + "true")

#padding...
true_obj = np.lib.pad(true_obj, padding_array, 'constant', constant_values=0)

#angles in radians
theta = np.arange(0, 180., 180. / num_angles)*np.pi/180.

simulation = gridrec.forward_project(true_obj, theta)

#The simulation generates a stack of projections, meaning, it changes the dimensions order
gridrec.save_cube(simulation, base_folder + "sim_project")

simulation = np.swapaxes(simulation,0,1)

gridrec.save_cube(simulation[64], base_folder + "sim_slice")

#Here I take only a subset of slices to not reconstruct the whole thing...
sub_slice = 15

#Calls backward projection
tomo_stack = gridrec.gridrec(simulation[64:65], theta, num_rays, k_r, 'gaussian')
if pad_1D > 0: tomo_stack = tomo_stack[:, pad_1D: -pad_1D, pad_1D: -pad_1D]
plt.imshow(abs(tomo_stack[0]),cmap='Greys')
plt.show()

#Calls forward projection
sino_stack = gridrec.gridrec_transpose(true_obj[64:65], theta, num_rays, k_r, 'gaussian')
if pad_1D > 0: sino_stack = sino_stack[:, :, pad_1D: -pad_1D]
plt.imshow(abs(sino_stack[0]),cmap='Greys')

#Save images
gridrec.save_cube(abs(tomo_stack), base_folder + "rec")
gridrec.save_cube(abs(sino_stack), base_folder + "sino")

print("A simulation of size", simulation.shape, "with kernel radius", k_r, "took", time.time() - start_time, "seconds to run")


#Calculates and plots mean squared erro
"""
image1 = true_obj[0, 64: -64, 64: -64]
image2 = tomo_stack[0][0:128,0:128]
image3 = simulation[64][0:128,0:128]
image4 = sino_stack[0][0:128,0:128]

np.save('image1.npy',image1)
np.save('image2.npy',image2)
np.save('image3.npy',image3)
np.save('image4.npy',image4)

image2 = abs(image2)
image4 = abs(image4)

image1 = (image1-image1.min())/(image1.max()-image1.min())
image2 = (image2-image2.min())/(image2.max()-image2.min())
image3 = (image3-image3.min())/(image3.max()-image3.min())
image4 = (image4-image4.min())/(image4.max()-image4.min())

diff1 = image1**2 - image2**2
diff2 = image3**2 - image3**2

plt.imshow(diff1,cmap='Greys')
plt.show()

plt.imshow(diff2,cmap='Greys')
plt.show()

mse_tomo = mean_squared_error(image1,image2)
print(mse_tomo)

mse_sino = mean_squared_error(image3,image4)
print(mse_sino)
"""


