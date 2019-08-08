import numpy as np 

def rebinner(x,y,rebin_factor,rate_flag):
	"""
	The function returns a rebinned array based on the rebin factor provided.
	Currently The function is not written. #the rebin factor should be a natural number. 
	Support for log binning (via a negative number will be provided soon)
	
	
	
	
	"""
	return None

def gap_detector (time,f=3, dt=None):
	"""
	
	Detects gap in the time series. Returns the index of the array supplied when the next time stamp 
	is atleast 'f' times 'dt' more than the current time stamp. If None, dt is computed in the function itself
	
	INPUT:
	
	time						: Array in which gaps are to searched for
	f							: The factor by which the consecutive time stamps should be separated to be considered a gap
	dt							: Minimum time bin of the array
	
	
	OUTPUT:
	
	index						: Start index of the gap
	
	
	"""
	diff = time[1:]-time[:-1]
	
	if dt == None: dt = np.median (diff)
	index_gap_start = np.where(diff>f*dt)[0]
	
	return index_gap_start
	
	



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



def peak_detector(time,rate,rerr,f=1,T=10,shot_sep=1,small_peak_flag=False, sig_det = 'med'):
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
	small_peak_flag				:True if you want to return the lower peaks. 
	sig_det						:Determines the method of sig determination Median of present error (med), STD of rate (std) or error propgation (pro)
	
	OUTPUT:
	peak_index_pos				: The index position of the peaks. 
	lower_peaks					: Other peaks which are within 1 sig pf the detected peak, returned if small_peak_flag is True
	
	Note: If small_peak_flag is True then the function returns a tuple of 2 arrays. 
	
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
		if sig_det == 'med': sig = np.median(seg_rerr)
		elif sig_det == 'std': sig = np.std(seg_rate)
		elif sig_det == 'pro': 
			print 'Propogation code is not written defaulting to med'
			sig = np.median(seg_rerr)
		else: 
			print 'Use med, std or pro only. \n I am going with med'
			sig = np.median(seg_rerr)
		peak_pos = int(np.argmax(seg_rate))
		peak_val = seg_rate[peak_pos]					# This value is the maximum count in the segment
		peak_time = seg_time[peak_pos]					# This value is the position of the peak in the segment. 
		other_peaks = np.where(seg_rate>peak_val-sig)[0]
		lower_peaks = np.append(lower_peaks,ind[other_peaks])
		if peak_val>np.mean(seg_rate)+sig*f:
			if peak_index_pos.size ==0:									# To ensure the consecutive shots are far enough. This condition can be applied at the end too
				peak_index_pos = np.append(peak_index_pos,int(ind[peak_pos]))
			elif len(peak_index_pos) !=0 and peak_time>time[peak_index_pos][-1]+shot_sep*T:
				peak_index_pos = np.append(peak_index_pos,int(ind[peak_pos]))
			elif len(peak_index_pos) !=0 and peak_time<time[peak_index_pos][-1]+shot_sep*T:			# To reatin the larger peak in the shot_sep duration
				if rate[peak_index_pos][-1] < peak_val: 
					peak_index_pos[-1] = int(ind[peak_pos])
				#~ print peak_index_pos.size	
		#~ else:
			#~ peak_index_pos = np.append(peak_index_pos,np.nan)
	peak_index_pos = peak_index_pos.astype(int)
	if small_peak_flag: return peak_index_pos,lower_peaks
	else: return peak_index_pos


def peak_isolator(peak_index,time,del_time=None, peak_duration=10.0):
	"""
	
	This function accepts an index value(peak_index) and returns a set of indices around that peak. 
	The duration around the peak is defaulted to 10s i.e. plus/minus 5s around the peak.
	
	INPUT:
	
	peak_index					: The position around which the indices will be returned
	time						: The time array corresponding to the peak_index
	del_time					: The minimum time bin of the time array (used to convert time to indices)
	peak_duration				: Duration of the peak Default value 10s
	
	
	OUTPUT:
	
	peak_profile_indices		: Array of index which correspond to the peak. 
	
	
	"""	
	
	diff = time[1:]-time[:-1]
	
	if del_time == None: del_time = np.median (diff)
	
	index_gap_start = gap_detector(time,3,del_time)
	
	number_of_indices = int(np.ceil(peak_duration/del_time))
	
	# Checking if the current peak is too close to a gap.
	
	distance_from_gap = index_gap_start-peak_index
	#~ print distance_from_gap
	
	closest_distance = np.argmin(np.abs(distance_from_gap))
	
	if (np.abs(distance_from_gap[closest_distance])< number_of_indices/2):
		
		if distance_from_gap[closest_distance] > 0:	
			# Means that the gap starts shortly after the peak
			peak_profile_indices = np.arange(peak_index - number_of_indices/2,index_gap_start[closest_distance],1)
		
		elif distance_from_gap[closest_distance] < 0:
			# Means that the gap ends shortly before the peak, +1 to gap start is done to get the gap end index
			peak_profile_indices = np.arange(index_gap_start[closest_distance]+1, peak_index + number_of_indices/2 + 1, 1)
		
		else : 
			print "The peak is at exactly gap start. Something is really wrong!!!!!!"
	
	else:
		peak_profile_indices = np.arange(peak_index - number_of_indices/2, peak_index + number_of_indices/2+1,1)
	
	return peak_profile_indices
