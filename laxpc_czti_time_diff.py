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

czti_data_band1		= fits.open(data_path+"gti_lcv_spc_bin_0p05_20_40kev_Q0.lc")
laxpc_data_band1	= fits.open(data_path+"laxpc_lc_0p05_unit1_20.0_40.0keV.lc")


czti_time_band1, czti_rate_band1, czti_r_er_band1 = mf.data_extractor(czti_data_band1)
laxpc_time_band1, laxpc_rate_band1, laxpc_r_er_band1 = mf.data_extractor(laxpc_data_band1)

time_diff	=	np.abs(czti_time_band1[:-66]-laxpc_time_band1)

ax1 = plt.subplot(111)
ax1.plot(time_diff, color='C0', marker='.', linestyle='None')
ax1.set_yscale("log")
ax1.set_ylabel('Time diff in 20-40 keV')


plt.legend()
plt.show()

#~ print peak_added_band1
