########################################################################
# This routine will select the detected peaks based on certain criteria 
# and classify them as shot if these criteria are met
# NOTE : Run this routine only after running shot_detector.py and shot_fitting.py
########################################################################





import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import my_funcs as mf
import argparse 


pr = argparse.ArgumentParser()

pr.add_argument("--lcdatadir", 		"-d",default="../lc_data/")
pr.add_argument("--filename1",		"-i1",default="laxpc_lc_0p05_unit1_3.0_80.0keV.lc")
pr.add_argument("--filename2", 		"-i2",default="laxpc_lc_0p05_unit2_3.0_80.0keV.lc")
pr.add_argument("--output_text", 	"-o",default="")
pr.add_argument("--peak_file_text", "-p",default="")
pr.add_argument("--fitted_text", 	"-f",default="")

pr.add_argument("--boundary_dist", 	"-b",default=0.1,type = float)
pr.add_argument("--par_ratio",	 	"-r",default=0.3,type = float)




args = pr.parse_args()


data_path = args.lcdatadir
file_name1 = args.filename1
if data_path[-1]!='/': data_path = data_path+'/'

fitted_text = args.fitted_text

unit1_data_total	= fits.open(data_path+file_name1)
unit1_time_total, unit1_rate_total, unit1_r_er_total = mf.data_extractor(unit1_data_total)

unit1_peak_features = np.loadtxt('unit1_fitted_vals_' + fitted_text + '.txt')
unit2_peak_features = np.loadtxt('unit2_fitted_vals_' + fitted_text + '.txt')
peak_time_from_file = np.loadtxt('peak_time_list_{}.txt'.format(args.peak_file_text))
peak_index 			= np.loadtxt('index_list_' + args.peak_file_text+ ".txt",dtype=int)

bounds = np.array([[1,1e-3,-100],[20000,100,-1e-3]])
min_bound = bounds[0]
max_bound = bounds[1]
#~ good_fits_index = np.where ()

labels = ['A','w1','w2']

good_fits_flag = np.ones(len(peak_index))					# We will store 1 for good fit and 0 for bad	

boundary_frac_dist = args.boundary_dist								# How far from the boundary the fit parameter has to be

for i,par in enumerate(labels):
	bad_fit_index = np.where( (np.abs(unit1_peak_features[:,i] - min_bound[i])< boundary_frac_dist * np.abs(min_bound[i])) 
							| (np.abs(unit1_peak_features[:,i] - max_bound[i])< boundary_frac_dist * np.abs(max_bound[i])) 
							| (np.abs(unit2_peak_features[:,i] - min_bound[i])< boundary_frac_dist * np.abs(min_bound[i])) 
							| (np.abs(unit2_peak_features[:,i] - max_bound[i])< boundary_frac_dist * np.abs(max_bound[i])) ) [0]
	good_fits_flag[bad_fit_index] = 0

print len(good_fits_flag), np.sum(good_fits_flag)	

out_text = args.output_text

good_fits_flag = good_fits_flag.astype(bool)
np.savetxt("good_fit_flag_{}.txt".format(out_text),good_fits_flag)


##### Comparing pars in different units to see if the shot is present in both. 


shot_flag = good_fits_flag.copy()						# 1 for Shot 0 otherwise. It assumes bad fits are not shots

par_diff_ratio = args.par_ratio							# We compute the ratio of pars and see if they lie within 1*par_diff_ratio of 1

for i in range (1,np.shape(unit1_peak_features)[1]):
	par_ratio = unit1_peak_features[:,i]/unit2_peak_features[:,i]
	no_shot_index = np.where( (par_ratio < 1-par_diff_ratio) | ( par_ratio > 1 + par_diff_ratio )) [0]
	
	shot_flag[no_shot_index] = 0 
	
print len(good_fits_flag), np.sum(good_fits_flag), np.sum(shot_flag)

np.savetxt("shot_flag_{}.txt".format(out_text),shot_flag)

## Saving the GTI of the shot

gti_start 	= []
gti_stop	= []

for i, peak_ind in enumerate(peak_index[shot_flag]):
	peak_indices = mf.peak_isolator(peak_ind,unit1_time_total,peak_duration=4)
	gti_start.append(unit1_time_total[peak_indices[0]])
	gti_stop.append(unit1_time_total[peak_indices[-1]])

np.savetxt("GTI_shots_{}.txt".format(out_text),np.transpose([gti_start,gti_stop]))
