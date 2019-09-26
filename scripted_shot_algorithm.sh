# This code will run the codes for the shots in a sequence intended. 
# Future versions could incorporate the passing of the arguments to the codes to generate output for a specific config

python shot_detector.py -d "../lc_data" -i1 "laxpc_lc_0p05_unit1_3.0_80.0keV.lc" -o "0p05_unit1_3.0_80.0keV" -s 0 -t 1 -f 3
python shot_fitting.py  -d "../lc_data" -i1 "laxpc_lc_0p05_unit1_3.0_80.0keV.lc" -i2 "laxpc_lc_0p05_unit1_3.0_80.0keV.lc" -o "0p05_3.0_80.0keV" -p "0p05_unit1_3.0_80.0keV" --peak_length 1 --base_length 5
python shot_selector.py -d "../lc_data" -i1 "laxpc_lc_0p05_unit1_3.0_80.0keV.lc" -i2 "laxpc_lc_0p05_unit1_3.0_80.0keV.lc" -f "0p05_3.0_80.0keV" -p "0p05_unit1_3.0_80.0keV"  -o "0p05_3.0_80.0keV" --boundary_dist 0.1 --par_ratio 0.3
#python shot_ratio.py
python shot_splitter.py -d "../lc_data" -i1 "laxpc_lc_0p05_unit1_3.0_80.0keV.lc" -f "0p05_3.0_80.0keV" -p "0p05_unit1_3.0_80.0keV"  -o "0p05_3.0_80.0keV" --number_seg 4
#python plotting_routines.py
	
