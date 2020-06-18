import os
from collections import Counter

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

if __name__ == "__main__":
    check_bids_files('../SmallData')
    list_bids_files('../SmallData')