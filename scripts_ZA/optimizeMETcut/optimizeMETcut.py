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

import argparse

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
            if key.ReadObj().GetName() == "met_pt_{0}_hZA_lljj_deepCSV_btagM_mll_cut".format(cat):
                key.ReadObj().SetDirectory(0)
                integral = integral + key.ReadObj().Integral()
                histo_met.Add(key.ReadObj(), 1)
        histo_met.SetDirectory(0)  

    #print "INTEGRAL: ", integral*lumi
    # Scale by the luminosity if MC histograms
    histo_met.Scale(lumi)
    
    return histo_met


def main():

    global lumi
    lumi = 35922. 
    path = '/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/backToCutBased_ellipses_NoSystematics_someMinorBkgsStillMissing/slurm/output'

    category = ["MuMu", "ElEl"]
    prefix = []
    for i, filename in enumerate(glob.glob(os.path.join(path, '*.root'))):
        split_filename = filename.split('/')
        if str(split_filename[-1]).startswith("HToZA"):
            prefix.append(split_filename[-1])
    
    
    c = []
    legend = []
    for k, cat in enumerate(category):

        legend.append(ROOT.TLegend(0.85,0.55,0.95,0.95))
        #legend[k]=ROOT.TLegend(0.85,0.55,1.0,1.0)
        #legend.SetTextFont(36)
        legend[k].SetHeader("{0} category".format(cat))
        histo_met_bkg = getHisto(path, isBkg=True, prefix="", cat=cat)

        i=0
        graphs = []
        for pref in prefix:
            split_prefix = pref.split("_")
            significance = []
            xAxis = []
            for j, i in enumerate(range(50, 151, 5)):
                histo_met_bkg.GetXaxis().SetRangeUser(0, i)
                #Check why for different i, the integral is the same
                histo_met_bkg.SetDirectory(0)
                histo_met_sig = getHisto(path, isBkg=False, prefix=pref, cat=cat)
                histo_met_sig.GetXaxis().SetRangeUser(0, i)
                histo_met_sig.SetDirectory(0)
                #significance = 2*(SQRT(S+B)-SQRT(B))
                signif = 2*(math.sqrt(histo_met_sig.Integral() + histo_met_bkg.Integral()) - math.sqrt(histo_met_bkg.Integral()))
                print "prefix: ", pref, "   i: ", i, "   significance: ", signif
                significance.append(float(signif))
                xAxis.append(float(i))

            significance_array = np.array(significance)
            xAxis_array = np.array(xAxis)
            graph = ROOT.TGraph(int(21), xAxis_array, significance_array)
            graph.SetName(split_prefix[1]+"_"+split_prefix[2])
            graphs.append(graph)

        print len(graphs)
        c.append(TCanvas("c{0}".format(k),"c{0}".format(k),800,600))
        c[k].DrawFrame(40,0.0012,160,0.02).SetTitle("Significance vs MET cut; MET cut (GeV); 2(#sqrt{S+B} - #sqrt{B})")
        for i, gr in enumerate(graphs):
            legend[k].AddEntry(gr, gr.GetName(), "l")
            gr.Draw("*L")
            gr.SetMarkerColor(i*5+2-i)
            gr.SetLineColor(i*5+2-i)
        legend[k].Draw()
        c[k].cd() 

        c[k].SaveAs("optimizeMETcut_{0}.root".format(cat))
        #del c1


#main
if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    main()

