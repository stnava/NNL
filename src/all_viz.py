##################################################################
import shutil
from pathlib import Path

copy_file_with_dirs = lambda src, dst: (dst.parent.mkdir(parents=True, exist_ok=True), shutil.copy(src, dst))[1]
link_file_with_dirs = lambda src, dst: (dst.parent.mkdir(parents=True, exist_ok=True), os.symlink(src, dst))[1]
# os.symlink(file, destination_file)lambda src, dst: (dst.parent.mkdir(parents=True, exist_ok=True), shutil.copy(src, dst))[1]

def map_modality(modality):
    modality_map = {
        't1': 'T1w',
        'flair': 'T2Flair',
        'dwi_ap': 'DTILR',
        'dwi_pa': 'DTIRL',
        'dtilr': 'DTILR',
        'dtirl': 'DTIRL',
        'perf': 'perf',
        'rsfmri': 'rsfMRI'
    }
    return modality_map.get(modality.lower(), None)

import os
import sys
from os.path import exists
from pathlib import Path
nthreads = str(2)
index=11
if len( sys.argv ) > 1 :
    index=int( sys.argv[1] )
    nthreads=sys.argv[2]
os.environ["TF_NUM_INTEROP_THREADS"] = nthreads
os.environ["TF_NUM_INTRAOP_THREADS"] = nthreads
os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = nthreads
os.environ["OPENBLAS_NUM_THREADS"] = nthreads
os.environ["MKL_NUM_THREADS"] = nthreads
import antspymm
import sys
import glob as glob
import os
import pandas as pd
import re as re
import random as random
from os.path import exists
mydir = os.path.expanduser( "/mnt/cluster/data/NNL/Nifti/" )
# print("index: " + str(index) + " threads " + nthreads )
# get all the subject t1 images
qcfn="images_to_qc_2024_June.csv"
mysep='_'
if not exists( qcfn ) :
    print("Collect all images" )
    mymods = ['t1','flair','dwi_ap', 'dwi_pa', 'perf', 'rsfmri' ]#   # antspymm.get_valid_modalities( )
    nwmods = ['T1w','T2Flair', 'DTILR', 'DTIRL', 'perf', 'rsfMRI' ]
    afns0=[]
    for m in mymods:
        afns0.append( glob.glob( mydir + "*/*/*"+m+"*nii.gz" ) )
    afns = []
    afns = [item for sublist in afns0 for item in sublist]
    afns.sort()
    print(len(afns))
    nrgfns=[]
    # reformat each image to NRG and copy it over 
    for x in afns:
        newx = os.path.basename(x)
        newx = re.sub( "dwi_ap.nii.gz", "DTILR", newx )
        newx = re.sub( "dwi_pa.nii.gz", "DTIRL", newx )
        xparts = re.split(r'_', newx )
        if len( xparts ) == 4:
            xparts = xparts[0:3] # remove extensions like heudiconv841
        xparts[0] = re.sub( 'sub-', '', xparts[0] ) # study
        for z in range(len(xparts)):
            xparts[z] = re.sub( '.nii.gz', '', xparts[z] )
        xparts.append( '000' ) # placeholder image id
        xparts =  ['NNL'] + xparts
        mm = 3
        xparts[mm] = map_modality( xparts[mm] )
        newx = "NRG/"+str(Path(*xparts)) + "/"+ mysep.join( xparts )+'.nii.gz'
        if antspymm.validate_nrg_file_format( newx, mysep )[0] and not exists( newx ) :
            print("copy "+ newx)
            link_file_with_dirs(Path(x), Path(newx))
            print("done")
        bvx=re.sub("nii.gz","bval",x)
        bvx2=re.sub("nii.gz","bvec",x)
        if exists( bvx ) and exists( bvx2 ):
            newbvx = "NRG/"+str(Path(*xparts)) + "/"+ mysep.join( xparts )+'.bval'
            newbvx2 = "NRG/"+str(Path(*xparts)) + "/"+ mysep.join( xparts )+'.bvec'
            link_file_with_dirs(Path(bvx), Path(newbvx))
            link_file_with_dirs(Path(bvx2), Path(newbvx2))

        if not antspymm.validate_nrg_file_format( newx, mysep )[0]:
            print("bad "+ newx)
            derka
        nrgfns.append( newx )
    df = pd.DataFrame(nrgfns, columns=['filename'])
    df.to_csv( qcfn )
    print( df. shape )
##########################
df = pd.read_csv( qcfn ) #
from pathlib import Path #
mypr=False
myresam=None # 2.0
odir='vizx_2024'
n=df.shape[0]
off=round( n / 200 )
indexLo=index*off
indexHi=(index+1)*off
print("Zindex " + str(index) + " low " + str(indexLo) + " high " + str( indexHi ) )
# for index2 in range( indexLo, indexHi ):
for index2 in range( 0, n+1 ):
    if index2 < df.shape[0]:
        ifn=df['filename'].iloc[index2]
        mystem=Path( ifn ).stem    
        mystem=Path( mystem ).stem    
        vizfn=odir+'/viz_'+mystem+'.png'
        csvfn=odir+'/viz_'+mystem+'.csv'
        if not exists( csvfn ):
            print(ifn, "index: " + str(index) + " threads " + nthreads + " " + vizfn)
            # try:
            antspymm.blind_image_assessment( ifn, vizfn, title=True,
                        resample=myresam, pull_rank=mypr, verbose=True )
            #    derka
            # except:
            #    pass

print( str(index) + " finnish")

