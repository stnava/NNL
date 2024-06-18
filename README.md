# antspymm processing for normative neuroimaging library
echo "Step 0: reorganize to NRG and run blind QC"
python3 src/all_viz.py
echo "Step 1: calculate outlierness scores and match good data together to the T1"
python3 src/outlierness.py
echo "Step 2: slurm antspymm"
cd /mnt/cluster/data/NNL/run_slurm_from_here 
# bash ../src/00_high_level_batch_call.sh  8 
# isqempty
cd ../
echo "Step 3: Agg"
python3 src/aggregate_new.py processedCSV
# echo "Step 4: Merge (FIXME)"

