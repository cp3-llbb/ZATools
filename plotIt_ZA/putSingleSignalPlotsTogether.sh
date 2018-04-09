#!/bin/bash

mkdir finalPlots_rhoSteps_singleSignals
for i in `seq 0 20`; do
    cp ./*_plots_signal_${i}/rho_steps_histo_ElEl_hZA_lljj_deepCSV_btagM_mll_and_met_cut_${i}.pdf finalPlots_rhoSteps_singleSignals 
    cp ./*_plots_signal_${i}/rho_steps_histo_ElEl_hZA_lljj_deepCSV_btagM_mll_and_met_cut_${i}.png finalPlots_rhoSteps_singleSignals 
    cp ./*_plots_signal_${i}/rho_steps_histo_ElEl_hZA_lljj_deepCSV_btagM_mll_and_met_cut_${i}_logy.pdf finalPlots_rhoSteps_singleSignals 
    cp ./*_plots_signal_${i}/rho_steps_histo_ElEl_hZA_lljj_deepCSV_btagM_mll_and_met_cut_${i}_logy.png finalPlots_rhoSteps_singleSignals 
    cp ./*_plots_signal_${i}/rho_steps_histo_MuMu_hZA_lljj_deepCSV_btagM_mll_and_met_cut_${i}.pdf finalPlots_rhoSteps_singleSignals 
    cp ./*_plots_signal_${i}/rho_steps_histo_MuMu_hZA_lljj_deepCSV_btagM_mll_and_met_cut_${i}.png finalPlots_rhoSteps_singleSignals 
    cp ./*_plots_signal_${i}/rho_steps_histo_MuMu_hZA_lljj_deepCSV_btagM_mll_and_met_cut_${i}_logy.pdf finalPlots_rhoSteps_singleSignals 
    cp ./*_plots_signal_${i}/rho_steps_histo_MuMu_hZA_lljj_deepCSV_btagM_mll_and_met_cut_${i}_logy.png finalPlots_rhoSteps_singleSignals 
done
