########################################################################
# This routine will select the detected peaks based on certain criteria 
# and classify them as shot if these criteria are met
# NOTE : Run this routine only after running shot_detector.py and shot_fitting.py
########################################################################





import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import my_funcs as mf



unit1_peak_features = np.loadtxt('unit1_peak_fit_values.txt')
unit2_peak_features = np.loadtxt('unit2_peak_fit_values.txt')
peak_time_from_file = np.loadtxt('peak_time_list_0p05_unit1.txt')
peak_index = np.loadtxt("index_list_0p05_unit1_fullrange.txt",dtype=int)

bounds = np.array([[-10,1,1e-3,-100],[10,20000,100,-1e-3]])
min_bound = bounds[0]
max_bound = bounds[1]
#~ good_fits_index = np.where ()

labels = ['t0','A','w1','w2']

good_fits_flag = np.ones(len(peak_index))					# We will store 1 for good fit and 0 for bad	

boundary_frac_dist = 1e-1								# How far from the boundary the fit parameter has to be

for i,par in enumerate(labels):
	bad_fit_index = np.where( (np.abs(unit1_peak_features[:,i] - min_bound[i])<boundary_frac_dist * np.abs(min_bound[i])) | (np.abs(unit1_peak_features[:,i] - max_bound[i])< boundary_frac_dist * np.abs(max_bound[i])) 
							| (np.abs(unit2_peak_features[:,i] - min_bound[i])<boundary_frac_dist * np.abs(min_bound[i])) | (np.abs(unit2_peak_features[:,i] - max_bound[i])< boundary_frac_dist * np.abs(max_bound[i])) ) [0]
	good_fits_flag[bad_fit_index] = 0

print len(good_fits_flag), np.sum(good_fits_flag)	
good_fits_flag = good_fits_flag.astype(bool)

np.savetxt("good_fit_flag.txt",good_fits_flag)

shot_flag = good_fits_flag.copy()						# 1 for Shot 0 otherwise. It assumes bad fits are not shots

par_diff_ratio = 0.3							# We compute the ratio of pars and see if they lie within 1*par_diff_ratio of 1

for i in range (1,np.shape(unit1_peak_features)[1]):
	par_ratio = unit1_peak_features[:,i]/unit2_peak_features[:,i]
	no_shot_index = np.where( (par_ratio < 1-par_diff_ratio) | ( par_ratio > 1 + par_diff_ratio )) [0]
	
	shot_flag[no_shot_index] = 0 
	
print len(good_fits_flag), np.sum(good_fits_flag), np.sum(shot_flag)

np.savetxt("shot_flag.txt",shot_flag)
