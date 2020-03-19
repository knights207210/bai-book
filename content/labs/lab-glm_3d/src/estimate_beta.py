import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

import nibabel as nib
#compute beta map 3D
def estimate_beta(X, Y):
    return np.dot(np.dot(np.linalg.pinv(np.dot(X.T, X)), X.T), Y)
def compute_beta_map(data,design_matrix):
    fir=data.get_fdata().shape[0]
    sec=data.get_fdata().shape[1]
    thi=data.get_fdata().shape[2]
    n_regressors = design_matrix.shape[1]
    N=np.zeros((fir,sec,thi,n_regressors)) 
    for i in range(fir):
        for j in range(sec):
            for k in range(thi):
                Y=data.get_fdata()[i,j,k,:]
                bs=estimate_beta(design_matrix,Y)
                N[i,j,k:]=bs
    return N