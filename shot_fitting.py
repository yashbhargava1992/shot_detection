
### THis routine will pick the shots as in the shot detection procedure and fit them with a profile
### The parameter for the shots will be tested 
### This version will fit the shots 



import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import my_funcs as mf
import argparse 


pr = argparse.ArgumentParser()

pr.add_argument("--lcdatadir", 		"-d",default="../lc_data/")
pr.add_argument("--filename1", 		"-i1",default="laxpc_lc_0p05_unit1_3.0_80.0keV.lc")
pr.add_argument("--filename2", 		"-i2",default="laxpc_lc_0p05_unit2_3.0_80.0keV.lc")
pr.add_argument("--output_text", 	"-o",default="")
pr.add_argument("--append_text", 	"-a",default="")
pr.add_argument("--peak_file_text", "-p",default="")

pr.add_argument("--peak_length", 	"-l", default=2, type = float)
pr.add_argument("--base_length", 	"-b", default=10, type = float)

args = pr.parse_args()


data_path = args.lcdatadir
file_name1 = args.filename1
file_name2 = args.filename2

if data_path[-1]!='/': data_path = data_path+'/'
unit1_data_band1	= fits.open(data_path+file_name1)
unit1_time_band1, unit1_rate_band1, unit1_r_er_band1 = mf.data_extractor(unit1_data_band1)
unit2_data_band1	= fits.open(data_path+file_name2)
unit2_time_band1, unit2_rate_band1, unit2_r_er_band1 = mf.data_extractor(unit2_data_band1)



gap_start = mf.gap_detector(unit1_time_band1,10)
gap_end = gap_start+1

shot_par_list = []

peak_file_name = args.append_text+"_index_list_" + args.peak_file_text + ".txt"
peak_index = np.loadtxt(peak_file_name,dtype=int)

offset_unit1_list = []
offset_unit2_list = []

peak_pars_unit1 = np.array([])
peak_pars_unit2 = np.array([])

print "Number of peaks",len(peak_index)

peak_length = args.peak_length
base_length = args.base_length
for i,index in enumerate(peak_index[:]):

	#~ print mf.peak_isolator(index,unit1_time_band1)
	
	base_profile_index = mf.peak_isolator(index,unit1_time_band1,peak_duration=base_length)
	peak_profile_index = mf.peak_isolator(index,unit1_time_band1,peak_duration=peak_length)
	
	# Plotting the peaks and the baseline
	#~ plt.plot(unit1_time_total[base_profile_index], unit1_rate_total[base_profile_index])
	#~ plt.plot(unit1_time_total[peak_profile_index], unit1_rate_total[peak_profile_index])
	#~ plt.plot(unit2_time_total[base_profile_index], unit2_rate_total[base_profile_index])
	#~ plt.plot(unit2_time_total[peak_profile_index], unit2_rate_total[peak_profile_index])
	
	only_base_index = np.setdiff1d(base_profile_index,peak_profile_index)
	#~ print peak_profile_index, only_base_index
	guess_vals = [100,0.1,-0.1]
	offset,popt,pcov = mf.peak_fitter(unit1_time_band1,unit1_rate_band1,only_base_index,index,peak_profile_index,guess_vals)
	#~ print i,'unit1', popt, guess_vals
	offset_unit1_list.append(offset)
	if i==0:
		peak_pars_unit1 = np.append(peak_pars_unit1,popt)
	else:	
		peak_pars_unit1 = np.vstack([peak_pars_unit1,popt])
	
	plt.plot(unit1_time_band1[base_profile_index], unit1_rate_band1[base_profile_index])
	plt.plot(unit1_time_band1[peak_profile_index], offset + mf.rise_n_decay(unit1_time_band1[peak_profile_index]-unit1_time_band1[index],*popt),'.')
	plt.plot(unit1_time_band1[peak_profile_index], offset + mf.rise_n_decay(unit1_time_band1[peak_profile_index]-unit1_time_band1[index],*guess_vals),'.')
	
	#~ if i%100==0:plt.show()
	plt.clf()
	offset,popt,pcov = mf.peak_fitter(unit2_time_band1,unit2_rate_band1,only_base_index,index,peak_profile_index,guess_vals)
	#~ print 'unit2',popt, guess_vals
	offset_unit2_list.append(offset)
	
	plt.plot(unit2_time_band1[base_profile_index], unit2_rate_band1[base_profile_index])
	plt.plot(unit2_time_band1[peak_profile_index], offset + mf.rise_n_decay(unit2_time_band1[peak_profile_index]-unit2_time_band1[index],*popt),'.')
	plt.plot(unit2_time_band1[peak_profile_index], offset + mf.rise_n_decay(unit2_time_band1[peak_profile_index]-unit2_time_band1[index],*guess_vals),'.')
	#~ plt.show()
	plt.clf()
	
	if i==0:
		peak_pars_unit2 = np.append(peak_pars_unit2,popt)
	else:	
		peak_pars_unit2 = np.vstack([peak_pars_unit2,popt])

print np.shape(peak_pars_unit1)

out_text = args.output_text

np.savetxt(args.append_text+'_unit1_fitted_vals_' + out_text + '.txt',peak_pars_unit1)			# Add saving using astropy.ascii.write. Will help in plotting.
np.savetxt(args.append_text+'_unit2_fitted_vals_' + out_text + '.txt',peak_pars_unit2)
