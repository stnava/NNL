#!/bin/bash
x=/mnt/cluster/data/NNL/src/all_viz.py
python3  $x $SLURM_ARRAY_TASK_ID 2

