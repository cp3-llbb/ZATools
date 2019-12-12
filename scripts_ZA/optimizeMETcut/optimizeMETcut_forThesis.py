# To optimize the cut on MET, we need the met_pt distribution for:
# 1) One signal sample (then it has to be extended to the 21)
# 2) All the backgrounds

#Things to do: add all the backgrounds together in order to have two superimposed histograms, one for the background and one for the signal.
# Then vary the met cut bin by bin and get the integral of the backrounds histo and of the signal histo and compute S/sqrt(B)


#! /bin/env python

import sys, os, json
import copy
import datetime
import subprocess
import numpy as np
import math
import glob
import ROOT
from ROOT import TCanvas, TPad, TLine, TH1F
import matplotlib
matplotlib.use('agg')
import matplotlib as ml
import matplotlib.pyplot as plt

import argparse

import random
from random import randint


def getHisto(path, isBkg, prefix, cat):

    _files = set()
    histo_met = TH1F("histo_met", "histo_met", 50, 0, 500)


    integral=0
    for i, filename in enumerate(glob.glob(os.path.join(path, '*.root'))):
        split_filename = filename.split('/')
        if isBkg:
            if str(split_filename[-1]).startswith("DoubleMuon") or str(split_filename[-1]).startswith("DoubleEG") or str(split_filename[-1]).startswith("MuonEG") or str(split_filename[-1]).startswith("HToZA"):
                continue
        else:
            if not str(split_filename[-1]) == prefix:
                continue
        #print split_filename[-1]
        f = ROOT.TFile.Open(filename)
        _files.add(f)
        for j, key in enumerate(f.GetListOfKeys()):
            cl = ROOT.gROOT.GetClass(key.GetClassName())
            #if key.ReadObj().GetName() == "met_pt_{0}_hZA_lljj_deepCSV_btagM_mll_cut".format(cat):
            if key.ReadObj().GetName() == "met_pt_{0}_hZA_lljj_deepCSV_btagM_no_cut".format(cat):
                key.ReadObj().SetDirectory(0)
                histo_met.Add(key.ReadObj(), 1)
        histo_met.SetDirectory(0) 

        if not isBkg:
            histo_met.Scale(1000)
    
    return histo_met


def getN(histo, metcut):
    histo.GetXaxis().SetRangeUser(0, metcut)
    N = histo.Integral()

    return N

def main():

    global lumi
    lumi = 35922. 
    #path = '/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/backToCutBased_ellipses_NoSystematics_someMinorBkgsStillMissing/slurm/output'
    path = '/nfs/user/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/backToCutBased_ellipses_NoSystematics_someMinorBkgsStillMissing/slurm/output'

    category = ["MuMu"]
    all_prefix = []
    prefix = []
    for i, filename in enumerate(glob.glob(os.path.join(path, '*.root'))):
        split_filename = filename.split('/')
        if str(split_filename[-1]).startswith("HToZA"):
            pref = split_filename[-1]
            if "2000" in pref or "3000" in pref:
                continue
            if i==5 or i==14 or i==35 or i==52 or i==25 or i==41:
                prefix.append(pref)
    
    #Remove randomly some signals
    #no_elements_to_keep = 5
    #prefix = set(random.sample(all_prefix, no_elements_to_keep))

    
    for k, cat in enumerate(category):

        i=0
        graphs = []
        histo_bkg = getHisto(path, isBkg=True, prefix="", cat=cat)
        for pref in prefix:
            split_prefix = pref.split("_")
            significance = []
            xAxis = []
            histo_sig = getHisto(path, isBkg=False, prefix=pref, cat=cat)
            for i in range(0, 251, 5):
                S = getN(histo_sig, i)
                B = getN(histo_bkg, i)
                #significance = 2*(SQRT(S+B)-SQRT(B))
                signif = math.sqrt(2*( (S+B)*math.log(1+S/B) -S ))
                #print "prefix: ", pref, "   i: ", i, "   significance: ", signif
                significance.append(float(signif))
                xAxis.append(float(i))

            significance_array = np.array(significance)
            xAxis_array = np.array(xAxis)

            labelH = pref.split('_')[1].split('-')[1]
            labelA = pref.split('_')[2].split('-')[1]

            from scipy.ndimage.filters import gaussian_filter1d
            ysmoothed = gaussian_filter1d(significance_array, sigma=3)

            plt.plot(xAxis_array, ysmoothed, label=r"$\mathrm{M_H=}$"+labelH+r",$\mathrm{M_A=}$"+labelA+" GeV")
            plt.xticks(np.arange(0, 251, 20))
            plt.plot([80,80],[0.015,0.1], color='black', linewidth=1)
            plt.ylim(0.015, 0.1)
            plt.xlabel("cut on "+r"$E^{\mathrm{miss}}_{\mathrm{T}}$"+" [GeV]", fontsize=20)
            plt.ylabel(r"$\xi$", fontsize=20)

    plt.legend()
    plt.savefig("optimizeMETcut_forthesis.pdf")


#main
if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    main()

