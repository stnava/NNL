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
imageType=ADNI
subscriptName=/mnt/cluster/data/ADNI/src/01_job_id_subscript.sh
# for testing
# sbatch  --cpus-per-task $cpusPerTask  -o ~/slurmout/${imageType}_8.%a.out    --array=0-2 $subscriptName   8000 $1
# exit
nsleep=240
for x in 1 2 ; do
# rm ~/slurmout/*
# scancel -u ubuntu
sbatch  --cpus-per-task $cpusPerTask  -o ~/slurmout/${imageType}_8.%a.out    --array=0-999 $subscriptName   8000 $1
 sleep $nsleep
sbatch  --cpus-per-task $cpusPerTask  -o ~/slurmout/${imageType}_9.%a.out    --array=0-999 $subscriptName   9000 $1
sleep $nsleep
sbatch  --cpus-per-task $cpusPerTask  -o ~/slurmout/${imageType}_10.%a.out    --array=0-999 $subscriptName   10000 $1
sleep $nsleep
sbatch  --cpus-per-task $cpusPerTask  -o ~/slurmout/${imageType}_11.%a.out    --array=0-999 $subscriptName   11000 $1
sleep $nsleep
sbatch  --cpus-per-task $cpusPerTask  -o ~/slurmout/${imageType}_0.%a.out    --array=0-999  $subscriptName 0 $1
sleep $nsleep
sbatch  --cpus-per-task $cpusPerTask  -o ~/slurmout/${imageType}_1.%a.out    --array=0-999  $subscriptName 1000 $1
sleep $nsleep
sbatch  --cpus-per-task $cpusPerTask  -o ~/slurmout/${imageType}_2.%a.out    --array=0-999 $subscriptName  2000 $1
sleep $nsleep
sbatch  --cpus-per-task $cpusPerTask  -o ~/slurmout/${imageType}_3.%a.out    --array=0-999 $subscriptName   3000 $1
sleep $nsleep
sbatch  --cpus-per-task $cpusPerTask  -o ~/slurmout/${imageType}_4.%a.out    --array=0-999 $subscriptName   4000 $1
sleep $nsleep
sbatch  --cpus-per-task $cpusPerTask  -o ~/slurmout/${imageType}_5.%a.out    --array=0-999 $subscriptName   5000 $1
sleep $nsleep
sbatch  --cpus-per-task $cpusPerTask  -o ~/slurmout/${imageType}_6.%a.out    --array=0-999 $subscriptName   6000 $1
sleep $nsleep
sbatch  --cpus-per-task $cpusPerTask  -o ~/slurmout/${imageType}_7.%a.out    --array=0-999 $subscriptName   7000 $1
sleep $nsleep
done

