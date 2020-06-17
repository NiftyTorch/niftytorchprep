import re
import os

def main():
    try:
        from invoke import task, Program, Collection
    except ModuleNotFoundError:
        print("You are probably running `niftytorchprep` for the first time")
        print("Press [enter] to install pyinvoke or Ctrl+C to abort\n")
        input()
        os.system("pip install invoke==1.4.1")
        raise

    @task
    def getvisualqc(c):
        """
        Installs visualqc.
        """
        c.run("pip install -U visualqc", echo = True)

    @task
    def qct1(c, bids_dir, out_dir = None):
        """
        Runs Quality Control (T1) from visualqc package and stores the
        results in the *out_dir*
        """
        command = f"visualqc_t1_mri -b {bids_dir}"
        if not out_dir is None:
            command += " -o {out_dir}"
        out = c.run(command, echo = True)

    @task
    def qcfunc(c, bids_dir, out_dir = None):
        """
        Runs Quality Control (Functional) from visualqc package and stores the
        results in the *out_dir*
        """
        command = f"visualqc_func_mri -b {bids_dir}"
        if not out_dir is None:
            command += " -o {out_dir}"
        c.run(command, echo = True)

    namespace = Collection(qct1, qcfunc, getvisualqc)

    program = Program(
      version = "0.0.1",
      namespace = namespace,
      binary = "niftytorchprep"
    )
    program.run()

if __name__ == "__main__":
    main()