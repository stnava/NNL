#!/bin/bash
echo off is $1
echo nthreads $2
x=/mnt/cluster/data/NNL/src/mm_nrg_csv_sr_first_ppmi_norm.py
python3  $x $SLURM_ARRAY_TASK_ID $2 $1

