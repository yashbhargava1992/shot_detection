import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

rc('text',usetex=True)
rc('font',**{'size':14} )


unit1_peak_features = np.loadtxt('unit1_peak_fit_values.txt')
unit2_peak_features = np.loadtxt('unit2_peak_fit_values.txt')

#~ plt.plot(unit1_peak_features[:,0],unit2_peak_features[:,0],'.')
#~ plt.show()

labels = ['A1','w1','A2','w2']
#~ fig = plt.figure()
fig = plt.figure (figsize=(10,9))
fig.subplots_adjust(hspace=0, wspace=0,top=0.95, bottom=0.1,left = 0.15)


for i in range (1,5,1):
	for j in range (1,i+1,1):
		ax1 = plt.subplot(4,4,(i-1)*4+j)
				
		ax1.plot(np.abs(unit1_peak_features[:,j-1]),np.abs(unit1_peak_features[:,i-1]),'.')
		ax1.set_xscale('log')
		ax1.set_yscale('log')
		ax1.tick_params(right=True, top = True,direction = 'in')
		if i==4: 
			ax1.set_xlabel(labels[j-1])		# Putting labels only at the edge of the triangle
			ax1.tick_params(direction = 'inout')
		else: ax1.tick_params(labelbottom=False)
		if j==1: 
			ax1.set_ylabel(labels[i-1])		# Putting labels only at the edge of the triangle
			ax1.tick_params(direction = 'inout')
		else: ax1.tick_params(labelleft=False)
		
		#~ ax2 = plt.subplot(4,4,(i-1)*4+j)
				
		#~ ax2.plot(np.abs(unit1_peak_features[:,j-1]),np.abs(unit1_peak_features[:,i-1]),'.')
		#~ ax2.set_xscale('log')
		#~ ax2.set_yscale('log')
		#~ ax2.tick_params(right=True, top = True,direction = 'in')
		#~ if i==4: 
			#~ ax2.set_xlabel(labels[j-1])		# Putting labels only at the edge of the triangle
			#~ ax2.tick_params(direction = 'inout')
		#~ else: ax2.tick_params(labelbottom=False)
		#~ if j==1: 
			#~ ax2.set_ylabel(labels[i-1])		# Putting labels only at the edge of the triangle
			#~ ax2.tick_params(direction = 'inout')
		#~ else: ax2.tick_params(labelleft=False)

plt.savefig('Parameter_var_unit1.pdf')
#~ plt.savefig('Parameter_var_unit2.pdf')
plt.show()
