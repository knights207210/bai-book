import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

import nibabel as nib
def ShowLocation(data, x, y, z):   
    abs_x = x
    abs_y = y
    abs_z = z
    
    #plot
    
    f, axs = plt.subplots(1,3,figsize=(10,10),gridspec_kw={'width_ratios': [1,data.shape[1]/data.shape[0],1]})
    
    #plt.subplot(1,3,2)
    
    axs[1].imshow(np.rot90(data[abs_x,:,:],1), interpolation='none')
    #axs[1].text(5,250,'x = '+str(x))
    axs[1].axhline(abs_z,color='white')
    axs[1].axvline(abs_y,color='white')
    
    #plt.subplot(1,3,1)
    axs[0].imshow(np.rot90(data[:,abs_y,:],1),  interpolation='none')
    axs[0].axhline(abs_z)
    axs[0].axvline(abs_x)

    #plt.subplot(1,3,3)
    axs[2].imshow(np.rot90(data[:,:,abs_z],1), interpolation='none')
    axs[2].axhline(abs_y)
    axs[2].axvline(abs_x)
    
    f.subplots_adjust(wspace=0, hspace=0)
    plt.show()

def find_most_active_slices_xyz(bcmap):
    max_sum_x = np.NINF
    max_sum_y = np.NINF
    max_sum_z = np.NINF
    num_x = np.NINF
    num_y = np.NINF
    num_z = np.NINF
    

    for num_slice in range(bcmap.shape[0]):
        slice_sum = np.sum(bcmap[num_slice,:,:])
        if slice_sum > max_sum_x:
            max_sum_x = slice_sum
            num_x = num_slice
    
    for num_slice in range(bcmap.shape[1]):
        slice_sum = np.sum(bcmap[:,num_slice,:])
        if slice_sum > max_sum_y:
            max_sum_y = slice_sum
            num_y = num_slice
    
    for num_slice in range(bcmap.shape[2]):
        slice_sum = np.sum(bcmap[:,:,num_slice])
        if slice_sum > max_sum_z:
            max_sum_z = slice_sum
            num_z = num_slice
                    
    return num_x, num_y, num_z

def find_most_active_slices_xyz_beta(bcmap,event):
    max_sum_x = np.NINF
    max_sum_y = np.NINF
    max_sum_z = np.NINF
    num_x = np.NINF
    num_y = np.NINF
    num_z = np.NINF
    

    for num_slice in range(bcmap.shape[0]):
        slice_sum = np.sum(bcmap[num_slice,:,:,event])
        if slice_sum > max_sum_x:
            max_sum_x = slice_sum
            num_x = num_slice
    
    for num_slice in range(bcmap.shape[1]):
        slice_sum = np.sum(bcmap[:,num_slice,:,event])
        if slice_sum > max_sum_y:
            max_sum_y = slice_sum
            num_y = num_slice
    
    for num_slice in range(bcmap.shape[2]):
        slice_sum = np.sum(bcmap[:,:,num_slice,event])
        if slice_sum > max_sum_z:
            max_sum_z = slice_sum
            num_z = num_slice
                    
    return num_x, num_y, num_z

def getMasked(cs, mask, threshold):
    masked = np.multiply(cs, mask)
    masked[masked == 0] = np.NINF
    
    maximum = masked.max()
    
    masked[masked<= threshold*maximum] = 1
    masked[mask == 0] = np.NINF
    return masked

def getMaskedContrast(cs,mask,threshold):
    masked_contrast = np.multiply(cs, mask)
    #masked_contrast[masked_contrast == 0] = np.NINF
    
    maximum = masked_contrast.max()
    
    masked_contrast[masked_contrast<= threshold*maximum] = 0
    #masked_contrast[mask == 0] = np.NINF
    return masked_contrast

def visualiza_contrast_withLocation_Interactive(masked_contrast, x,y,z):
    ShowLocation(masked_contrast, x, y, z)
    
def visualize_beta_withLocation_Interactive(masked_beta, x,y,z):
    ShowLocation(masked_contrast, x, y, z)