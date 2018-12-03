#! /bin/env python

import sys, os, json
import copy
import numpy as np
import glob
import re
import os.path
import ROOT
from ROOT import TCanvas, TPad, TLine
from ROOT import kBlack, kBlue, kRed

from getHisto import getHisto
import argparse


def main():

    file_path_DYreweighted = '/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/DYreweighted_onlymjj_updown_forDY'
    file_path_DYreweighted_withmlljj = '/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/DYreweighted_mjj_and_mlljj_updown_pol6_forDY/'
    file_path_data = '/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/DYreweighted_onlymjj_updown_fordata'
    file_path_DYnoreweighted = "/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/noDYreweighted_forDY"
    #file_path_DYreweighteddividedBy1p009577814 = "/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/DYreweighted_onlymjj_updown_dividedBy1p009577814_forDY"
    #file_path_DYreweighteddividedBy1p01 = "/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/DYreweighted_mjj_and_mlljj_updown_final_copyForIntgralAndTTbarUnc/slurm/output/"
    file_path_DYreweighteddividedBy1p01 = "/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/DYreweighted_mjj_and_mlljj_updown_final/slurm/output/"

    #prefix can be either "jj_M" or "lljj_M"
    #mjj_MC = getHisto(file_path_DYreweighted, prefix="jj_M", isData=False)
    #mjj_data = getHisto(file_path_data, prefix="jj_M", isData=True)
    #mjj_MCnoreweighted = getHisto(file_path_DYnoreweighted, prefix="jj_M", isData=False)
    #mjj_MCreweighteddividedBy1p009577814 = getHisto(file_path_DYreweighteddividedBy1p009577814, prefix="jj_M", isData=False)
    
    mlljj_MCnoreweighted = getHisto(file_path_DYnoreweighted, prefix="lljj_M", isData=False)
    mlljj_MCreweighted_withmlljj = getHisto(file_path_DYreweighted_withmlljj, prefix="lljj_M", isData=False)
    mlljj_MCreweighteddividedBy1p01 = getHisto(file_path_DYreweighteddividedBy1p01, prefix="lljj_M", isData=False)

    print "Integral mlljj_MC with DY reweighted: ", mlljj_MCreweighted_withmlljj.Integral()
    print "Integral mlljj_MC no DY reweighted: ", mlljj_MCnoreweighted.Integral()
    print "mlljj reweighted/non-reweighted: ", mlljj_MCreweighted_withmlljj.Integral()/mlljj_MCnoreweighted.Integral()
    print "Integral mlljj_MC with DY reweighted by 1.01..: ", mlljj_MCreweighteddividedBy1p01.Integral()

    '''
    mjj_MCnoreweighted = getHisto(file_path_DYnoreweighted, prefix="jj_M", isData=False)
    mjj_MCreweighted_withmlljj = getHisto(file_path_DYreweighted_withmlljj, prefix="jj_M", isData=False)
    mjj_MCreweighteddividedBy1p01 = getHisto(file_path_DYreweighteddividedBy1p01, prefix="jj_M", isData=False)

    print "Integral mlljj_MC with DY reweighted: ", mjj_MCreweighted_withmlljj.Integral()
    print "Integral mlljj_MC with DY reweighted by 1.01..: ", mjj_MCreweighteddividedBy1p01.Integral()
    '''

##main
if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    main()
