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
#~ data_path = "../orbitwise_lxp/"

unit1_data_band1	= fits.open(data_path+"laxpc_lc_0p05_unit1_3.0_5.0keV.lc")
unit1_data_band2	= fits.open(data_path+"laxpc_lc_0p05_unit1_5.0_10.0keV.lc")
unit1_data_band3 	= fits.open(data_path+"laxpc_lc_0p05_unit1_10.0_20.0keV.lc")
unit2_data_band1	= fits.open(data_path+"laxpc_lc_0p05_unit2_3.0_5.0keV.lc")
unit2_data_band2	= fits.open(data_path+"laxpc_lc_0p05_unit2_5.0_10.0keV.lc")
unit2_data_band3 	= fits.open(data_path+"laxpc_lc_0p05_unit2_10.0_20.0keV.lc")
unit3_data_band1	= fits.open(data_path+"laxpc_lc_0p05_unit3_3.0_5.0keV.lc")
unit3_data_band2	= fits.open(data_path+"laxpc_lc_0p05_unit3_5.0_10.0keV.lc")
unit3_data_band3 	= fits.open(data_path+"laxpc_lc_0p05_unit3_10.0_20.0keV.lc")

#~ back_unit1_data_band1 = fits.open(data_path+"Back_lightcurve_L1_3.0_5.0keV.lc")
#~ back_unit1_data_band2 = fits.open(data_path+"Back_lightcurve_L1_5.0_10.0keV.lc")
#~ back_unit1_data_band3 = fits.open(data_path+"Back_lightcurve_L1_10.0_20.0keV.lc")

unit1_time_band1, unit1_rate_band1, unit1_r_er_band1 = mf.data_extractor(unit1_data_band1)
unit2_time_band1, unit2_rate_band1, unit2_r_er_band1 = mf.data_extractor(unit2_data_band1)
unit3_time_band1, unit3_rate_band1, unit3_r_er_band1 = mf.data_extractor(unit3_data_band1)
unit1_time_band2, unit1_rate_band2, unit1_r_er_band2 = mf.data_extractor(unit1_data_band2)
unit2_time_band2, unit2_rate_band2, unit2_r_er_band2 = mf.data_extractor(unit2_data_band2)
unit3_time_band2, unit3_rate_band2, unit3_r_er_band2 = mf.data_extractor(unit3_data_band2)
unit1_time_band3, unit1_rate_band3, unit1_r_er_band3 = mf.data_extractor(unit1_data_band3)
unit2_time_band3, unit2_rate_band3, unit2_r_er_band3 = mf.data_extractor(unit2_data_band3)
unit3_time_band3, unit3_rate_band3, unit3_r_er_band3 = mf.data_extractor(unit3_data_band3)

#~ back_unit1_time_band1, back_unit1_rate_band1, back_unit1_r_er_band1 = mf.data_extractor(back_unit1_data_band1)
#~ back_unit1_time_band2, back_unit1_rate_band2, back_unit1_r_er_band2 = mf.data_extractor(back_unit1_data_band2)
#~ back_unit1_time_band3, back_unit1_rate_band3, back_unit1_r_er_band3 = mf.data_extractor(back_unit1_data_band3)


#~ print unit1_time_band1[-1]-unit1_time_band1[0]
gap_start = mf.gap_detector(unit1_time_band1,10)
gap_end = gap_start+1
print gap_start

''
#~ jump = len(unit1_time_band1)/246
#~ for i in range(0,len(unit1_time_band1),jump):
for i,seg_end in enumerate(gap_start):
	
	#~ if i+jump<=len(unit1_time_band1):short_seg = np.arange(i,i+jump,1)
	#~ else: short_seg = np.arange(i,len(unit1_time_band1),1)
	if i==0: short_seg = np.arange(0,seg_end,1)
	elif i==len(gap_start)-1: 
		short_seg = np.arange(gap_end[i],len(unit1_time_band1),1)
	else: short_seg = np.arange(gap_end[i-1],seg_end,1)
	
	print short_seg
	# Plotting shots in Band 1
	ax1 = plt.subplot(211)
	ax1.errorbar(unit1_time_band1[short_seg], unit1_rate_band1[short_seg], yerr=unit1_r_er_band1[short_seg],alpha=0.5,color='grey')
	#~ plt.plot(unit1_time_band1[short_seg], unit1_rate_band1[short_seg])
	#~ peak_pos = mf.peak_detector(unit1_time_band1[short_seg], unit1_rate_band1[short_seg], unit1_r_er_band1[short_seg],f=1,T=2,shot_sep=-1,small_peak_flag=False)
	peak_pos,other_peaks = mf.peak_detector(unit1_time_band1[short_seg], unit1_rate_band1[short_seg], unit1_r_er_band1[short_seg],f=5,T=32,shot_sep=0.5,small_peak_flag=True,sig_det='std')
	#~ ax1.plot(unit1_time_band1[short_seg][other_peaks], unit1_rate_band1[short_seg][other_peaks],'or',label='Other peaks')
	ax1.plot(unit1_time_band1[short_seg][peak_pos], unit1_rate_band1[short_seg][peak_pos],'og',label='SHOT')
	#~ ax1.errorbar(back_unit1_time_band1[short_seg], back_unit1_rate_band1[short_seg], yerr=back_unit1_r_er_band1[short_seg])
	ax1.set_ylabel('Count rate Unit1')
	plt.legend()
	print unit1_time_band1[short_seg][0], unit2_time_band1[short_seg][0]
	# Plotting the same pos in Band 2
	ax2 = plt.subplot(212,sharex=ax1)
	ax2.errorbar(unit2_time_band1[short_seg], unit2_rate_band1[short_seg], yerr=unit2_r_er_band1[short_seg],alpha=0.5,color='grey')
	#~ ax2.plot(unit2_time_band1[short_seg][other_peaks], unit2_rate_band1[short_seg][other_peaks],'or',label='Other peaks')
	ax2.plot(unit2_time_band1[short_seg][peak_pos], unit2_rate_band1[short_seg][peak_pos],'og',label='SHOT')
	ax2.set_ylabel('Count rate Unit2')
	ax2.set_xlabel('Time in s')

	
	# PLotting the ratio of the counts in B2 and B1
	#~ ax3 = plt.subplot(313,sharex=ax1)
	#~ rat_err,rat = mf.error_propagator_for_ratio(unit1_rate_band2[short_seg],unit1_r_er_band2[short_seg],unit1_rate_band1[short_seg],unit1_r_er_band1[short_seg],True)
	#~ ax3.plot(unit1_time_band2[short_seg], unit1_rate_band2[short_seg]/unit1_rate_band1[short_seg])
	#~ ax3.errorbar(unit1_time_band2[short_seg], rat,yerr=rat_err,alpha=0.5)
	#~ ax3.plot(unit1_time_band2[short_seg][other_peaks], rat[other_peaks],'o',label='Other peaks')
	#~ ax3.plot(unit1_time_band2[short_seg][peak_pos], rat[peak_pos],'o',label='SHOT')
	
	
	
	plt.show()
	plt.clf()

''
