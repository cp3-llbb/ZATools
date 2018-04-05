#! /bin/env python

import sys, os, json
import copy
import datetime
import subprocess
import numpy as np
import glob
import ROOT
from ROOT import TCanvas, TPad, TLine

import argparse


with open('../scripts_ZA/ellipsesScripts/ellipseParam_ElEl.json') as ell_file:
    ell_index = json.load(ell_file)
for i, (mA, mH, theta, a, b, MA, MH) in enumerate(ell_index):
    with open('./singleSignals/SignalFiles_{0}.yml'.format(i), 'a') as newFile:
        newFile.write('# '+'Signal\n')
        newFile.write('\n')
        newFile.write('\''+'HToZATo2L2B_MH-{0}_MA-{1}_13TeV-madgraph_*_histos.root'.format(MH, MA)+'\':'+'\n')
        newFile.write('    type: signal\n')
        newFile.write('    scale: 1000\n')
        newFile.write('    line-color: '+'\''+'#'+'d62728'+'\''+ ' #'+'red\n')
        newFile.write('    legend: '+'\''+'2HDM ({0},{1})'.format(MH, MA)+'\''+'\n')
        newFile.write('    legend-order: 14\n')
        newFile.write('    line-width: 2.7\n')
        newFile.write('    line-type: 1\n')
    newFile.close()
