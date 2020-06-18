import os
import glob
import sys
import shutil
import numpy as np
from collections import Counter
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split

import pandas as pd

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_bids_files(startpath, width = 55):
    """
    Check BIDS correctness with *BIDSValidator*
    Input:
        *startpath* - str
          path to BIDS catalogue
        *width* - int
          distance from the file name to status report
    Output:
        None
    """
    from bids_validator import BIDSValidator

    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 2 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 2 * (level + 1)
        for f in files:
            if f.startswith('.'): continue
            bids_flag = BIDSValidator().is_bids(os.path.join(root.replace(startpath, ''), f))
            status = f"{bcolors.OKGREEN}ok{bcolors.ENDC}" if bids_flag else f"{bcolors.FAIL}no{bcolors.ENDC}"
            txt = '{}{}'.format(subindent, f)
            distance = ' ' * (width - len(txt)) if (width - len(txt)) > 0 else '  '
            print('{} {}{}'.format(txt, distance, status))

def list_bids_files(startpath, width = 20):
    """
    List BIDS files with summary of extensions in each folder.
    Input:
        *startpath* - str
          path to BIDS catalogue
        *width* - int
          distance from the file name to the number of files
    Output:
        None
    """
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 2 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 2 * (level + 1)
        extensions = ['.'.join(f.split('.')[1:]) for f in files if not f.startswith('.')]
        for k, v in Counter(extensions).items():
            if k == '':
                k = 'PLAIN'
            else:
                k = '*.{}'.format(k)
            txt = '{}{}'.format(subindent, k)
            distance = ' ' * (width - len(txt)) if (width - len(txt)) > 0 else '  '
            print('{} {}{}'.format(txt, distance, f"{bcolors.BOLD}{v}{bcolors.ENDC}"))




def copy_image_files(dir_with_modality_dirs, subj_output_dir, subjid):
    '''
    Provide (1) path to the parent directory of the modality directories
    (either the subject or session level), and (2) the subject output directory
    '''
    workingdir = dir_with_modality_dirs
    modalpaths = os.path.join(workingdir, '*')
    modalities = sorted(glob.glob(modalpaths))

    for modality in modalities:
        print(modality)
        imgfilepaths = os.path.join(modality, '*.nii*')
        imgfiles = sorted(glob.glob(imgfilepaths))
        if not imgfiles:
            raise IOError("could not find nifti files for", subjid)
        for img in imgfiles:
            try:
                shutil.copy(img, subj_output_dir)
            except OSError:
                raise IOError("unable to copy nifti files")
            else:
                print("copied files successfully")

def move_to_destination(output_dir, subj, destination):
    'Helper function that moves subject data (*subj*) to *output_dir* / *destination*'
    subj_orig_path = os.path.join(output_dir, subj)
    try:
        dest = shutil.move(subj_orig_path, destination)
    except OSError:
        print("destination may already exist")

def create_training_data(bids_dir, output_dir, variable_to_classify, test_set_size  = 0.1,
                         val_set_size = 0.2):
    """
    Creates training data for NIFTYTORCH from *bids_dir*.
    Input:
        *bids_dir* - str
          path to BIDS catalogue
        *output_dir* - str
          output data path
        *variable_to_classify* - str
          target variable
        *test_set_size* - float
          proportion of subject to go into test set
        *val_set_size* - float
          proportion of subject to go into validation set
    Output:
        None
    """
    filepaths = os.path.join(bids_dir, 'sub-*')
    subj_dirs = sorted(glob.glob(filepaths))
    # get list of subjects
    subjList = []
    for subj in subj_dirs:
        subjID = os.path.basename(subj)
        subjList.append(subjID)

    participantsTsvPath   = os.path.join(bids_dir, 'participants.tsv')
    participantsTsvExists = os.path.exists(participantsTsvPath)
    participant_metadata  = pd.read_csv(participantsTsvPath, sep='\t')
    participant_metadata  = participant_metadata.sort_values('participant_id')
    if not participantsTsvExists:
        raise IOError("participants.tsv file missing. Do not continue without this file")
    else:
        print("participants.tsv file found")
    subsetDf = participant_metadata[participant_metadata["participant_id"].isin(subjList)]
    if len(subsetDf) == 0:
        raise ValueError("Check that your participants are listed in the participants.tsv file")
    # check if the variable_to_classify is in the participants.tsv file
    if not variable_to_classify in list(participant_metadata.columns):
        raise IOError("Please make sure your variable is a column in your participants.tsv file")

    num_classes=len(np.unique(participant_metadata[variable_to_classify].to_numpy()))
    if not (len(subjList)*test_set_size)>=num_classes:
        raise IOError("Please increase the proportion of the test set size so there will be at least one sample per class.")
    if not (len(subjList)*val_set_size)>=num_classes:
        raise IOError("Please increase the proportion of the validation set size so there will be at least one sample per class.")

    # Make new folders for each subject
    try:
        os.mkdir(output_dir)
    except OSError:
        print("Creation of the directory %s failed" % output_dir)
    else:
        print("Successfully created the directory %s " % output_dir)
    for subj in subj_dirs:
        subjname = os.path.basename(subj)
        print(subjname)
        newdirpath = os.path.join(output_dir,subjname)
        try:
            if not os.path.exists(newdirpath):
                os.mkdir(newdirpath)
        except OSError:
            print ("Creation of the directory %s failed" % newdirpath)
        else:
            print ("Successfully created the directory %s " % newdirpath)

    # Copy nifti files from bids dir to output directory
    for subj in subj_dirs:
        sespath = os.path.join(subj,'ses-*')
        ses_dirs = sorted(glob.glob(sespath))
        subjID = os.path.basename(subj)
        subjOutputDir = os.path.join(output_dir, subjID)
        # some BIDS directories may have session folders.
        if ses_dirs:
            for session in ses_dirs:
                print(session)
                workingdir = session
                copy_image_files(workingdir,subjOutputDir, subjID)
        if not ses_dirs:
            print("ses_dirs do not exist")
            workingdir = subj
            copy_image_files(workingdir, subjOutputDir, subjID)

    subjListKey = {v: k for k, v in enumerate(subjList)}
    y = subsetDf[variable_to_classify].to_numpy()
    num_samples = len(y)
    X = np.zeros(num_samples)
    sss = StratifiedShuffleSplit(n_splits = 2, test_size = test_set_size)
    indices1, indices2 = sss.split(X, y)
    test_indices=indices1[1]

    if not (pd.Series(subjList).isin(subsetDf["participant_id"]).all()):
        raise IOError("There are participants missing in your participants.tsv file")
    if subsetDf[variable_to_classify].isnull().values.any():
        raise IOError("ERROR: You have missing values in your selected variable for classification.")

    # remove test set from rest of data for re-splitting and save subj ids
    test_subj = []
    for subj in subjListKey:
        if subjListKey[subj] in test_indices:
            indexNames = subsetDf[subsetDf['participant_id'] == subj].index
            subsetDf = subsetDf.drop(indexNames)
            test_subj.append(subj)
            try:
                subjList.remove(subj)
            except:
                print('subject not in list anymore')

    subjListKey = {v: k for k, v in enumerate(subjList)}

    # recalculate val_set_size percentage based on remaining participants
    new_val_setsize = (val_set_size*num_samples)/((val_set_size*num_samples) +\
                                       ((1-(val_set_size+test_set_size)) * num_samples))
    new_val_setsize = round(new_val_setsize, 2)
    y = subsetDf[variable_to_classify].to_numpy()
    num_samples = len(y)
    X = np.zeros(num_samples)

    sss = StratifiedShuffleSplit(n_splits = 2, test_size = new_val_setsize)
    print('validation set size:', new_val_setsize)

    indices1,indices2 = sss.split(X, y)
    train_indices = indices1[0]
    validation_indices = indices1[1]

    train_dir = os.path.join(output_dir, 'train')
    val_dir = os.path.join(output_dir, 'val')
    test_dir = os.path.join(output_dir, 'test')

    for newdir in (train_dir, val_dir, test_dir):
        try:
            if not os.path.exists(newdir):
                os.mkdir(newdir)
        except OSError:
            raise ValueError("Creation of the directory %s failed" % newdir)
        else:
            print("Successfully created the directory %s " % newdir)

    for subj in test_subj:
        print(subj, "is in test set")
        move_to_destination(output_dir, subj, test_dir)

    for subj in subjListKey:
        if subjListKey[subj] in train_indices:
            print(subj, "is in training set")
            move_to_destination(output_dir, subj, train_dir)
        elif subjListKey[subj] in validation_indices:
            print(subj, "is in validation set")
            move_to_destination(output_dir, subj, val_dir)

if __name__ == "__main__":
    heck_bids_files('../SmallData')
    list_bids_files('../SmallData')
    create_training_data('testcopybids', 'outtest', 'sex')
