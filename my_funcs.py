import numpy as np 

def rebinner(x,y,rebin_factor,rate_flag):
	"""
	The function returns a rebinned array based on the rebin factor provided.
	Currently the rebin factor should be a natural number. 
	Support for log binning (via a negative number will be provided soon)
	
	
	
	
	"""
	return None



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



