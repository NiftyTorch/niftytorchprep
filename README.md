# ohbm-hackthon2020
BIDS to NiftyTorch: data preparation for deep learning

This repository is dedicated to NiftyTorch OHBM BrainHack [project](https://github.com/ohbm/hackathon2020/issues/85).

The chat room: https://mattermost.brainhack.org/brainhack/channels/hbmhack-niftytorch

The project pitch is included in the repo. 

For BIDS: https://bids.neuroimaging.io
For NiftyTorch getting started: https://niftytorch.github.io/doc/#installation


## How it works?

It installs `niftytorchprep` CLI tool that helps you prepare your data for *niftytorch* training.

### Install
```
python setup.py install
```

### Interfacte
```
$ niftytorchprep --help  
Usage: niftytorchprep [OPTIONS] COMMAND [ARGS]...

  NIFTYTORCHPREP helps to get your data ready for *niftytorch* training. You
  can browse through your options below. Each one has respective help
  function.

Options:
  --help  Show this message and exit.

Commands:
  bids-files       Print types of files and their number per folder.
  bids-totraining  Takes data from BIDS_DIR and organises it in a training...
  bids-validate    Basic BIDS verification.
  qc-anat          Runs Quality Control (T1) from visualqc package and...
  qc-func          Runs Quality Control (Functional) from visualqc package...
  qc-getvisualqc   Installs visualqc from PIP.
```

See it in action:

![nitrytorchprep demo](extras/niftytorch.gif "nitrytorchprep demo")

## Contributors
Dominik Krzemiński
Cardiff University Brain Research Imaging Centre

Sara Morsy 
Faculty of Medicine, Tanta University, Egypt

Kaori Lily Ito
Neural Plasticity & Neurorehabilitaiton Laboratory, University of Southern California
