#!/bin/bash
echo off is $1
echo nthreads $2
x=/mnt/cluster/data/ADNI/src/mm_nrg_csv_sr_first_ppmi_norm.py
# x=/mnt/cluster/data/ADNI/src/mm_nrg_csv.py
# x=/mnt/cluster/data/ADNI/src/mm_nrg_csv_newt1.py
# x=/mnt/cluster/data/ADNI/src/arnaud_low_res.py
python3  $x $SLURM_ARRAY_TASK_ID $2 $1

