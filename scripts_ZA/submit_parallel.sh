#!/bin/bash -l

#SBATCH --job-name=arrayJob
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

#dir="/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/plot_InOut_differentRhoSteps_systematics/slurm/output/"
# Do some work based on the SLURM_ARRAY_TASK_ID
# For example:
srun python unify_inOut_histograms.py -i /nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/plot_InOut_differentRhoSteps_systematics_backupCopy2/slurm/output/input_${SLURM_ARRAY_TASK_ID}.root -p /nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/plot_InOut_differentRhoSteps_systematics_backupCopy2/slurm/output
# 
# where my_process is you executable

