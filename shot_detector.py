########################################################################
# The target is to detect peaks in the light curve which correspond to 
# shots. Physically shots should be detected in all the instruments 'simultaneously' and in all energies
# Thus this can be a great discrimnator to find if the peak we see is a real or a fake shot. 
########################################################################
########################################################################




import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import my_funcs as mf


data_path = "../lc_data/"

unit1_data_band1	= fits.open(data_path+"laxpc_lc_0p05_unit1_3.0_5.0keV.lc")
unit1_data_band2	= fits.open(data_path+"laxpc_lc_0p05_unit1_5.0_10.0keV.lc")
unit1_data_band3 	= fits.open(data_path+"laxpc_lc_0p05_unit1_10.0_20.0keV.lc")
unit2_data_band1	= fits.open(data_path+"laxpc_lc_0p05_unit2_3.0_5.0keV.lc")
unit2_data_band2	= fits.open(data_path+"laxpc_lc_0p05_unit2_5.0_10.0keV.lc")
unit2_data_band3 	= fits.open(data_path+"laxpc_lc_0p05_unit2_10.0_20.0keV.lc")
unit3_data_band1	= fits.open(data_path+"laxpc_lc_0p05_unit3_3.0_5.0keV.lc")
unit3_data_band2	= fits.open(data_path+"laxpc_lc_0p05_unit3_5.0_10.0keV.lc")
unit3_data_band3 	= fits.open(data_path+"laxpc_lc_0p05_unit3_10.0_20.0keV.lc")



unit1_time_band1, unit1_rate_band1, unit1_r_er_band1 = mf.data_extractor(unit1_data_band1)
unit2_time_band1, unit2_rate_band1, unit2_r_er_band1 = mf.data_extractor(unit2_data_band1)
unit3_time_band1, unit3_rate_band1, unit3_r_er_band1 = mf.data_extractor(unit3_data_band1)
unit1_time_band2, unit1_rate_band2, unit1_r_er_band2 = mf.data_extractor(unit1_data_band2)
unit2_time_band2, unit2_rate_band2, unit2_r_er_band2 = mf.data_extractor(unit2_data_band2)
unit3_time_band2, unit3_rate_band2, unit3_r_er_band2 = mf.data_extractor(unit3_data_band2)
unit1_time_band3, unit1_rate_band3, unit1_r_er_band3 = mf.data_extractor(unit1_data_band3)
unit2_time_band3, unit2_rate_band3, unit2_r_er_band3 = mf.data_extractor(unit2_data_band3)
unit3_time_band3, unit3_rate_band3, unit3_r_er_band3 = mf.data_extractor(unit3_data_band3)


jump = len(unit1_time_band1)/100
for i in range(0,len(unit1_time_band1),jump):
	
	short_seg = np.arange(i,i+jump,1)
	plt.errorbar(unit1_time_band1[short_seg], unit1_rate_band1[short_seg], yerr=unit1_r_er_band1[short_seg])
	peak_pos = mf.peak_detector(unit1_time_band1[short_seg], unit1_rate_band1[short_seg], unit1_r_er_band1[short_seg],f=2,T=5)
	plt.plot(unit1_time_band1[short_seg][peak_pos], unit1_rate_band1[short_seg][peak_pos],'o')
	plt.show()

