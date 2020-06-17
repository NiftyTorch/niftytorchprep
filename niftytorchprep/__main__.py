import click
import os
from subprocess import PIPE, run
import invoke

def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    print(result.stdout)
    print(result.stderr)
    return result.stdout, result.stderr

@click.group("Quality Control")
def qc():
    pass

@qc.command()
@click.argument('bids_dir', type=click.Path(exists=True))
@click.option('--out_dir', default=None, help="output directory")
def qc_anat(bids_dir, out_dir):
    """
    Runs Quality Control (T1) from visualqc package and stores the
    results in the *out_dir*.
    """
    command = f"visualqc_t1_mri -b {bids_dir}"
    if not out_dir is None:
        command += " -o {out_dir}"
    output, err = out(command)
    if "command not found" in err:
        print("You should install *visualqc* first")

@qc.command()
@click.argument('bids_dir', type=click.Path(exists=True))
@click.option('--out_dir', default=None, help="output directory")
def qc_func(bids_dir, out_dir):
    """
    Runs Quality Control (Functional) from visualqc package and stores the
    results in the *out_dir*
    """
    command = f"visualqc_func_mri -b {bids_dir}"
    if not out_dir is None:
        command += " -o {out_dir}"
    output, err = out(command)
    if "command not found" in err:
        print("You should install *visualqc* first")

@qc.command()
def qc_visualqc():
    """
    Installs visualqc from PIP.
    """
    invoke.run("pip install -U visualqc")


cli = click.CommandCollection(sources=[qc])

if __name__ == '__main__':
    cli()
