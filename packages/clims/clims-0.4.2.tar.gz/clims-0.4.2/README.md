# Table of Contents
[[_TOC_]]

# clims

Command-line interface for materials simulations. 

Basically pulls together usefull python packages of the materials simulation community:

* [ASE](https://wiki.fysik.dtu.dk/ase/index.html)
* [spglib](https://spglib.github.io/spglib/) (cyrstal symmetry properties)
* [phonopy](https://phonopy.github.io/phonopy/) (phonon properties from finite-differences)

This package is tailored for the needs of FHI-aims.

## System requirements

A python 3 installation with a version `python>=3.7` is required. To check your python version type:
```
python --version
```

In the following instructions on some systems it may be needed to use `python3` and `pip3`.

On a computer with such an installation, the below commands will install a number of other useful community packages for atomistic simulations as prerequisites, most importantly, `ASE`, `spglib`, `phonopy`, as well as several others.

Please also see the troubleshooting notes below in case you encounter a particular, missing prerequisite during the installation process.

## How to install

It is best to install `clims` in a virtual environment. May not always true, e.g. on computing clusters. 

### Install/Activate virtualenv (optional)

Make sure that `virtualenv` is installed:
```
pip show virtualenv 
```
If not installed, install it:
```
pip install --user virtualenv
```

Go into the root directory of clims. Initialize the virtual environment:
```
python -m venv env
```

Activate the virtual environment:
```
source env/bin/activate
```

You should now see `(env)` in at the beginning of your command line.


### Install clims

Install clims (make sure that you are in the root director of clims (where this README is)) with:
```
pip install --user .

```

If all goes well, you will have a working clims installation after this step. If something does not work (for instance, if a particular installation prerequisite that should be part of python is missing), unfortunately the error messages written by `pip` can be somewhat cryptic. As an approximate rule, the final line of a python error message often identifies the piece that was missing.

To test your installation you can run:
```
pytest -vv
```

### Troubleshooting

**Installation under CentOS**: In order for this installation to work, we noticed that the `_ctypes` module is required. This only works if the library `libffi` (including development headers - sometimes called `libffi-dev` or `libffi-devel`) is also required and the computer's python version must have been built with support for `libffi-dev` (or `libffi-devel`). If support for `libffi` headers is not present, then someone will unfortunately have to rebuild and reinstall the python >= 3.7 installation on the computer you are using from scratch.


## How to configure clims

The most important thing to set is the path to the FHI-aims species defaults:
```
clims-configure --species-path <your/path/to/FHIaims/species_defaults>
```

## Features

After successful installation the following commands should be available in the terminal:

| clims command | description |
| ------ | ------ |
| `clims-unit-cell-info` | Get brief overview of input structure, if periodic: generate primitive or conventional unit cell. |
| `clims-supercell` | Generate supercell. |
| `clims-real2frac`,`clims-frac2real`| Convert atomic coordinates of periodic structure from Cartesian to real and vice versa. |
| `clims-phonopy-initialize`, `clims-phonopy-postprocess` | Generate supercell structures with displaced atoms (initialize) and read forces after FHI-aims calculation to plot phonon DOS (postprocess). |
| `clims-wigner-seitz-cluster` | Constructs a Cluster of the shape of the Wigner-Seitz cell. |
| `clims-aimsplot` | Famous aimsplot script for plotting band structure and DOS from FHI-aims. |
| `clims-xyplot` | Simple X-Y plot of data files. |
| `clims-prepare-run` | Create `control.in` template based on a `geometry.in` file. If requested a submission file is provided, too. |
| `clims-configure` | Configure Path to exectutable and species defaults directory, mpi run command, submission header. Needed e.g. for `clims-prepare-run` |
| `clims-testsuite` | Create a testsuite of all defined input parameter combinations. |
