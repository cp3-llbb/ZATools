#!/bin/bash

# Slurm configuration
#SBATCH --workdir /home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ToysGenerationForLLE/
#SBATCH --job-name cp3-llbb
#SBATCH --output ElEl/logs/slurm_%a.out
#SBATCH --error ElEl/logs/slurm_%a.err
#SBATCH --mem-per-cpu 3000

#SBATCH --array 0-5

srun python smoother.py -i "histos_${SLURM_ARRAY_TASK_ID}.root" -cat "ElEl"
