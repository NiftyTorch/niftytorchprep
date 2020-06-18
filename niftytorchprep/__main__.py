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

@click.group("Data preparation")
def data():
    pass

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
    if out.failed == True and "command not found" in out.sterr:
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
    if out.failed == True and "command not found" in out.sterr:
        print("You should install *visualqc* first")

@qc.command()
def qc_getvisualqc():
    """
    Installs visualqc from PIP.
    """
    run("pip install -U visualqc")


cli = click.CommandCollection(sources=[qc, bids])

if __name__ == '__main__':
    cli()
