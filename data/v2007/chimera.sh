#!/bin/bash --login

#SBATCH --time=0:15:00
#SBATCH --nodes=1
## SBATCH --ntasks=1
#SBATCH -c 1
## SBATCH --cpus-per-task=1
#SBATCH --mem=16g
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jones657@msu.edu
#SBATCH --job-name=chimera_v2007
#SBATCH --output=/mnt/home/jones657/Documents/sheafbind/data/sbatch_logs/%x-%A-%a.out
                 
#SBATCH --array=0-99


source /mnt/home/jones657/Documents/sheafbind/.venv/bin/activate
cd /mnt/home/jones657/Documents/sheafbind/data/v2007/
python3 chimera.py 100 $SLURM_ARRAY_TASK_ID
