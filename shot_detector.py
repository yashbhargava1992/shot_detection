########################################################################
# The target is to detect peaks in the light curve which correspond to 
# shots. Physically shots should be detected in all the instruments 'simultaneously' and in all energies
# Thus this can be a great discrimnator to find if the peak we see is a real or a fake shot. 
# This version of the code will detect shots in one unit and one energy band.  
########################################################################
########################################################################




import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import my_funcs as mf
import argparse 


pr = argparse.ArgumentParser()

pr.add_argument("--lcdatadir", 		"-d",default="../lc_data/")
pr.add_argument("--filename", 		"-i1",default="laxpc_lc_0p05_unit1_3.0_80.0keV.lc")
pr.add_argument("--output_text", 	"-o",default="")

pr.add_argument("--shot_sep", 		"-s",type=float,default=0.5)
pr.add_argument("--search_length",	"-t",type=float,default=32.0)
pr.add_argument("--significance", 	"-f",type=float,default=3)
pr.add_argument("--method", 		"-m",default='std')


args = pr.parse_args()


data_path = args.lcdatadir
file_name = args.filename

if data_path[-1]!='/': data_path = data_path+'/'
unit1_data_band1	= fits.open(data_path+file_name)


unit1_time_band1, unit1_rate_band1, unit1_r_er_band1 = mf.data_extractor(unit1_data_band1)

#~ print unit1_time_band1[-1]-unit1_time_band1[0]
gap_start = mf.gap_detector(unit1_time_band1,10)
gap_end = gap_start+1
#~ print gap_start

list_of_peak_indices = []
list_of_peak_times = []

# Search criteria
f = args.significance
T = args.search_length
shot_sep = args.shot_sep


for i,seg_end in enumerate(gap_start):

	if i==0: short_seg = np.arange(0,seg_end,1)
	elif i==len(gap_start)-1: 
		short_seg = np.arange(gap_end[i],len(unit1_time_band1),1)
	else: short_seg = np.arange(gap_end[i-1],seg_end,1)

	peak_pos,other_peaks = mf.peak_detector(unit1_time_band1[short_seg], unit1_rate_band1[short_seg], unit1_r_er_band1[short_seg],
										f=f,T=T,shot_sep=shot_sep,small_peak_flag=True,sig_det='std')
	#~ peak_pos = mf.peak_detector(unit1_time_band1[short_seg], unit1_rate_band1[short_seg], unit1_r_er_band1[short_seg],f=1,T=2,shot_sep=-1,small_peak_flag=False)

	list_of_peak_indices = np.append(list_of_peak_indices,short_seg[peak_pos])
	list_of_peak_times = np.append(list_of_peak_times,unit1_time_band1[short_seg][peak_pos])

out_text = args.output_text

np.savetxt('index_list_' + out_text + '.txt',list_of_peak_indices,fmt='%1i')		# Saving the list of indices to be used with 0.05 s LC of the observation. 
np.savetxt('peak_time_list_' + out_text + '.txt',list_of_peak_times)
