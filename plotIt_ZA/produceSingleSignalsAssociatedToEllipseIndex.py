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
import shutil

path = './singleSignals_FORTHESIS'
if not os.path.exists(path):
    os.makedirs(path)
else:
    shutil.rmtree(path)           # Removes all the subdirectories!
    os.makedirs(path)


with open('../scripts_ZA/ellipsesScripts/fullEllipseParamWindowFit_MuMu_part0.json') as ell_file:
#with open('../scripts_ZA/ellipsesScripts/ellipseParam_ElEl.json') as ell_file:
    ell_index = json.load(ell_file)
for i, (mA, mH, theta, a, b, MA, MH) in enumerate(ell_index):
    with open(path+'/SignalFiles_{0}.yml'.format(i), 'a') as newFile:
        MA = format(MA, '.2f')
        MH = format(MH, '.2f')
        str_MA = str(MA).replace('.','p')
        str_MH = str(MH).replace('.','p')
        print str_MH, str_MA
        newFile.write('# '+'Signal\n')
        newFile.write('\n')
        newFile.write('\''+'HToZATo2L2B_{0}_{1}_*_histos.root'.format(str_MH, str_MA)+'\':'+'\n')
        #newFile.write('\''+'HToZATo2L2B_MH-{0}_MA-{1}_13TeV-madgraph_*_histos.root'.format(MH, MA)+'\':'+'\n')
        newFile.write('    type: signal\n')
        newFile.write('    scale: 1000\n')
        newFile.write('    line-color: '+'\''+'#'+'d62728'+'\''+ ' #'+'red\n')
        MA = float(MA)
        MH = float(MH)
        newFile.write('    legend: '+'\''+'M_{H}=%d,M_{A}=%d GeV' % (int(MH), int(MA))+'\''+'\n')
        newFile.write('    legend-order: 14\n')
        newFile.write('    line-width: 2.7\n')
        newFile.write('    line-type: 1\n')
    newFile.close()

print "Output saved in ", path
