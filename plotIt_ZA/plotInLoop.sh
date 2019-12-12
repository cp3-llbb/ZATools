#!/bin/bash

arr=(0 10 16)

#for i in `seq 0 20`; do
for i in "${arr[@]}"; do
    echo $i
    #python listHistos.py -d ../factories_ZA/plot_InOut_differentRhoSteps_systematic_updated_bugFixed/ -ell=$i --llbb
    python listHistos.py -d ../factories_ZA/newProd_42Syst_splitJEC_splitPDF_part0_copyTTbarUnc/slurm/output/ -ell=$i --llbb --unblinded
    ./plotIt.sh plots_signal_FORTHESIS_MuEl$i 
done
