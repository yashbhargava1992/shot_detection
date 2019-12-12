# This code will run the codes for the shots in a sequence intended. 
# Future versions could incorporate the passing of the arguments to the codes to generate output for a specific config

data_dir="../lc_data"
unit1_filename="laxpc_lc_0p05_unit1_3.0_80.0keV.lc"
unit2_filename="laxpc_lc_0p05_unit2_3.0_80.0keV.lc"
det_out="0p05_unit1_3.0_80.0keV"
fit_out="0p05_3.0_80.0keV"
sel_out="0p05_3.0_80.0keV"
spl_out="0p05_3.0_80.0keV"
append_text="all_peaks_v2"
res_out="${append_text}_0p05_3.0_80.0keV" 

det_comm="python shot_detector.py -d ${data_dir} -i1 ${unit1_filename} -a ${append_text} -o ${det_out} --shot_sep 0.05 --search_length 10 --significance 3"
fit_comm="python shot_fitting.py  -d ${data_dir} -i1 ${unit1_filename} -a ${append_text} -i2 ${unit2_filename} -o ${fit_out} -p ${det_out} --peak_length 4 --base_length 20"
sel_comm="python shot_selector.py -d ${data_dir} -i1 ${unit1_filename} -a ${append_text} -i2 ${unit2_filename} -f ${fit_out} -p ${det_out}  -o ${sel_out} --boundary_dist 0.1 --par_ratio 0.3"
spl_comm="python shot_splitter.py -d ${data_dir} -i1 ${unit1_filename} -a ${append_text} -f ${sel_out} -p ${det_out}  -o ${spl_out} --number_seg 9 --peak_duration 4"

echo "Running Detection algorithm"
echo ${det_comm}
${det_comm}

echo "Running Fitting algorithm"
echo ${fit_comm}
${fit_comm}

echo "Running Selection algorithm"
echo ${sel_comm}
${sel_comm}

#~ python shot_ratio.py

echo "Running Splitting code"
echo ${spl_comm}
${spl_comm}

#~ python plotting_routines.py

cp scripted_shot_algorithm.sh ${append_text}_scripted_shot_algorithm.sh
mkdir -p ${res_out}
mv ${append_text}*txt ${res_out}
mv ${append_text}*sh ${res_out}
