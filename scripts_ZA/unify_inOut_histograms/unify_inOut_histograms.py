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


def getHisto(path, cat, ell_index, systematics_string, prefix):

    _files = set()
    histos_sameEllipse = []

    ell_idx = "cut_" + str(ell_index) + "_"


    for i, filename in enumerate(glob.glob(os.path.join(path, '*.root'))):
        split_filename = filename.split('/')
        if not str(split_filename[-1]) == prefix:
            continue
        f = ROOT.TFile.Open(filename, "read")
        _files.add(f)
        #loop over files
        for key in f.GetListOfKeys():
            pass_basic_cut = cat in key.ReadObj().GetName() and "hZA_lljj_deepCSV_btagM_mll_and_met_cut" in key.ReadObj().GetName() and ell_idx in key.ReadObj().GetName() 
            cl = ROOT.gROOT.GetClass(key.GetClassName())
            if systematics_string=='noSyst':
                if pass_basic_cut and "isInOrOut" in key.ReadObj().GetName() and "__" not in key.ReadObj().GetName():
                    key.ReadObj().SetDirectory(0)
                    histos_sameEllipse.append(key.ReadObj())
            else:
                if pass_basic_cut and "isInOrOut" in key.ReadObj().GetName() and systematics_string in key.ReadObj().GetName():
                    key.ReadObj().SetDirectory(0)
                    histos_sameEllipse.append(key.ReadObj())

            if systematics_string=='noSyst':
                if pass_basic_cut and "overFlow" in key.ReadObj().GetName() and "__" not in key.ReadObj().GetName():
                    key.ReadObj().SetDirectory(0)
                    histos_sameEllipse.append(key.ReadObj())
            else:
                if pass_basic_cut and "overFlow" in key.ReadObj().GetName() and systematics_string in key.ReadObj().GetName():
                    key.ReadObj().SetDirectory(0)
                    histos_sameEllipse.append(key.ReadObj())
            pass_basic_cut = False

            #if "lep1_pt" in key.ReadObj().GetName() and cat in key.ReadObj().GetName() and "hZA_lljj_deepCSV_btagM_mll_and_met_cut" in key.ReadObj().GetName() and ell_idx in key.ReadObj().GetName() and systematics_string in key.ReadObj().GetName():
            #    print "lep1_pt integral: ", key.ReadObj().Integral()
            #if "jet2_eta" in key.ReadObj().GetName() and cat in key.ReadObj().GetName() and "hZA_lljj_deepCSV_btagM_mll_and_met_cut" in key.ReadObj().GetName() and ell_idx in key.ReadObj().GetName() and systematics_string in key.ReadObj().GetName():
            #    print "jet2_eta integral: ", key.ReadObj().Integral()

    #print "INTEGRAL: ", integral*lumi
    for histo in histos_sameEllipse:
        histo.SetDirectory(0)
    
    return histos_sameEllipse
    f.Close()


def main():

    parser = argparse.ArgumentParser() 
    parser.add_argument('-i', '--inputFile', required=True, help='Input file')
    parser.add_argument('-p', '--path', required=True, help='Path to files')
    args = parser.parse_args()

    _ffiles = set()
    _rfiles = set()

    global lumi
    lumi = 35922. 

    category = ["MuMu", "ElEl"]
    systematics_string = ['noSyst', 'elidisodown', 'elidisoup', 'jecdown', 'jecup', 'jerdown', 'jerup', 'jjbtagheavydown', 'jjbtagheavyup', 'jjbtaglightdown', 'jjbtaglightup', 'muiddown', 'muidup', 'muisodown', 'muisoup', 'pdfdown', 'pdfup', 'pudown', 'puup', 'scaleUncorr0', 'scaleUncorr1', 'scaleUncorr2', 'scaleUncorr3', 'scaleUncorr4', 'scaleUncorr5', 'scaleUncorrdown', 'scaleUncorrup', 'trigeffdown', 'trigeffup']

    #At plotIt stage, if blinded put data only in overflow bin, otherwise in each bin

    filename = args.inputFile 
    split_filename = filename.split('/')
    print "filename: ", filename
    

    f = ROOT.TFile.Open(filename, "read")
    new_filename = split_filename[-1].rstrip('.root')
    new_filename = new_filename.rsplit('_', 2)[0]
    print "new_filename: ", new_filename

    r_file = ROOT.TFile.Open(new_filename+".root", "update")
    #loop over files
    for d, key in enumerate(f.GetListOfKeys()):
        cl = ROOT.gROOT.GetClass(key.GetClassName())
        if "isInOrOut" not in key.ReadObj().GetName() and "overFlow" not in key.ReadObj().GetName():
            if cl.InheritsFrom("TH1") or cl.InheritsFrom("TH2"):
                key.ReadObj().SetDirectory(0)
            key.ReadObj().Write()
    #    print "d: ", d
    print "NOW CLOSE FIRST FILE"
    r_file.Close()
    print "NOW CLOSE SECOND FILE"
    f.Close()
    print "FILES CLOSED"


    for cat in category:
        print "cat: ", cat
        for ell_index in range(0, 21):
            print "ell_index: ", ell_index
            for syst_string in systematics_string:
           
                histos = getHisto(args.path, cat, ell_index, syst_string, prefix=split_filename[-1])

                integral=0
                for i, h in enumerate(histos):
                    h.GetXaxis().SetRangeUser(1,2) #true bin
                    h.SetDirectory(0)
                    integral = integral + h.Integral()
                print "Integral from sum: ", integral

                if syst_string == 'noSyst':
                    rho_steps_histo = TH1F("rho_steps_histo_{0}_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{1}".format(cat, ell_index), "rho_steps_histo_{0}_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{1}".format(cat, ell_index), 7, 0, 7)
                else:
                    rho_steps_histo = TH1F("rho_steps_histo_{0}_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{1}__{2}".format(cat, ell_index, syst_string), "rho_steps_histo_{0}_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{1}__{2}".format(cat, ell_index, syst_string), 7, 0, 7)
                for i, h in enumerate(histos):
                    h.GetXaxis().SetRangeUser(1,2) #true bin
                    h.SetDirectory(0)
                    rho_steps_histo.SetBinContent(rho_steps_histo.FindBin(i), h.Integral())

                print "Integral from final histo: ", rho_steps_histo.Integral()

                r_file = ROOT.TFile.Open(new_filename+".root", "update")
                rho_steps_histo.SetDirectory(0)
                rho_steps_histo.Write()
                r_file.Close()

                del histos
                del rho_steps_histo

#main
if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    main()

