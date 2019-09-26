########################################################################
# This routine segments the time around shots into even number of segments
# of same length say 1 s and creates sets of GTI to make PDS for GHATS
# NOTE : Run this routine only after running shot_detector.py
########################################################################


import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import my_funcs as mf
from astropy.io import ascii
from astropy.table import Table
import argparse 


pr = argparse.ArgumentParser()

pr.add_argument("--lcdatadir", 		"-d",default="../lc_data/")
pr.add_argument("--filename1",		"-i1",default="laxpc_lc_0p05_unit1_3.0_80.0keV.lc")

pr.add_argument("--output_text", 	"-o",default="")
pr.add_argument("--peak_file_text", "-p",default="")
pr.add_argument("--shot_flag_text", "-f",default="")

pr.add_argument("--number_seg", 	"-n",default=4,type = int)

args = pr.parse_args()


data_path = args.lcdatadir
file_name1 = args.filename1
if data_path[-1]!='/': data_path = data_path+'/'


unit1_data_total	= fits.open(data_path+file_name1)
unit1_time_total, unit1_rate_total, unit1_r_er_total = mf.data_extractor(unit1_data_total)


good_index 			= np.loadtxt('shot_flag_{}.txt'.format(args.shot_flag_text))
good_index 			= good_index.astype(bool)


peak_index = np.loadtxt("index_list_{}.txt".format(args.peak_file_text),dtype=int)

number_seg 	= args.number_seg
gti_start 	= np.array([]) 			# Holds start point of GTI of all segments, will be a 2d array finally
gti_stop 	= np.array([])
for i,index in enumerate(peak_index[good_index]):
	
	segmented_peak = mf.peak_segmenter(index, unit1_time_total, number_seg, peak_duration = 4) 
	#~ print segmented_peak[:,0],segmented_peak[:,-1], 
	if i==0: 
		gti_start 	= np.append(gti_start,segmented_peak[:,0])
		gti_stop	= segmented_peak[:,-1]
		#~ print gti_stop
	elif i>0:
		#~ print np.shape(gti_stop)
		gti_start 	= np.vstack([gti_start,segmented_peak[:,0]])
		gti_stop	= np.vstack([gti_stop,segmented_peak[:,-1]])
	#~ print np.shape(gti_start), np.shape(gti_stop)
#~ print np.shape(gti_start)
#~ i=0
#~ temp = np.array([unit1_time_total[gti_start[:,i].astype(int)],unit1_time_total[gti_stop[:,i].astype(int)]],dtype=float)
#~ print temp.dtype
for i in range(np.shape(gti_start)[1]):
	
	#~ np.savetxt("seg_gti_{}.txt".format(i), np.transpose([unit1_time_total[gti_start[:,i].astype(int)],unit1_time_total[gti_stop[:,i].astype(int)]]),fmt='%.3f, %.3f')
	
	tab_dat = Table([unit1_time_total[gti_start[:,i].astype(int)],unit1_time_total[gti_stop[:,i].astype(int)]])
	ascii.write(tab_dat, "seg_gti_{0}_{1}.txt".format(args.output_text,i), format='no_header',overwrite=True)
	
