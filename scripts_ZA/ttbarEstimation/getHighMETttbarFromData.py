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

from random import randint



def cloneTH1(hist):
    if (hist == None):
        return None
    cloneHist = ROOT.TH1F(str(hist.GetName()) + "_clone", hist.GetTitle(), hist.GetNbinsX(), hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())
    return cloneHist


def cloneTH2(hist):
    if (hist == None):
        return None
    cloneHist = ROOT.TH2F(str(hist.GetName()) + "_clone", hist.GetTitle(), hist.GetNbinsX(), hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax(), hist.GetNbinsY(), hist.GetYaxis().GetXmin(), hist.GetYaxis().GetXmax()) 
    return cloneHist


def getHistos(path, prefix):

    _files = set()
    histos = []
    new_histos = []

    for i, filename in enumerate(glob.glob(os.path.join(path, '*.root'))):
        split_filename = filename.split('/')
        if not str(split_filename[-1]).startswith(prefix):
            continue
        f = ROOT.TFile.Open(filename)
        _files.add(f)
        histos_fromSameFile = []
        for j, key in enumerate(f.GetListOfKeys()):
            cl = ROOT.gROOT.GetClass(key.GetClassName())
            if not cl.InheritsFrom("TH1"):
                continue
            key.ReadObj().SetDirectory(0)
            histos_fromSameFile.append(key.ReadObj())
            #histos_fromSameFile[j].SetDirectory(0)
            if "met_pt" in key.ReadObj().GetName() and "MuEl" in key.ReadObj().GetName() and "inverted_met_cut" in key.ReadObj().GetName():
                print "filename: ", split_filename[-1], "   histo name: ", key.ReadObj().GetName(), "   # entries: ", key.ReadObj().GetEntries()
        histos.append(histos_fromSameFile)

    print "Number of files processed for %s: " %prefix, len(histos)
    print "Number of histograms processed for %s: " %prefix, len(histos[0])

    from pprint import pprint
    #pprint(histos)

    for j in range(0, len(histos[0])):
        if "_vs_" in str(histos[0][j].GetName()):
            new_histo = cloneTH2(histos[0][j])
        else:
            new_histo = cloneTH1(histos[0][j])
        for i in range(0, len(histos)):
            if "met_pt" in histos[i][j].GetName() and "MuEl" in histos[i][j].GetName() and "inverted_met_cut" in histos[i][j].GetName():
                print " histo name: ", histos[i][j].GetName(), "   # entries: ", histos[i][j].GetEntries()
            new_histo.Add(histos[i][j], 1)
            new_histo.SetDirectory(0)
        new_histos.append(new_histo)

    # Scale by the luminosity if MC histograms
    if prefix != 'MuonEG':
        for h in new_histos:
            h.Scale(lumi)
    
    return new_histos







def main():

 
    global lumi
    lumi = 35922. 
    #path = '/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/ttbarSplitting/slurm/output/'
    path = '/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/inverted_met_cut/slurm/output/'

    histos_data = getHistos(path, "MuonEG")
    histos_SingleTop = getHistos(path, "ST")
    new_plots = []

    if len(histos_data) != len(histos_SingleTop):
        print "Something went wrong: different number of histograms in data and MC!"
    
    for h in histos_data:
        print "BEFORE SUBTRACTION. NAME: ", h.GetName(), "    INTEGRAL: ", h.Integral()
    
    for h in histos_SingleTop:
        print "SINGLE TOP. NAME: ", h.GetName(), "    INTEGRAL: ", h.Integral()
 
    for i in range(0, len(histos_data)):
        if "MuEl" in str(histos_data[i].GetName()) and "inverted_met_cut" in str(histos_data[i].GetName()):
            histos_data[i].Add(histos_SingleTop[i], -1)
            histos_data[i].SetDirectory(0)

    # Now histos_data has the same plots as normal data except for high met MuEl, which has the SingleTop subtracted
    # In PlotIt, these histograms will be normalized with the lumi. Since this is data,
    # we don't want any normalization by lumi. To avoid this, we "normalize" all the plots
    # by 1/lumi here.

    for i in range(0, len(histos_data)):
        if "MuMu" in str(histos_data[i].GetName()) and "inverted_met_cut" in str(histos_data[i].GetName()):
            for j in range(0, len(histos_data)):
                if str(histos_data[i].GetName()).replace("MuMu", "MuEl") == str(histos_data[j].GetName()):
                    histos_data[i].Reset()
                    histos_data[i].Add(histos_data[j], 1)
                    histos_data[i].SetDirectory(0)
        if "ElEl" in str(histos_data[i].GetName()) and "inverted_met_cut" in str(histos_data[i].GetName()):
            for j in range(0, len(histos_data)):
                if str(histos_data[i].GetName()).replace("ElEl", "MuEl") == str(histos_data[j].GetName()):
                    histos_data[i].Reset()
                    histos_data[i].Add(histos_data[j], 1)
                    histos_data[i].SetDirectory(0)


    for h in histos_data:
        h.Scale(1/lumi)
        name = h.GetName()
        h.SetName(name.replace("_clone", ""))
        h.SetDirectory(0)

    for h in histos_data:
        print "AFTER SUBTRACTION. NAME: ", h.GetName(), "    INTEGRAL: ", h.Integral()

    # Save the file that contains the regions at high met defined as dataElMu - SingleTop
    r_file = ROOT.TFile.Open("dataMuEl_minus_SingleTop_inHighMET.root", "recreate")
    for hist in histos_data:
        hist.Write()
    r_file.Close()




#main
if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    main()
