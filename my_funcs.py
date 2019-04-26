import numpy as np 

def rebinner(x,y,rebin_factor,rate_flag):
	"""
	The function returns a rebinned array based on the rebin factor provided.
	Currently the rebin factor should be a natural number. 
	Support for log binning (via a negative number will be provided soon)
	
	
	
	
	"""
	return None

def error_propagator_for_ratio(num,num_err,den,den_err,ratio_flag=False):
	"""
	
	Computes the error for the ratio of 2 time series (currently). Also returns the ratio itself if ratio flag is set true
	
	INPUT:
	
	num							: Numerator for the ratio
	num_err						: Error on numerator
	den							: Denominator for the ratio
	den_err						: Error on denominator
	ratio_flag					: If true, returns the ratio and the error on the ratio
	
	OUTPUT:
	
	rat_err						: Error on the ratio
	ratio						: Returned if ratio flag is true
	
	
	"""
	
	ratio = num/den
	rat_err = ratio * (num_err/num+den_err/den)
	if ratio_flag: return rat_err,ratio
	else: rat_err
	

def data_extractor(fits_file_object):
	
	"""
	
	Takes in the object opened by fits.open and returns the time rate and rate_error arrays from the 1st extension of the same object
	
	
	INPUT:
	
	fits_file_object			:The object from fits.open
	
	
	OUTPUT:
	time						:Time array from the first extension
	rate						:Rate array from the first extension
	rate_error					:Error on the rate array from the first extension
	
	"""
	time = (fits_file_object[1].data)['Time']
	rate = (fits_file_object[1].data)['Rate']
	rate_error = (fits_file_object[1].data)['Error']
	
	return time,rate,rate_error



def peak_detector(time,rate,rerr,f=1,T=10,shot_sep=1,small_peak_flag=False):
	"""
	
	Takes the light curve (with err on the rate) and returns the position of the peaks with which are certain fraction above the mean. 
	Note: This doesn't fit the peak with anything. The computing is done using a simple comparison. The current version can detect peaks in discrete windows
	For example the code will divide the LC into segments of length T and return the highest peaks in each segment. 
	A more refined detection will be attempted later
	
	INPUT:
	time						:Time array of the LC 
	rate						:Rate array of the LC
	rerr						:Error on the rate
	f							:The factor by which the peak should be greater than the mean level, typically greater than 1
	T							:The duration of the time for which the mean has to be computed. same unit as time
	shot_sep					:Minimum separation between 2 consecutive 'shots'
	
	OUTPUT:
	peak_index_pos				: The index position of the peaks. 
	lower_peaks					: Other peaks which are within 1 sig pf the detected peak, returned if small_peak_flag is True
	
	
	
	"""
	
	total_duration = time[-1]-time[0]
	number_of_segments = int(total_duration/T)
	jump = len(time)/number_of_segments
	peak_index_pos = np.array([],dtype=int)
	lower_peaks = np.array([],dtype=int)
	
	for i in range(0,len(time),jump):
		
		if i+jump<=len(time):ind = np.arange (i,i+jump,1)				# taking care of the trailing part of the array 
		else : ind=np.arange (i,len(time),1)							# which doesn't have the same number of points as the jump	
		seg_time = time[ind]
		seg_rate = rate[ind]
		seg_rerr = rerr[ind]
		sig = np.median(seg_rerr)
		peak_pos = int(np.argmax(seg_rate))
		peak_val = seg_rate[peak_pos]					# This value is the maximum count in the segment
		peak_time = seg_time[peak_pos]					# This value is the position of the peak in the segment. 
		other_peaks = np.where(seg_rate>peak_val-sig)[0]
		lower_peaks = np.append(lower_peaks,ind[other_peaks])
		if peak_val>np.mean(seg_rate)*f:
			if peak_index_pos.size ==0:									# To ensure the consecutive shots are far enough. This condition can be applied at the end too
				peak_index_pos = np.append(peak_index_pos,int(ind[peak_pos]))
			elif len(peak_index_pos) !=0 and peak_time>time[peak_index_pos][-1]+shot_sep*T:
				peak_index_pos = np.append(peak_index_pos,int(ind[peak_pos]))
		#~ print peak_index_pos.size	
		#~ else:
			#~ peak_index_pos = np.append(peak_index_pos,np.nan)
	peak_index_pos = peak_index_pos.astype(int)
	if small_peak_flag: return peak_index_pos,lower_peaks
	else: return peak_index_pos
	
	 
