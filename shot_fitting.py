
### THis routine will pick the shots as in the shot detection procedure and fit them with a profile
### The parameter for the shots will be tested 



import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import my_funcs as mf


data_path = "../lc_data/"

unit1_data_band1	= fits.open(data_path+"laxpc_lc_0p05_unit1_3.0_5.0keV.lc")
unit1_data_band2	= fits.open(data_path+"laxpc_lc_0p05_unit1_5.0_10.0keV.lc")
unit2_data_band1	= fits.open(data_path+"laxpc_lc_0p05_unit2_3.0_5.0keV.lc")
unit2_data_band2	= fits.open(data_path+"laxpc_lc_0p05_unit2_5.0_10.0keV.lc")
unit1_data_total	= fits.open(data_path+"laxpc_lc_0p05_unit1_3.0_80.0keV.lc")
unit2_data_total	= fits.open(data_path+"laxpc_lc_0p05_unit2_3.0_80.0keV.lc")


unit1_time_band1, unit1_rate_band1, unit1_r_er_band1 = mf.data_extractor(unit1_data_band1)
unit2_time_band1, unit2_rate_band1, unit2_r_er_band1 = mf.data_extractor(unit2_data_band1)
unit1_time_band2, unit1_rate_band2, unit1_r_er_band2 = mf.data_extractor(unit1_data_band2)
unit2_time_band2, unit2_rate_band2, unit2_r_er_band2 = mf.data_extractor(unit2_data_band2)
unit1_time_total, unit1_rate_total, unit1_r_er_total = mf.data_extractor(unit1_data_total)
unit2_time_total, unit2_rate_total, unit2_r_er_total = mf.data_extractor(unit2_data_total)


gap_start = mf.gap_detector(unit1_time_band1,10)
gap_end = gap_start+1

shot_par_list = []

peak_index = np.loadtxt("index_list_0p05_unit1_fullrange.txt",dtype=int)
#~ peak_time_from_file = np.loadtxt('peak_time_list_0p05_unit1.txt')

#~ peak_time = unit1_time_band1[peak_index]
#~ peak_rate = unit1_rate_band1[peak_index]
#~ plt.plot(unit1_time_band1, unit1_rate_band1)
#~ plt.plot(peak_time,peak_rate,'.')
#~ plt.show()
offset_unit1_list = []
offset_unit2_list = []

peak_pars_unit1 = np.array([])
peak_pars_unit2 = np.array([])

print "Number of peaks",len(peak_index)
for i,index in enumerate(peak_index[:]):

	#~ print mf.peak_isolator(index,unit1_time_band1)
	
	base_profile_index = mf.peak_isolator(index,unit1_time_total,peak_duration=10)
	peak_profile_index = mf.peak_isolator(index,unit1_time_total,peak_duration=1)
	
	# Plotting the peaks and the baseline
	#~ plt.plot(unit1_time_total[base_profile_index], unit1_rate_total[base_profile_index])
	#~ plt.plot(unit1_time_total[peak_profile_index], unit1_rate_total[peak_profile_index])
	#~ plt.plot(unit2_time_total[base_profile_index], unit2_rate_total[base_profile_index])
	#~ plt.plot(unit2_time_total[peak_profile_index], unit2_rate_total[peak_profile_index])
	
	only_base_index = np.setdiff1d(base_profile_index,peak_profile_index)
	#~ print peak_profile_index, only_base_index
	guess_vals = [100,0.1,100,-0.1]
	offset,popt,pcov = mf.peak_fitter(unit1_time_total,unit1_rate_total,only_base_index,index,peak_profile_index,guess_vals)
	#~ print i,'unit1', popt, guess_vals
	offset_unit1_list.append(offset)
	if i==0:
		peak_pars_unit1 = np.append(peak_pars_unit1,popt)
	else:	
		peak_pars_unit1 = np.vstack([peak_pars_unit1,popt])
	
	plt.plot(unit1_time_total[base_profile_index], unit1_rate_total[base_profile_index])
	plt.plot(unit1_time_total[peak_profile_index], offset + mf.rise_n_decay(unit1_time_total[peak_profile_index]-unit1_time_total[index],*popt),'.')
	plt.plot(unit1_time_total[peak_profile_index], offset + mf.rise_n_decay(unit1_time_total[peak_profile_index]-unit1_time_total[index],*guess_vals),'.')
	
	#~ if i==361: plt.show()
	plt.clf()
	offset,popt,pcov = mf.peak_fitter(unit2_time_total,unit2_rate_total,only_base_index,index,peak_profile_index,guess_vals)
	#~ print 'unit2',popt, guess_vals
	offset_unit2_list.append(offset)
	
	plt.plot(unit2_time_total[base_profile_index], unit2_rate_total[base_profile_index])
	plt.plot(unit2_time_total[peak_profile_index], offset + mf.rise_n_decay(unit2_time_total[peak_profile_index]-unit2_time_total[index],*popt),'.')
	plt.plot(unit2_time_total[peak_profile_index], offset + mf.rise_n_decay(unit2_time_total[peak_profile_index]-unit2_time_total[index],*guess_vals),'.')
	#~ plt.show()
	plt.clf()
	if i==0:
		peak_pars_unit2 = np.append(peak_pars_unit2,popt)
	else:	
		peak_pars_unit2 = np.vstack([peak_pars_unit2,popt])

print np.shape(peak_pars_unit1)
np.savetxt('unit1_peak_fit_values.txt',peak_pars_unit1)
np.savetxt('unit2_peak_fit_values.txt',peak_pars_unit2)
