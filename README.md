# shot_detection

Using a binned light curve the goal is to detect shots in the light curve. 
The shots are defined as fast rising and falling flares are observed to happen in a time scales of few seconds. 
The count rates seem to jump by a factor of 1.5-2 in the interval. 

The shots which are physical (i.e. from the source) will be visible in all the instruments and in all energy ranges. 
Thus it is quite easy to discern from the fake (i.e. those arising from poissonian fluctuations). 

Given the bright nature of the source (Cyg X-1 in this case) we can find shots in soft energy in a single LAXPC unit 
and fit the the found shots in other energy bands and units.  

Another important aspect which turned up during the discussion is that to reduce the effect of the background variations 
we can work with only the top LAXPC layer for softer energies and all the layers for higher energies (>20 keV)
This doesn't change the detection algorithm at all. 

v0.1 
This is part of branch 'testing'. The code detects the shots with a certain level above the mean count rate (indicated by f), 
where the mean is computed over a time interval of 'T' and the shots are separated by 'shot_sep' (in units of T). 
The code also returns other peaks which are within 1-sig of the detected peak. 

Currently only the index of the shots and other peaks is returned. The shot can be plotted and seen by running the code. 

Since the data is inherently segmented (due to orbits of Astrosat), we use this to do piecewise detection of the shot. 


Future plan:
1) Reproduce the energy dependence of the shot:
-- To do this, the shots need to be averaged over detections in different energy bands. Then the ratio of the shot in different energies need to be plotted. 

2) Characterisation of the shot:
-- To do this, we need to fit each shot with a predecided profile and plot the distribution of these parameters (Histograms and pairwise)

v0.2
The modules of detecting, fitting, selecting and segmenting are written. Also code for computing the ratio

Detection	: Same as version 1
Fitting		: Fits each shot with an exponential rise and decay over an average count rate. 
			The average count rate is determined by mean counts in region around the peak. If a peak cannot be fitted, bound values are returned
Selecting	: The peaks which are present in both LAXPC units and are not ultra wide/flat are ignored. 
Segmenting	: The selected shots can be segmented for shot-phase resolved analysis
Ratio		: To plot the energy dependence of the shots. 


v0.3 in progress
A bash script is added to run all the codes one after another. 
The codes were altered to accept the parameters from the argument passed while invoking the code
The script has variables to ease the further runs

New update could be to include parsing the arguments to the bash script itself.
