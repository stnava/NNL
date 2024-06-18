#!/bin/bash

NUMPARAMS=$#

ntt=4
subscriptName=src/01_viz_call.sh
sbatch  --cpus-per-task $ntt  -o ~/slurmout/viz_0.%a.out    --array=0-999  $subscriptName 

