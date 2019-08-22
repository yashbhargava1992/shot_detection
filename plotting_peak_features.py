
# THe program will plot the pairwise variation of the parameters. 


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

rc('text',usetex=True)
rc('font',**{'size':14} )


unit1_peak_features = np.loadtxt('unit1_peak_fit_values.txt')
unit2_peak_features = np.loadtxt('unit2_peak_fit_values.txt')
peak_time_from_file = np.loadtxt('peak_time_list_0p05_unit1.txt')

print len(unit1_peak_features),len(peak_time_from_file)
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
				
		ax1.plot(np.abs(unit1_peak_features[:,j-1]),np.abs(unit1_peak_features[:,i-1]),marker='.',linestyle='None', markersize=0.5, color='k')
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

plt.savefig('Parameter_var_unit1_fitted_time.pdf')
plt.clf()


fig = plt.figure (figsize=(10,9))
fig.subplots_adjust(hspace=0, wspace=0,top=0.95, bottom=0.1,left = 0.15)

plt.suptitle("Unit 2 peak parameters for exp rise and decay")
number_of_columns = np.shape(unit2_peak_features)[1]
for i in range (1,number_of_columns+1,1):
	for j in range (1,i+1,1):
		ax1 = plt.subplot(number_of_columns,number_of_columns,(i-1)*number_of_columns+j)
				
		ax1.plot(np.abs(unit1_peak_features[:,j-1]),np.abs(unit1_peak_features[:,i-1]),marker='.',linestyle='None', markersize=0.5, color='k')
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
		ax1.plot(peak_time_from_file,np.abs(unit1_peak_features[:,i-1]),'.C0')
		ax1.plot(peak_time_from_file,np.abs(unit2_peak_features[:,i-1]),'.C1')
		ax1.set_ylabel(labels[i-1])
	else : 
		ax2 = plt.subplot(number_of_columns,1,i,sharex=ax1)
		ax2.plot(peak_time_from_file,np.abs(unit1_peak_features[:,i-1]),'.C0')
		ax2.plot(peak_time_from_file,np.abs(unit2_peak_features[:,i-1]),'.C1')
		ax2.set_ylabel(labels[i-1])
		ax2.set_yscale('log')
	if i== number_of_columns:
		ax2.set_xlabel('Time of the shot')

plt.show()
