
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


unit1_time_band1, unit1_rate_band1, unit1_r_er_band1 = mf.data_extractor(unit1_data_band1)
unit2_time_band1, unit2_rate_band1, unit2_r_er_band1 = mf.data_extractor(unit2_data_band1)
unit1_time_band2, unit1_rate_band2, unit1_r_er_band2 = mf.data_extractor(unit1_data_band2)
unit2_time_band2, unit2_rate_band2, unit2_r_er_band2 = mf.data_extractor(unit2_data_band2)


gap_start = mf.gap_detector(unit1_time_band1,10)
gap_end = gap_start+1

shot_par_list = []


