# estare
<p align="center">
  𐎠𐎿𐎫𐎼
</p>

[![Python application](https://github.com/soheil-soltani/estare/actions/workflows/ci.yml/badge.svg?branch=master_pre_stage)](https://github.com/soheil-soltani/estare/actions/workflows/ci.yml)


estare was developed for aligning and stacking photos particularly astronomical photos, which may require careful adjustment before stacking.
It is run in two modes: `scan` for feature detection, and `stack` for stacking up two frames. The former is a prerequisit for the alignment step.
Run the scan mode to select features such as bright stars that are present in both frames that are going to be aligned. Later, when running the
`stack` mode, the algorithm uses the coordinates obtained in the feature detection step to adjust the frames before stacking them up. 


# Install

To install the current release, use one of the following methods.

## Python package index

`pip install estare`

Use this method if you intend to use estare as a command line tool. It is recommended to install the pip package in a virtual environment.


## From the GitHub repository

You can also download the package directly from GitHub.


# Run

If estare is installed using the `pip` distribution, you can run it from the command line by calling

`estare scan ...` or

`estare stack ...` 

On the other hand, if it is downloaded as a package, it needs to be extracted first. Afterwards, you can run it like a package: \

`python -m estare scan ...` or 

`python -m estare stack ...`

In either case, use `estare -h` for a complete guide on how to run each mode.

