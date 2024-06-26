##################################################################
# NRG = https://github.com/stnava/biomedicalDataOrganization
##################################################################
import os
import sys
from os.path import exists
nthreads = str(48)
index=334 # 1509 # 1080  #  16 # 779 # 375 # 886
if len( sys.argv ) > 1 :
    index=int( sys.argv[1] )+int( sys.argv[3] )
    nthreads=str(sys.argv[2])
os.environ["TF_NUM_INTEROP_THREADS"] = nthreads
os.environ["TF_NUM_INTRAOP_THREADS"] = nthreads
os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = nthreads
os.environ["OPENBLAS_NUM_THREADS"] = nthreads
os.environ["MKL_NUM_THREADS"] = nthreads
print(" threads " + str(nthreads))
import ants
import antspymm
import antspyt1w
import antspynet
import siq
import sys
import glob as glob
import os
import pandas as pd
import re as re
mydir = os.path.expanduser( "/mnt/cluster/data/NNL/NRG/NNL/")
print("index: " + str(index) + " threads " + nthreads )
studyfn="/mnt/cluster/data/NNL/matched_mm_data5.csv"
df=pd.read_csv( studyfn )
if index > (df.shape[0]-1):
    print("index " + str(index) + " too big")
    sys.exit(0)

tlrfn = antspyt1w.get_data('T_template0_LR', target_extension='.nii.gz' )
tfn = antspyt1w.get_data('T_template0', target_extension='.nii.gz' )
templatea = ants.image_read( tfn )
templatea = ( templatea * antspynet.brain_extraction( templatea, 't1' ) ).iMath( "Normalize" )
templatealr = ants.image_read( tlrfn )


import subprocess
cmd_str = " sudo find /tmp  -cmin +330 -delete "
subprocess.run(cmd_str, shell=True)

csvfns = df['filename']
csvrow = df[ df['filename'] == csvfns[index] ] 
# csvrow.rename(columns={csvrow.columns[0]: 'filename'}, inplace=True)
print( csvrow )
print( csvrow.keys() )
print( csvrow['subjectID'] )
srOption = False
testfn = os.path.expanduser( "~/.antspymm/siq_default_sisr_2x2x2_1chan_featvggL6_best_mdl.h5" )
testfn = os.path.expanduser( "~/.antspymm/siq_smallshort_train_2x2x2_2chan_featgraderL6_postseg_best_mdl.h5")
if not exists( testfn ):
    print("downloading sr models - takes a few GB of space")
    antspymm.get_data()
else:
    print("SR models are here ... " + testfn )
rootdir='/mnt/cluster/data/NNL/'
mfn='/home/ubuntu/.antspymm/siq_smallshort_train_2x2x2_2chan_featgraderL6_postseg_best_mdl.h5'
mdl, mdlshape = siq.read_srmodel(mfn)
csvrow=csvrow.dropna(axis=1)
sid=str(csvrow['subjectID'].iloc[0] )
dt=str(csvrow['date'].iloc[0])
iid='000' # str(csvrow['imageID'].iloc[0])
nrgt1fn=os.path.join( rootdir, "NRG/NNL", sid, dt, 'T1w', iid, str(csvrow['filename'].iloc[0]+'.nii.gz') )
dosr=False
if not exists( nrgt1fn ):
    print("T1 " + nrgt1fn + " is gatored")
    print("sr first done")
    sys.exit(0)
else:    
    imgo = antspymm.mm_read( nrgt1fn, modality='T1w' ).iMath("Normalize")
    imgo_spacing = ants.get_spacing( imgo )
    local_grade = 3.0 # antspyt1w.resnet_grader( imgo * antspynet.brain_extraction( imgo, 't1' ) )['gradeNum'][0]
    imgo_spacing = ants.get_spacing( imgo )
    if imgo_spacing[2] < 0.80:
        srout = nrgt1fn # dont use the SR - too taxing on compute at this point given how few subjects it is 
    if local_grade <= 0.20:
        print( nrgt1fn + " failing grade " + str( local_grade ) )
        sys.exit(0)
    print("T1 " + os.path.basename(nrgt1fn) + " is bigtime")
    srout = re.sub( "nrgdata", "nrgdatasr", nrgt1fn )
    print( srout )
    if not exists( srout ) and dosr:
        bxt  = antspyt1w.brain_extraction( imgo )
        imgb = imgo*bxt
        mylr = antspyt1w.label_hemispheres( imgb, templatea, templatealr )
        print("start SR")
        mysr = siq.inference( imgo, mdl, segmentation=mylr*bxt, truncation=[0.001,0.999], poly_order=1, verbose=True )
        os.makedirs( os.path.dirname( srout ), exist_ok=True )
        ants.image_write( ants.iMath( mysr['super_resolution'], "Normalize"),  srout )

csvrow['projectID']='NNL'
############################################################################################
mods=['T1w' ] #  , 'DTI', 'T2Flair', 'rsfMRI' ]
template = ants.image_read("~/.antspymm/PPMI_template0.nii.gz").reorient_image2("LPI")
bxt = ants.image_read("~/.antspymm/PPMI_template0_brainmask.nii.gz").reorient_image2("LPI")
template = template * bxt
template = ants.crop_image( template, ants.iMath( bxt, "MD", 12 ) )
srolder=False
door=True
if True: 
    if dosr:
        outdir = rootdir + "processedCSVSRFIRST/"
        studycsv2 = antspymm.study_dataframe_from_matched_dataframe(
            csvrow,
            rootdir + "NRG/",
            outdir, verbose=True)
        studycsv2.iat[0, studycsv2.columns.get_loc('filename')] = srout

        mmrun = antspymm.mm_csv( studycsv2,
                        dti_motion_correct='SyN',
                        dti_denoise=True,
                        srmodel_NM = "siq_smallshort_train_bestup_1chan_featgraderL6_best_mdl.h5",
                        srmodel_DTI = "siq_smallshort_train_bestup_1chan_featgraderL6_best_mdl.h5",
                        normalization_template=template,
                        normalization_template_output='ppmi',
                        normalization_template_transform_type='antsRegistrationSyNQuickRepro[s]',
                        normalization_template_spacing=[1,1,1])
    if door:
        outdir = rootdir + "processedCSV/"
        studycsv2 = antspymm.study_dataframe_from_matched_dataframe(
            csvrow,
            rootdir + "NRG/",
            outdir,  verbose=True)
        qvfn = os.path.join( studycsv2['outputdir'].iloc[0], studycsv2['projectID'].iloc[0],
                studycsv2['subjectID'].iloc[0], studycsv2['date'].iloc[0] )
        qvfn1 = qvfn + '/' + studycsv2['projectID'].iloc[0] + "_" + studycsv2['subjectID'].iloc[0] + "_"+ studycsv2['date'].iloc[0] + "_pre.png"
        qvfn2 = qvfn + '/' + studycsv2['projectID'].iloc[0] + "_" + studycsv2['subjectID'].iloc[0] + "_"+ studycsv2['date'].iloc[0] + "_post.png"
        slf=0.6
        antspymm.quick_viz_mm_nrg( studycsv2['sourcedir'].iloc[0], 
                studycsv2['projectID'].iloc[0],
                studycsv2['subjectID'].iloc[0], 
                studycsv2['date'].iloc[0],
                slice_factor=slf,
                filename = qvfn1 )
        mmrun = antspymm.mm_csv( studycsv2,
                        dti_motion_correct='SyN',
                        dti_denoise=True,
                        normalization_template=template,
                        normalization_template_output='ppmi',
                        normalization_template_transform_type='antsRegistrationSyNQuickRepro[s]',
                        normalization_template_spacing=[1,1,1])

        antspymm.quick_viz_mm_nrg( studycsv2['outputdir'].iloc[0],
                studycsv2['projectID'].iloc[0],
                studycsv2['subjectID'].iloc[0],
                studycsv2['date'].iloc[0],
                post=True,
                slice_factor=slf,
                original_sourcedir=studycsv2['sourcedir'].iloc[0], filename = qvfn2 )

print("sr first done")

