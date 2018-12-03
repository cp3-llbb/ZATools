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

    file_path = '/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/JECsplitting_rho_0_to_3_copyForBinByBinTTbarUnc/slurm/output'

    path_mjj = os.path.join(os.getcwd(),'mjj.root')

    try:
        os.stat(path_mjj)
    except:
        print "File does not exist, creating it..."

        #prefix can be either "jj_M" or "lljj_M"
        mjj_MC = getHisto(file_path, prefix="jj_M", isData=False)
        mjj_data = getHisto(file_path, prefix="jj_M", isData=True)
        
        #Saving files
        w_file = ROOT.TFile.Open("mjj.root", "recreate")
        mjj_MC.SetDirectory(0)
        mjj_data.SetDirectory(0)
        mjj_MC.Write()
        mjj_data.Write()
        w_file.Close()
    
    else: #file exist, read it
        ratio_file = ROOT.TFile.Open("mjj.root")
        mjj_MC = ratio_file.Get("jj_M_MC")
        mjj_data = ratio_file.Get("jj_M_data")

        #Draw
        c1 = ROOT.TCanvas("c1", "c1", 800, 800)
        mjj_MC.SetLineColor(kRed)
        mjj_MC.Draw()
        mjj_data.SetLineColor(kBlue)
        mjj_data.Draw("same")
        c1.SaveAs("mjj.pdf", "pdf")
        
        #create histo of ratio data/MC
        ratio_mjj = mjj_data.Clone("ratio_mjj")
        ratio_mjj.Divide(mjj_MC)
        ratio_mjj.SetMinimum(0.5)
        ratio_mjj.SetMaximum(1.5)
        #ratio_mjj.Sumw2();
        #ratio_mjj.SetStats(0)

        c2 = ROOT.TCanvas("c2", "c2", 800, 800)
        ratio_mjj.SetLineColor(kRed)
        ratio_mjj.Fit('pol5')
        ratio_mjj.Draw()
        c2.SaveAs("mjj_ratio.pdf", "pdf")

        ratio_file.Close()

##main
if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    main()
