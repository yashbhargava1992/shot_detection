
### Program to see the distribution of the shots.



import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import my_funcs as mf


data_path = "../lc_data/"

unit1_data_band1	= fits.open(data_path+"laxpc_lc_0p05_unit1_3.0_5.0keV.lc")
unit1_data_band2	= fits.open(data_path+"laxpc_lc_0p05_unit1_5.0_10.0keV.lc")
unit2_data_band1	= fits.open(data_path+"laxpc_lc_0p05_unit2_3.0_5.0keV.lc")
unit2_data_band2	= fits.open(data_path+"laxpc_lc_0p05_unit2_5.0_10.0keV.lc")


unit1_time_band1, unit1_rate_band1, unit1_r_er_band1 = mf.data_extractor(unit1_data_band1)
unit2_time_band1, unit2_rate_band1, unit2_r_er_band1 = mf.data_extractor(unit2_data_band1)
unit1_time_band2, unit1_rate_band2, unit1_r_er_band2 = mf.data_extractor(unit1_data_band2)
unit2_time_band2, unit2_rate_band2, unit2_r_er_band2 = mf.data_extractor(unit2_data_band2)


gap_start = mf.gap_detector(unit1_time_band1,10)
gap_end = gap_start+1


f_list = np.arange(1,11,1)
number_peaks = np.zeros(len(f_list))

print f_list

stat_flag = False

if stat_flag:
	for x,f in enumerate(f_list):
		for i,seg_end in enumerate(gap_start):
		
			if i==0: short_seg = np.arange(0,seg_end,1)
			elif i==len(gap_start)-1: 
				short_seg = np.arange(gap_end[i],len(unit1_time_band1),1)
			else: short_seg = np.arange(gap_end[i-1],seg_end,1)
			
			#~ print np.median (unit1_r_er_band1[short_seg]), np.std(unit1_rate_band1[short_seg])
			peak_pos = mf.peak_detector(unit1_time_band1[short_seg], unit1_rate_band1[short_seg], unit1_r_er_band1[short_seg],
										f=f,T=16,shot_sep=0.25,small_peak_flag=False,sig_det='std')
			number_peaks[x] += len(peak_pos)					# This stores number of peaks detected which are greater than f-sigma. 
	
	
	print number_peaks
	
	# Computing number of peaks within f and f+1 sigma. Since we want a peak to be assigned to the bin with highest f,
	# we start from there (hence reversing the number_peaks array) and append the bin for the highest number as is. And then reversing it back
	
	diff_peaks = (np.append(number_peaks[-1],np.diff(number_peaks[::-1])))[::-1]
	print diff_peaks
	plt.plot(f_list,number_peaks)
	plt.plot(f_list,diff_peaks) 			
	#~ plt.bar(f_list[:-1],diff_peaks[::-1],width=1,align='edge')
	plt.yscale('log')
	#~ plt.show()

rate_hist = np.histogram (unit1_rate_band1[:gap_start[-3]],100)	

plt.plot(rate_hist[1][:-1],rate_hist[0],'.')
plt.xscale('log')
plt.show()
