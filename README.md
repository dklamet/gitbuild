

## Prerequisites TBD #
* devtools, intended for gnu make and gcc/g++
* python3

## Usage ##

1. Modify script with desired repo and branch. Change regular expression to select tags if desired
1. Test, wrap with script if desired to configure any special development environment

## Operation ##
1. Checks out the given repository and branch (coded into gitbuild.py) into temporary directory (name uses timestamp)
1. Parses through all commits looking for tags begining with a digit (see regex)
1. If a directory with the given tag exists, skip to next tag
1. Checks out each selected commit (those with tags).
1. Does '''git submodule init''', and '''git submodule update''' (which won't hurt anything if no submodules
1. looks for makefile (or Makefile) and does a 'make'
1. Renames directory to tag (if build fails, :FAILED is appended)
1. Each build directory has <tagname>.log file output of build.
1. Clones new directory, checkout and repeat.
1. Deletes intermediate directory at the end, if run

Intended use is to be run by cron, each half hour  


## Limitations ##

Source is checked out and builds are performed in a subdirectory of the current directory. This is currently hard-coded

# TODO

* Error checking
* Factor out and make tool command execution consistent.



Notes:

It works for me given my current limited requirements. Much simpler to set up than Jenkins, other continuous integration tools.


