#!/bin/bash -l

#SBATCH --job-name=unifyHistos
#SBATCH --array=0-83
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=3000
#SBATCH -p debug -n 1

######################
# Begin work section #
######################

# Print this sub-job's task ID
echo "My SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID
mkdir /nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/finalHistos_toRunLimits/
mkdir /nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/finalHistos_toRunLimits/slurm
mkdir /nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/finalHistos_toRunLimits/slurm/output

for filename in "/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/plot_InOut_differentRhoSteps_systematics_backupCopy3/slurm/output/*input_${SLURM_ARRAY_TASK_ID}.root"; do
    srun python unify_inOut_histograms.py -i $filename -p /nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/plot_InOut_differentRhoSteps_systematics_backupCopy3/slurm/output
done

#mv *out /nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/finalHistos_toRunLimits/slurm/output 
#mv *root /nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/finalHistos_toRunLimits/slurm/output 
