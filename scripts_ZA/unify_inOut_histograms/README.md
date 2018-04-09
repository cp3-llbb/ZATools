### README of unify_inOut_histograms directory ###

This directory contains the scripts to put the different histograms In/Out in a single histogram called rhoSteps_histo_cat_hZA_lljj_deepCSV_btagM_mll_and_met_cut_ellIndex where cat = ['MuMu', 'ElEl'] and ellIndex = [0, ... , 20].

List of scripts and how to use them:

1) rename_for_slurm.py: first script to run. this script just renames the input files (the ones coming from factories_ZA) by appending a string "input_i" where i is an index numerating the files. I.e., if the files (backgrounds, data, and signal) are 84, i = [0, ..., 83]. Run it with the option "-p" which is the path to the files. This script is needed because the parallel submission of jobs to the cluster requires an index in the input files. WARNING: the script renames the file. Just to make sure you keep your files safe, you may want to create a backup copy, that you can delete when you see that everything ran fine.

2) unify_inOut_histograms.py. It takes as options the path (-p) where the output file from factories_ZA is and the name of the file (-i). The script reads the input file, creates another output file with the same name in ??? and simply appends to it the histograms if they don't have anything to do with the ellipses, otherwise it creates the rhoSteps_histo and stores it as well. This is run in step 3).

3) submit_parallel.sh. This submits one job per file to the cluster. You just have to modify the path and then run it with "batch submit_parallel.sh". WARNING: change the number of jobs in the array option depending on the number of files you are running on.

