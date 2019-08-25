########################################################################
# This routine co-adds shots from two energy bands and finds their ratio
# to check whether the profile has any characteristic feature during
# rise and decay of the shot
# NOTE : Run this routine only after running shot_detector.py
########################################################################





import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import my_funcs as mf


data_path = "../lc_data/"
#~ data_path = ""
#~ data_path = "../orbitwise_lxp/"

unit1_data_band1	= fits.open(data_path+"laxpc_lc_0p05_unit1_3.0_5.0keV.lc")
unit1_data_band2	= fits.open(data_path+"laxpc_lc_0p05_unit1_5.0_10.0keV.lc")
unit1_data_band3	= fits.open(data_path+"laxpc_lc_0p05_unit1_10.0_20.0keV.lc")
unit1_data_band4	= fits.open(data_path+"laxpc_lc_0p05_unit1_20.0_40.0keV.lc")
unit1_data_band5	= fits.open(data_path+"laxpc_lc_0p05_unit1_40.0_80.0keV.lc")

unit2_data_band1	= fits.open(data_path+"laxpc_lc_0p05_unit2_3.0_5.0keV.lc")
unit2_data_band2	= fits.open(data_path+"laxpc_lc_0p05_unit2_5.0_10.0keV.lc")
unit2_data_band3	= fits.open(data_path+"laxpc_lc_0p05_unit2_10.0_20.0keV.lc")
unit2_data_band4	= fits.open(data_path+"laxpc_lc_0p05_unit2_20.0_40.0keV.lc")
unit2_data_band5	= fits.open(data_path+"laxpc_lc_0p05_unit2_40.0_80.0keV.lc")

#~ back_unit1_data_band1 = fits.open(data_path+"Back_lightcurve_L1_3.0_5.0keV.lc")
#~ back_unit1_data_band2 = fits.open(data_path+"Back_lightcurve_L1_5.0_10.0keV.lc")
#~ back_unit1_data_band3 = fits.open(data_path+"Back_lightcurve_L1_10.0_20.0keV.lc")

unit1_time_band1, unit1_rate_band1, unit1_r_er_band1 = mf.data_extractor(unit1_data_band1)
unit1_time_band2, unit1_rate_band2, unit1_r_er_band2 = mf.data_extractor(unit1_data_band2)
unit1_time_band3, unit1_rate_band3, unit1_r_er_band3 = mf.data_extractor(unit1_data_band3)
unit1_time_band4, unit1_rate_band4, unit1_r_er_band4 = mf.data_extractor(unit1_data_band4)
unit1_time_band5, unit1_rate_band5, unit1_r_er_band5 = mf.data_extractor(unit1_data_band5)

unit2_time_band1, unit2_rate_band1, unit2_r_er_band1 = mf.data_extractor(unit2_data_band1)
unit2_time_band2, unit2_rate_band2, unit2_r_er_band2 = mf.data_extractor(unit2_data_band2)
unit2_time_band3, unit2_rate_band3, unit2_r_er_band3 = mf.data_extractor(unit2_data_band3)
unit2_time_band4, unit2_rate_band4, unit2_r_er_band4 = mf.data_extractor(unit2_data_band4)
unit2_time_band5, unit2_rate_band5, unit2_r_er_band5 = mf.data_extractor(unit2_data_band5)

#~ back_unit1_time_band1, back_unit1_rate_band1, back_unit1_r_er_band1 = mf.data_extractor(back_unit1_data_band1)
#~ back_unit1_time_band2, back_unit1_rate_band2, back_unit1_r_er_band2 = mf.data_extractor(back_unit1_data_band2)
#~ back_unit1_time_band3, back_unit1_rate_band3, back_unit1_r_er_band3 = mf.data_extractor(back_unit1_data_band3)

#~ index_list=[]
#~ index_txt	= open("index_list_0p05_unit1_fullrange.txt","r")
#~ for line in index_txt : index_list.append(int(line.rstrip()))
index_list = np.loadtxt("index_list_0p05_unit1_fullrange.txt")

peak_added_band1, count_peak=mf.peak_add(unit2_time_band1, unit2_rate_band1, index_list)
peak_added_band2, count_peak=mf.peak_add(unit2_time_band2, unit2_rate_band2, index_list)
peak_added_band3, count_peak=mf.peak_add(unit2_time_band3, unit2_rate_band3, index_list)
peak_added_band4, count_peak=mf.peak_add(unit2_time_band4, unit2_rate_band4, index_list)
peak_added_band5, count_peak=mf.peak_add(unit2_time_band5, unit2_rate_band5, index_list)
			
peak_added_band1=peak_added_band1/count_peak
max_band1=np.max(peak_added_band1)
#~ peak_added_band1=peak_added_band1/max_band1

peak_added_band2=peak_added_band2/count_peak
max_band2=np.max(peak_added_band2)
#~ peak_added_band2=peak_added_band2/max_band2

peak_added_band3=peak_added_band3/count_peak
max_band3=np.max(peak_added_band3)

peak_added_band4=peak_added_band4/count_peak
max_band4=np.max(peak_added_band4)

peak_added_band5=peak_added_band5/count_peak
max_band5=np.max(peak_added_band5)


np.savetxt('co_added_0456_laxpc20_3.0_5.0_keV.txt',peak_added_band1)		# Saving the list of indices to be used with 0.05 s LC of the observation. 
np.savetxt('co_added_0456_laxpc20_5.0_10.0_keV.txt',peak_added_band2)
np.savetxt('co_added_0456_laxpc20_10.0_20.0_keV.txt',peak_added_band3)
np.savetxt('co_added_0456_laxpc20_20.0_40.0_keV.txt',peak_added_band4)
np.savetxt('co_added_0456_laxpc20_40.0_80.0_keV.txt',peak_added_band5)



#~ print peak_added_band1
