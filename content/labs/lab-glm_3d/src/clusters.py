import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

import nibabel as nib
import scipy.misc
from scipy import ndimage
from scipy.ndimage.filters import gaussian_filter

def convolveFilter(data, sigma = 0.2): 
    return gaussian_filter(data, sigma)

def label_clusters(data):
    labeled_img, num_labels = scipy.ndimage.label(data)
    return labeled_img, num_labels

def get_clusterforvis(data, clustered_data, label_num):
    datac = data.copy() 
    datac[clustered_data!=label_num] = np.NINF
    
    return datac