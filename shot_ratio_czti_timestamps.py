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


data_path = ""
#~ data_path = "../lcv_czti_bin_0p05/"

czti_data_band1	= fits.open(data_path+"gti_lcv_spc_bin_0p05_20_40kev_Q0.lc")
czti_data_band2	= fits.open(data_path+"gti_lcv_spc_bin_0p05_40_80kev_Q0.lc")
czti_data_band3	= fits.open(data_path+"gti_lcv_spc_bin_0p05_80_100kev_Q0.lc")

#~ back_czti_data_band1 = fits.open(data_path+"Back_lightcurve_L1_3.0_5.0keV.lc")
#~ back_czti_data_band2 = fits.open(data_path+"Back_lightcurve_L1_5.0_10.0keV.lc")
#~ back_czti_data_band3 = fits.open(data_path+"Back_lightcurve_L1_10.0_20.0keV.lc")

czti_time_band1, czti_rate_band1, czti_r_er_band1 = mf.data_extractor(czti_data_band1)
czti_time_band2, czti_rate_band2, czti_r_er_band2 = mf.data_extractor(czti_data_band2)
czti_time_band3, czti_rate_band3, czti_r_er_band3 = mf.data_extractor(czti_data_band3)

#~ back_czti_time_band1, back_czti_rate_band1, back_czti_r_er_band1 = mf.data_extractor(back_czti_data_band1)
#~ back_czti_time_band2, back_czti_rate_band2, back_czti_r_er_band2 = mf.data_extractor(back_czti_data_band2)
#~ back_czti_time_band3, back_czti_rate_band3, back_czti_r_er_band3 = mf.data_extractor(back_czti_data_band3)

peaktime_list=[]
#~ peaktime_txt	= open(data_path+"peak_time_list_0p05_unit1.txt","r")
peaktime_txt	= open(data_path+"czti_3sig_peak_time_list_0p05_czti.txt","r")
for line in peaktime_txt : peaktime_list.append(float(line.rstrip()))
#~ print len(peaktime_list)
"""
Applying mask in the following segment

flag=[]
flag_txt		= open(data_path+"shot_flag.txt","r")
for line in flag_txt : flag.append(float(line.rstrip()))
flag=np.array(flag)
peaktime_list=np.array(peaktime_list)
peaktime_list=peaktime_list*flag
peaktime_list=peaktime_list[peaktime_list != 0]
#~ print "   ", len(peaktime_list)

Mask over
"""
peak_added_band1, count_peak=mf.peak_add_timestamp(czti_time_band1, czti_rate_band1, peaktime_list)
peak_added_band2, count_peak=mf.peak_add_timestamp(czti_time_band2, czti_rate_band2, peaktime_list)
peak_added_band3, count_peak=mf.peak_add_timestamp(czti_time_band3, czti_rate_band3, peaktime_list)
		
peak_added_band1=peak_added_band1
max_band1=np.max(peak_added_band1)
#~ peak_added_band1=peak_added_band1/max_band1

peak_added_band2=peak_added_band2
max_band2=np.max(peak_added_band2)
#~ peak_added_band2=peak_added_band2/max_band2

peak_added_band3=peak_added_band3
max_band3=np.max(peak_added_band3)

ratio1=peak_added_band2/peak_added_band1
ratio2=peak_added_band3/peak_added_band1

ax1 = plt.subplot(511)
ax1.plot(peak_added_band1, color='C0', marker='.', linestyle='None')
ax1.set_ylabel('Peak in 20-40 keV')

ax2 = plt.subplot(512, sharex=ax1)
ax2.plot(peak_added_band2, color='C1', marker='.', linestyle='None')
ax2.set_ylabel('Peak in 40-80 keV')

ax3 = plt.subplot(513,sharex=ax1)
ax3.plot(ratio1, color='C2', marker='.', linestyle='None')
ax3.set_ylabel('Ratio 40-80/20-40 keV')

ax4 = plt.subplot(514, sharex=ax1)
ax4.plot(peak_added_band3, color='C3', marker='.', linestyle='None')
ax4.set_ylabel('Peak in 80-100 keV')

ax5 = plt.subplot(515, sharex=ax1)
ax5.plot(ratio2, color='C2', marker='.', linestyle='None')
ax5.set_ylabel('Ratio 80-100/20-40 keV')

np.savetxt('cztidetect_3sig_time_co_added_0456_20.0_40.0_keV.txt',peak_added_band1)
np.savetxt('cztidetect_3sig_time_co_added_0456_40.0_80.0_keV.txt',peak_added_band2)
np.savetxt('cztidetect_3sig_time_co_added_0456_80.0_100.0_keV.txt',peak_added_band3)


plt.legend()
plt.show()

#~ print peak_added_band1
