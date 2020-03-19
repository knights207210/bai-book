import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

import nibabel as nib
#compute beta map 3D
def compute_contrast(beta_map, contrast):         
    b = np.squeeze(beta_map)      
    c = np.array(contrast).T
    cs = np.dot(b,c)
    return cs

def generateContrast(dm, t1, t2):
    labels = dm.columns
    contrast = np.zeros(len(labels))
    t1_all = []
    t2_all = []
    if '+' in  t1:
        t1_all = t1.split('+')
    else:
        t1_all = [t1]
    if '+' in t2:
        t2_all = t2.split('+')
    else:
        t2_all = [t2]
    t1_flag = False
    t2_flag = False
    for i, label in enumerate(labels):
        for t1i in t1_all:
            if t1i in label:
                contrast[i] = 0.5
                break
                
        for t2i in t2_all:
            if t2i in label:
                contrast[i] = -0.5
                break
        
        #if t1 in label:
            #contrast[i] = 0.5
        #if t2 in label:
            #contrast[i] = -0.5
    return contrast