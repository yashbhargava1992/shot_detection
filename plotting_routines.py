
# The program will plot the pairwise variation of the parameters, 
# Variation of parameters with time and co-added shots. 
# Note: Run this program after running shot_fitting, shot_ratio, shot_selector



import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

rc('text',usetex=True)
rc('font',**{'size':14} )


unit1_peak_features = np.loadtxt('unit1_peak_fit_values.txt')
unit2_peak_features = np.loadtxt('unit2_peak_fit_values.txt')
peak_time_from_file = np.loadtxt('peak_time_list_0p05_unit1.txt')
good_index 			= np.loadtxt('shot_flag.txt')
#~ good_index 			= np.ones(len(peak_time_from_file))		# Use this if all peaks are to be plotted

good_index 	= good_index.astype(bool)
print len(unit1_peak_features),len(peak_time_from_file), good_index
#~ plt.plot(unit1_peak_features[:,0],unit2_peak_features[:,0],'.')
#~ plt.show()

labels = ['t0','A','w1','w2']
#~ labels = ['A1','w1','A2','w2']
#~ fig = plt.figure()
fig = plt.figure (figsize=(10,9))
fig.subplots_adjust(hspace=0, wspace=0,top=0.95, bottom=0.1,left = 0.15)

plt.suptitle("Unit 1 peak parameters for exp rise and decay")   # suptitle is used for overall title

number_of_columns = np.shape(unit1_peak_features)[1]
for i in range (1,number_of_columns+1,1):
	for j in range (1,i+1,1):
		ax1 = plt.subplot(number_of_columns,number_of_columns,(i-1)*number_of_columns+j)
				
		ax1.plot(np.abs(unit1_peak_features[:,j-1])[good_index],np.abs(unit1_peak_features[:,i-1])[good_index],marker='.',linestyle='None', markersize=0.5, color='k')
		#~ ax1.set_xscale('log')
		#~ ax1.set_yscale('log')
		ax1.tick_params(right=True, top = True,direction = 'in')
		if i==4: 
			ax1.set_xlabel(labels[j-1])		# Putting labels only at the edge of the triangle
			ax1.tick_params(direction = 'inout')
		else: ax1.tick_params(labelbottom=False)
		if j==1: 
			ax1.set_ylabel(labels[i-1])		# Putting labels only at the edge of the triangle
			ax1.tick_params(direction = 'inout')
		else: 
			ax1.tick_params(labelleft=False)
			ax1.set_yscale('log')
			ax1.set_xscale('log')

#~ plt.show()
plt.savefig('Parameter_var_unit1_fitted_time.pdf')
plt.clf()


fig = plt.figure (figsize=(10,9))
fig.subplots_adjust(hspace=0, wspace=0,top=0.95, bottom=0.1,left = 0.15)

plt.suptitle("Unit 2 peak parameters for exp rise and decay")
number_of_columns = np.shape(unit2_peak_features)[1]
for i in range (1,number_of_columns+1,1):
	for j in range (1,i+1,1):
		ax1 = plt.subplot(number_of_columns,number_of_columns,(i-1)*number_of_columns+j)
				
		ax1.plot(np.abs(unit1_peak_features[:,j-1])[good_index],np.abs(unit1_peak_features[:,i-1])[good_index],marker='.',linestyle='None', markersize=0.5, color='k')
		#~ ax1.set_xscale('log')
		#~ ax1.set_yscale('log')
		ax1.tick_params(right=True, top = True,direction = 'in')
		if i==4: 
			ax1.set_xlabel(labels[j-1])		# Putting labels only at the edge of the triangle
			ax1.tick_params(direction = 'inout')
		else: ax1.tick_params(labelbottom=False)
		if j==1: 
			ax1.set_ylabel(labels[i-1])		# Putting labels only at the edge of the triangle
			ax1.tick_params(direction = 'inout')
		else: ax1.tick_params(labelleft=False)

plt.savefig('Parameter_var_unit2_fitted_time.pdf')
#~ plt.show()
plt.clf()

fig = plt.figure (figsize=(10,9))
fig.subplots_adjust(hspace=0, wspace=0,top=0.95, bottom=0.1,left = 0.15)

for i in range (1,number_of_columns+1):
	if i==1 : 
		ax1 = plt.subplot(number_of_columns,1,i)
		ax1.plot(peak_time_from_file[good_index],np.abs(unit1_peak_features[:,i-1])[good_index],'.C0')
		ax1.plot(peak_time_from_file[good_index],np.abs(unit2_peak_features[:,i-1])[good_index],'.C1')
		ax1.set_ylabel(labels[i-1])
	else : 
		ax2 = plt.subplot(number_of_columns,1,i,sharex=ax1)
		ax2.plot(peak_time_from_file[good_index],np.abs(unit1_peak_features[:,i-1])[good_index],'.C0')
		ax2.plot(peak_time_from_file[good_index],np.abs(unit2_peak_features[:,i-1])[good_index],'.C1')
		ax2.set_ylabel(labels[i-1])
		ax2.set_yscale('log')
	if i== number_of_columns:
		ax2.set_xlabel('Time of the shot')

plt.show()

# Plotting co-added shots

peak_added_band1 = np.loadtxt('co_added_0456_laxpc20_3.0_5.0_keV.txt')		# Saving the list of indices to be used with 0.05 s LC of the observation. 
peak_added_band2 = np.loadtxt('co_added_0456_laxpc20_5.0_10.0_keV.txt')
peak_added_band3 = np.loadtxt('co_added_0456_laxpc20_10.0_20.0_keV.txt')
peak_added_band4 = np.loadtxt('co_added_0456_laxpc20_20.0_40.0_keV.txt')
peak_added_band5 = np.loadtxt('co_added_0456_laxpc20_40.0_80.0_keV.txt')


ratio1=peak_added_band2/peak_added_band1
ratio2=peak_added_band3/peak_added_band1
ratio3=peak_added_band4/peak_added_band1
ratio4=peak_added_band5/peak_added_band1

ax1 = plt.subplot(411)
ax1.plot(ratio1, color='C1', marker='.', linestyle='None')
ax1.set_ylabel('Ratio 5-10/3-5 keV')

ax2 = plt.subplot(412, sharex=ax1)
ax2.plot(ratio2, color='C2', marker='.', linestyle='None')
ax2.set_ylabel('Ratio 10-20/3-5 keV')


ax3 = plt.subplot(413, sharex=ax1)
ax3.plot(ratio3, color='C0', marker='.', linestyle='None')
ax3.set_ylabel('Ratio 20-40/3-5 keV')

ax3 = plt.subplot(414, sharex=ax1)
ax3.plot(ratio3, color='C3', marker='.', linestyle='None')
ax3.set_ylabel('Ratio 40-80/3-5 keV')

plt.legend()
plt.show()

