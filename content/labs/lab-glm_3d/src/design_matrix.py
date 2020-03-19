import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

import nibabel as nib
# (seconds)
total_scan_time = 300 # five minutes

# (milliseconds)
onset_times = [0,2400,5700,8700,11400,15000,18000,20700,23700,26700,29700,33000,35400,39000,41700,44700,48000,
        50700,53700,56400,59700,62400,66000,69000,71400,75000,78000,80400,83400,87000,89700,93000,96000,
        99000,102000,105000,108000,110400,113700,116700,119400,122700,125400,129000,131400,135000,137700,
        140400,143400,146700,149400,153000,156000,159000,162000,164400,167700,170400,173700,176700,179700,
        182700,186000,188400,191700,195000,198000,201000,203700,207000,210000,212700,215700,218700,221400,
        224700,227700,230700,234000,236700,240000,243000,246000,248400,251700,254700,257400,260400,264000,
        266700,269700,272700,275400,278400,281700,284400,288000,291000,293400,296700]

# onset type (one-based index)
onset_types = [8,8,11,1,3,10,5,10,4,6,10,2,7,9,9,7,7,11,11,9,
        1,4,11,5,6,9,11,11,7,3,10,11,2,11,11,11,7,11,11,6,
        10,2,8,11,9,7,7,2,3,10,1,8,2,9,3,8,9,4,7,1,
        11,11,11,1,7,9,8,8,2,2,2,6,6,1,8,1,5,3,8,10,
        11,11,9,1,7,4,4,8,2,1,1,11,5,2,11,10,9,5,10,10]

localizer_labels = ['horizontal_checkerboard',
          'vertical_checkerboard',
          'motor_right_auditory',          
          'motor_left_auditory',
          'motor_right_visual',          
          'motor_left_visual',
          'subtraction_auditory',
          'subtraction_visual',          
          'sentence_visual',   
          'sentence_auditory']

def get_localizer_design_data():

    # onset type
    onset_types_0_based = np.array(onset_types) - 1
    
    events = list(zip(onset_times, onset_types_0_based))
    
    # ignore the last onset type
    events = [(onset_time, onset_type) for (onset_time, onset_type) in events if onset_type != 10]
    
    return (events, localizer_labels)

events, labels = get_localizer_design_data()

def compute_design_vector(events, event_index, n_tr, tr):
    
    selected_onset_times = [onset_time for onset_time, onset_type in events if onset_type == event_index]
        
    iss = np.floor(np.array(selected_onset_times) / (tr * 1000)).astype(int)
                           
    line = np.zeros(n_tr)
        
    line[iss] = 1
    
    return line
def create_design_matrix(events, labels, tr, duration):     
    ### BEGIN SOLUTION
    
    design_matrix = np.zeros((duration, len(labels)),int)
    for i in range(0, len(labels)):
        design_vector_i = compute_design_vector(events, i, duration, tr)
        design_matrix[:,i] = design_vector_i.T
    design_matrix = pd.DataFrame(data=design_matrix, columns=labels)
    
    ### END SOLUTION
    return design_matrix

def add_intercept(design_matrix):     
    ### BEGIN SOLUTION
    design_matrix_new = design_matrix.copy()
    n_rows = design_matrix.shape[0]
    design_matrix_new['intercept'] = np.ones(n_rows)
    return design_matrix_new
    ### END SOLUTION
    
def add_poly(design_matrix, degrees=2, flipped=False):     
    ### BEGIN SOLUTION
    design_matrix_new = design_matrix.copy()
    time = np.linspace(-1, 1, design_matrix.shape[0])
    if flipped:
        poly = (1-time) ** degrees
        design_matrix_new['1-poly'+str(degrees)] = poly
    else:
        poly = time ** degrees    
        design_matrix_new['poly'+str(degrees)] = poly
    return design_matrix_new

from numpy import sin, pi, arange
def add_cosine(design_matrix, freq, amplitude, phase = 0):         
    duration = design_matrix.shape[0]   
    time = np.linspace(0, 1, duration)
    w = amplitude * sin(2*pi*freq*time + pi*phase)
    copy = design_matrix.copy()
    copy['cos'+str(freq)] = w
    return copy

from nltools.external import glover_hrf
def convolve_hrf(design_matrix, tr):     
    ### BEGIN SOLUTION
    design_matrix_new = design_matrix.copy()
    hrf = glover_hrf(tr, oversampling=1) 
    labels = design_matrix.columns    
    for label in labels:
        design_matrix_new[label] = np.convolve(design_matrix_new[label].to_numpy(), hrf, mode='same')        
    return design_matrix_new
    ### END SOLUTION
    
def add_many(design_matrix, funcs = []):     
    ### BEGIN SOLUTION
    design_matrix_new = design_matrix.copy() 
    
    for func in funcs:
        design_matrix_new = func(design_matrix_new)
        
    return design_matrix_new
    
    ### END SOLUTION
funcs = [
    lambda dm : convolve_hrf(dm, 2),
    lambda dm : add_intercept(dm),
    lambda dm : add_poly(dm, degrees = 2),
    lambda dm : add_poly(dm, degrees = 3),
    lambda dm : add_poly(dm, degrees = 2, flipped = True),
    lambda dm : add_poly(dm, degrees = 3, flipped = True),  
    lambda dm : add_cosine(dm, 1, 1),
    lambda dm : add_cosine(dm, 2, 1),    
    lambda dm : add_cosine(dm, 3, 1),        
]
