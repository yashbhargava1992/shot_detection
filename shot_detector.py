########################################################################
# The target is to detect peaks in the light curve which correspond to 
# shots. Physically shots should be detected in all the instruments 'simultaneously' and in all energies
# Thus this can be a great discrimnator to find if the peak we see is a real or a fake shot. 
########################################################################
########################################################################




import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits


unit1_data_3_5 		= fits.open("lc_data/laxpc_lc_5s_unit1_3.0_5.0keV.lc")
unit1_data_5_10 	= fits.open("lc_data/laxpc_lc_5s_unit1_5.0_10.0keV.lc")
unit1_data_10_20 	= fits.open("lc_data/laxpc_lc_5s_unit1_10.0_20.0keV.lc")
unit2_data_3_5 		= fits.open("lc_data/laxpc_lc_5s_unit2_3.0_5.0keV.lc")
unit2_data_5_10 	= fits.open("lc_data/laxpc_lc_5s_unit2_5.0_10.0keV.lc")
unit2_data_10_20 	= fits.open("lc_data/laxpc_lc_5s_unit2_10.0_20.0keV.lc")
unit3_data_3_5 		= fits.open("lc_data/laxpc_lc_5s_unit3_3.0_5.0keV.lc")
unit3_data_5_10 	= fits.open("lc_data/laxpc_lc_5s_unit3_5.0_10.0keV.lc")
unit3_data_10_20 	= fits.open("lc_data/laxpc_lc_5s_unit3_10.0_20.0keV.lc")


unit1_time_3_5 		= (unit1_data_3_5[1].data)["Time"]
unit1_rate_3_5 		= (unit1_data_3_5[1].data)["Rate"]
unit1_r_er_3_5 		= (unit1_data_3_5[1].data)["Error"]
unit1_time_5_10 	= (unit1_data_5_10[1].data)["Time"]
unit1_rate_5_10 	= (unit1_data_5_10[1].data)["Rate"]
unit1_r_er_5_10 	= (unit1_data_5_10[1].data)["Error"]
unit1_time_10_20 	= (unit1_data_10_20[1].data)["Time"]
unit1_rate_10_20 	= (unit1_data_10_20[1].data)["Rate"]
unit1_r_er_10_20 	= (unit1_data_10_20[1].data)["Error"]
unit2_time_3_5 		= (unit2_data_3_5[1].data)["Time"]
unit2_rate_3_5 		= (unit2_data_3_5[1].data)["Rate"]
unit2_r_er_3_5 		= (unit2_data_3_5[1].data)["Error"]
unit2_time_5_10 	= (unit2_data_5_10[1].data)["Time"]
unit2_rate_5_10 	= (unit2_data_5_10[1].data)["Rate"]
unit2_r_er_5_10 	= (unit2_data_5_10[1].data)["Error"]
unit2_time_10_20 	= (unit2_data_10_20[1].data)["Time"]
unit2_rate_10_20 	= (unit2_data_10_20[1].data)["Rate"]
unit2_r_er_10_20 	= (unit2_data_10_20[1].data)["Error"]
unit3_time_3_5 		= (unit3_data_3_5[1].data)["Time"]
unit3_rate_3_5 		= (unit3_data_3_5[1].data)["Rate"]
unit3_r_er_3_5 		= (unit3_data_3_5[1].data)["Error"]
unit3_time_5_10 	= (unit3_data_5_10[1].data)["Time"]
unit3_rate_5_10 	= (unit3_data_5_10[1].data)["Rate"]
unit3_r_er_5_10 	= (unit3_data_5_10[1].data)["Error"]
unit3_time_10_20 	= (unit3_data_10_20[1].data)["Time"]
unit3_rate_10_20 	= (unit3_data_10_20[1].data)["Rate"]
unit3_r_er_10_20 	= (unit3_data_10_20[1].data)["Error"]



