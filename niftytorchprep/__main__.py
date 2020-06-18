import click
import os
import glob
import re
from invoke import run

from .tools import *

@click.group("BIDS control")
def bids():
    pass

@bids.command()
@click.argument('bids_dir', type = click.Path(exists = True))
def bids_validate(bids_dir):
    """
    Basic BIDS verification. Print 'ok' for correct BIDS files or 'no' otherwise.
    """
    check_bids_files(bids_dir)

@bids.command()
@click.argument('bids_dir', type = click.Path(exists = True))
def bids_files(bids_dir):
    """
    Print types of files and their number per folder.
    """
    list_bids_files(bids_dir)

@click.group("Quality Control")
def qc():
    pass

@qc.command()
@click.argument('bids_dir', type = click.Path(exists = True))
@click.option('--out_dir', default=None, help="output directory")
def qc_anat(bids_dir, out_dir):
    """
    Runs Quality Control (T1) from visualqc package and stores the
    results in the *out_dir*.
    """
    command = f"visualqc_t1_mri -b {bids_dir}"
    if not out_dir is None:
        command += " -o {out_dir}"
    out = run(command, echo = True, warn = True)
    if out.failed == True and "command not found" in out.stderr:
        print("You should install *visualqc* first")

@qc.command()
@click.argument('bids_dir', type = click.Path(exists = True))
@click.option('--out_dir', default=None, help="output directory")
def qc_func(bids_dir, out_dir):
    """
    Runs Quality Control (Functional) from visualqc package and stores the
    results in the *out_dir*
    """
    command = f"visualqc_func_mri -b {bids_dir}"
    if not out_dir is None:
        command += " -o {out_dir}"
    out = run(command, echo = True, warn = True)
    if out.failed == True and "command not found" in out.stderr:
        print("You should install *visualqc* first")

@qc.command()
def qc_getvisualqc():
    """
    Installs visualqc from PIP.
    """
    run("pip install -U visualqc")

@click.group("Data preparation")
def data():
    pass

@data.command()
@click.argument('bids_dir', type = click.Path(exists = True))
@click.argument('out_dir', type = click.Path())
@click.argument('var_to_classify', type = str)
@click.option('--test', default=0.1, type=float, help="proportion of test set (from 0 to 1)")
@click.option('--val', default=0.2, type=float, help="proportion of validation set (from 0 to 1)")
def bids_totraining(bids_dir, out_dir, var_to_classify, test, val):
    """
    Takes data from BIDS_DIR and organises it in a training ready format
    in OUT_DIR.
    """
    create_training_data(bids_dir, out_dir, var_to_classify,
                         test_set_size  = test, val_set_size = val)


help_content = """
NIFTYTORCHPREP helps to get your data ready
for *niftytorch* training. You can browse through your
options below. Each one has respective help function.
"""
cli = click.CommandCollection(sources = [qc, bids, data],
                              help = help_content)

if __name__ == '__main__':
    cli()
