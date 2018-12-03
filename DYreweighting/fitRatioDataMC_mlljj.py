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

    global lumi
    lumi = 35922.
    file_path = '/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/tryWithReweightedDY/slurm/output'

    path_mlljj = os.path.join(os.getcwd(),'mlljj.root')

    try:
        os.stat(path_mlljj)
    except:
        print "File does not exist, creating it..."

        #prefix can be either "jj_M" or "lljj_M"
        mlljj_MC = getHisto.getHisto(file_path, prefix="lljj_M", isData=False)
        mlljj_data = getHisto.getHisto(file_path, prefix="lljj_M", isData=True)
        
        #Saving files
        w_file = ROOT.TFile.Open("mlljj.root", "recreate")
        mlljj_MC.SetDirectory(0)
        mlljj_data.SetDirectory(0)
        mlljj_MC.Write()
        mlljj_data.Write()
        w_file.Close()
    
    else: #file exist, read it
        ratio_file = ROOT.TFile.Open("mlljj.root")
        mlljj_MC = ratio_file.Get("lljj_M_MC")
        mlljj_data = ratio_file.Get("lljj_M_data")

        #Draw
        c1 = ROOT.TCanvas("c1", "c1", 800, 800)
        mlljj_MC.SetLineColor(kRed)
        mlljj_MC.Draw()
        mlljj_data.SetLineColor(kBlue)
        mlljj_data.Draw("same")
        c1.SaveAs("mlljj.pdf", "pdf")
        
        #create histo of ratio data/MC
        ratio_mlljj = mlljj_data.Clone("ratio_mlljj")
        ratio_mlljj.Divide(mlljj_MC)
        ratio_mlljj.SetMinimum(0.5)
        ratio_mlljj.SetMaximum(1.5)
        #ratio_mlljj.Sumw2();
        #ratio_mlljj.SetStats(0)

        c2 = ROOT.TCanvas("c2", "c2", 800, 800)
        ratio_mlljj.SetLineColor(kRed)
        fit_func = ROOT.TF1("pol6", "pol6")
        #fit_func.SetParameter(1, 0.0000005)
        ratio_mlljj.Fit(fit_func)
        #ratio_mlljj.GetXaxis().SetLimits(0, 150)
        #ratio_mlljj.GetXaxis().SetRange(0, 150)
        ratio_mlljj.Draw()
        c2.SaveAs("mlljj_ratio.pdf", "pdf")

        ratio_file.Close()

##main
if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    main()
