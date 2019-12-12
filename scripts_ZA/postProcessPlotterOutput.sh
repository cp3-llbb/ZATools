#!/usr/bin/env bash

# Execute this after having run the plots

export PATH=/nfs/soft/parallel/bin/:$PATH

if [[ "$1" == "-h" || -z "$1" ]]; then
    echo "Usage: $0 (base directory name)"
    exit 0
fi

directories=(`ls . | grep $1"_"`)

echo "Found directories: ${directories[*]}"

for d in ${directories[*]}; do
    dir=$d/slurm/output
    
    if [[ ! -d "${dir}" ]]; then
        echo "${dir} should be a valid directory"
        exit 1
    fi

    pushd $dir

    # Merge all the plotter output files
    ../hadd_histos.sh -r

    dir_content=(`ls *.root`)

    # Signal reweighting: merge the different bases together
    #if [[ ${dir_content[*]} =~ GluGluToHH.*base.*.root ]]; then 
    #    echo "Merging reweighted signals..."
    #    mergeReweightBases.sh . -r
    #fi

    # Merge the small backgrounds together to speed up the next steps
    #if [[ ${dir_content[*]} =~ WWToLNuQQ ]]; then
    #    echo "Merging VV samples..."
    #    to_merge=`ls WW*.root ZZ*.root WZ*.root`
    #    hadd VVToAll_merged_histos.root ${to_merge} && rm ${to_merge}
    #fi
    #if [[ ${dir_content[*]} =~ GluGluHToWWTo2L2Nu_M125_13TeV_powheg ]]; then
    #    echo "Merging Higgs samples..."
    #    to_merge=`ls GluGluHTo*.root GluGluZH*.root HZJ_HToWW*.root ZH_HToBB*.root ggZH_HToBB*.root VBFHTo*.root WplusH*.root WminusH*.root HWplusJ*.root HWminusJ*.root bbHToBB*.root ttHTo*.root`
    #    hadd Higgs_M125_merged_histos.root ${to_merge} && rm ${to_merge}
    #fi
    
    dir_content=(`ls *.root`)

    file_content=`rootls ${dir_content[0]}`

    # flatten 2D plots
    #if [[ ${file_content} =~ mjj_vs_NN ]]; then
    #    echo "Flattening 2D histograms..."
    #    parallel -j 5 flattenTH2.py -p "flat_" -a "x" -r \'mjj_vs_NN.*\' -- ::: *.root
    #    parallel -j 5 flattenTH2.py -p "flatDrop_" -a "x" -r \'mjj_vs_NN.*\' -d 3 -- ::: *.root
    #else
    #    echo "No 2D histograms found!"
    #fi

    # take envelopes for scale systematics
    if [[ ${file_content} =~ scaleUncorr ]]; then
        echo "Creating scale systematics..."
        parallel -j 5 createScaleSystematics.py -s scaleUncorr -- ::: *.root
    else
        echo "No scale systematics found!"
    fi
    
    echo "Done."

    popd
done

mkdir -p $1/slurm/output
if [[ ${directories[*]} =~ $1_for_signal ]]; then echo "Moving signal files to main folder..."; mv $1_for_signal/slurm/output/*.root $1/slurm/output ; fi
if [[ ${directories[*]} =~ $1_for_data ]]; then echo "Moving data files to main folder..."; mv $1_for_data/slurm/output/*.root $1/slurm/output ; fi
if [[ ${directories[*]} =~ $1_for_MCbkgminusDY ]]; then echo "Moving MC bkg files to main folder..."; mv $1_for_MCbkgminusDY/slurm/output/*.root $1/slurm/output ; fi
if [[ ${directories[*]} =~ $1_for_DY ]]; then echo "Moving MC DY files to main folder..."; mv $1_for_DY/slurm/output/*.root $1/slurm/output ; fi

#if [[ ${directories[*]} =~ $1_for_signal ]]; echo "Removing empty signal folders..."; then rm -r $1_for_signal/ ; fi
#if [[ ${directories[*]} =~ $1_for_data ]]; echo "Removing empty data folders..."; then rm -r $1_for_data/ ; fi
#if [[ ${directories[*]} =~ $1_for_MCbkgminusDY ]]; echo "Removing empty MCbkgminusDY folders..."; then rm -r $1_for_MCbkgminusDY/ ; fi
#if [[ ${directories[*]} =~ $1_for_DY ]]; echo "Removing empty DY folders..."; then rm -r $1_for_DY/ ; fi
