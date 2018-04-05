#! /bin/env python

import sys, os, json
import copy
import datetime
import subprocess
import numpy as np
import glob
import ROOT

import argparse

parser = argparse.ArgumentParser() 
parser.add_argument('-p', '--path', required=True, help='Path to files')
args = parser.parse_args()

for i, full_filename in enumerate(glob.glob(os.path.join(args.path, '*.root'))):
    split_filename = full_filename.split("/")
    filename = split_filename[-1]
    print "old filename: ", filename
    new_filename = filename[:-5] + "_input_{0}.root".format(i)
    print "new filename: ", new_filename
    os.rename(os.path.join(args.path,filename), os.path.join(args.path,new_filename))

