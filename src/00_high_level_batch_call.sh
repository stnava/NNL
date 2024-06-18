#!/bin/bash

NUMPARAMS=$#

if [ $NUMPARAMS -lt 1 ]
then
echo " USAGE ::  "
echo "  sh   $0 cpusPerTask  "
echo "subscriptName should point to src/generic/01_job_id_subscript.sh"
exit
fi
cpusPerTask=$1
imageType=NNL
subscriptName=/mnt/cluster/data/NNL/src/01_job_id_subscript.sh
sbatch  --cpus-per-task $cpusPerTask  -o ~/slurmout/${imageType}_0.%a.out    --array=0-366 $subscriptName 0 $1


