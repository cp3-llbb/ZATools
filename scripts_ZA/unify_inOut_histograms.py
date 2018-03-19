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

    ell_idx = "_" + str(ell_index) + "_"


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
    systematics_string = ['noSyst', 'elidisodown', 'elidisoup', 'jecdown', 'jecup', 'jerdown', 'jerup', 'jjbtagheavydown', 'jjbtagheavyup', 'jjbtaglightdown', 'jjbtaglightup', 'muiddown', 'muidup', 'muisodown', 'muisoup', 'pdfdown', 'pdfup', 'pudown', 'puup', 'scaleUncorr0', 'scaleUncorr1', 'scaleUncorr2', 'scaleUncorr3', 'scaleUncorr4', 'scaleUncorr5', 'trigeffdown', 'trigeffup']

    #At plotIt stage, if blinded put data only in overflow bin, otherwise in each bin

    filename = args.inputFile 
    split_filename = filename.split('/')
    print "filename: ", filename
                
    if "input_0.root" in split_filename[-1]:
        true_filename = "ggZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_1.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-650_MA-50_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_2.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-500_MA-200_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_3.root" in split_filename[-1]:
        true_filename = "ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_4.root" in split_filename[-1]:
        true_filename = "WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_5.root" in split_filename[-1]:
        true_filename = "WWToLNuQQ_13TeV-powheg_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_6.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-250_MA-100_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_7.root" in split_filename[-1]:
        true_filename = "DoubleEG_Run2016H-03Feb2017-v3_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_8.root" in split_filename[-1]:
        true_filename = "MuonEG_Run2016D-03Feb2017-v1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_9.root" in split_filename[-1]:
        true_filename = "DoubleMuon_Run2016G-03Feb2017-v1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_10.root" in split_filename[-1]:
        true_filename = "DoubleEG_Run2016E-03Feb2017-v1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_11.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-500_MA-50_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_12.root" in split_filename[-1]:
        true_filename = "WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_13.root" in split_filename[-1]:
        true_filename = "ST_tW_antitop_5f_noFullyHadronicDecays_13TeV-powheg_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_14.root" in split_filename[-1]:
        true_filename = "DYToLL_0J_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_15.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-800_MA-200_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_16.root" in split_filename[-1]:
        true_filename = "WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_17.root" in split_filename[-1]:
        true_filename = "DoubleEG_Run2016H-03Feb2017-v2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_18.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-1000_MA-500_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_19.root" in split_filename[-1]:
        true_filename = "ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_20.root" in split_filename[-1]:
        true_filename = "DoubleMuon_Run2016H-03Feb2017-v3_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_21.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-200_MA-100_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_22.root" in split_filename[-1]:
        true_filename = "TT_Other_TuneCUETP8M2T4_13TeV-powheg-pythia8_extended_ext0_plus_ext1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_23.root" in split_filename[-1]:
        true_filename = "DoubleEG_Run2016G-03Feb2017-v1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_24.root" in split_filename[-1]:
        true_filename = "DoubleMuon_Run2016E-03Feb2017-v1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_25.root" in split_filename[-1]:
        true_filename = "ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powheg-pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_26.root" in split_filename[-1]:
        true_filename = "MuonEG_Run2016F-03Feb2017-v1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_27.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-2000_MA-1000_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_28.root" in split_filename[-1]:
        true_filename = "ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_29.root" in split_filename[-1]:
        true_filename = "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_30.root" in split_filename[-1]:
        true_filename = "WWW_TuneCUETP8M1_13TeV-amcatnlo-pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_31.root" in split_filename[-1]:
        true_filename = "DoubleMuon_Run2016H-03Feb2017-v2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_32.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-300_MA-100_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_33.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-800_MA-700_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_34.root" in split_filename[-1]:
        true_filename = "WWTo4Q_13TeV-powheg_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_35.root" in split_filename[-1]:
        true_filename = "HZJ_HToWW_M125_13TeV_powheg_pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_36.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-300_MA-50_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_37.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-200_MA-50_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_38.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-250_MA-50_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_39.root" in split_filename[-1]:
        true_filename = "MuonEG_Run2016C-03Feb2017-v1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    #Input_40 was wrong
    elif "input_40.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-500_MA-300_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_41.root" in split_filename[-1]:
        true_filename = "WWTo2L2Nu_13TeV-powheg_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_42.root" in split_filename[-1]:
        true_filename = "ZZTo2L2Nu_13TeV_powheg_pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_43.root" in split_filename[-1]:
        true_filename = "GluGluZH_HToWWTo2L2Nu_ZTo2L_M125_13TeV_powheg_pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_44.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-800_MA-100_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_45.root" in split_filename[-1]:
        true_filename = "WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_46.root" in split_filename[-1]:
        true_filename = "WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_47.root" in split_filename[-1]:
        true_filename = "DoubleEG_Run2016C-03Feb2017-v1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_48.root" in split_filename[-1]:
        true_filename = "TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_49.root" in split_filename[-1]:
        true_filename = "ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_50.root" in split_filename[-1]:
        true_filename = "DYToLL_2J_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_51.root" in split_filename[-1]:
        true_filename = "MuonEG_Run2016B-03Feb2017-ver2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_52.root" in split_filename[-1]:
        true_filename = "ttHToNonbb_M125_TuneCUETP8M2_13TeV_powheg_pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_53.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-1000_MA-50_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_54.root" in split_filename[-1]:
        true_filename = "TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_55.root" in split_filename[-1]:
        true_filename = "DYToLL_1J_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_56.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-3000_MA-2000_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_57.root" in split_filename[-1]:
        true_filename = "ST_t-channel_top_4f_inclusiveDecays_13TeV-powheg-pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_58.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-500_MA-100_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_59.root" in split_filename[-1]:
        true_filename = "DoubleMuon_Run2016D-03Feb2017-v1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_60.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-1000_MA-200_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_61.root" in split_filename[-1]:
        true_filename = "DoubleEG_Run2016F-03Feb2017-v1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_62.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-800_MA-50_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_63.root" in split_filename[-1]:
        true_filename = "ST_tW_top_5f_noFullyHadronicDecays_13TeV-powheg_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_64.root" in split_filename[-1]:
        true_filename = "MuonEG_Run2016G-03Feb2017-v1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_65.root" in split_filename[-1]:
        true_filename = "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_66.root" in split_filename[-1]:
        true_filename = "WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_plus_ext2_plus_ext3_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_67.root" in split_filename[-1]:
        true_filename = "ttHTobb_M125_TuneCUETP8M2_13TeV_powheg_pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_68.root" in split_filename[-1]:
        true_filename = "MuonEG_Run2016H-03Feb2017-v2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_69.root" in split_filename[-1]:
        true_filename = "TTTo2L2Nu_13TeV-powheg_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_70.root" in split_filename[-1]:
        true_filename = "DoubleEG_Run2016B-03Feb2017-ver2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_71.root" in split_filename[-1]:
        true_filename = "MuonEG_Run2016E-03Feb2017-v1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_72.root" in split_filename[-1]:
        true_filename = "DoubleEG_Run2016D-03Feb2017-v1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_73.root" in split_filename[-1]:
        true_filename = "DoubleMuon_Run2016F-03Feb2017-v1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_74.root" in split_filename[-1]:
        true_filename = "MuonEG_Run2016H-03Feb2017-v3_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_75.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-300_MA-200_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_76.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-800_MA-400_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_77.root" in split_filename[-1]:
        true_filename = "WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_78.root" in split_filename[-1]:
        true_filename = "DoubleMuon_Run2016C-03Feb2017-v1_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_79.root" in split_filename[-1]:
        true_filename = "ZZTo4L_13TeV_powheg_pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_80.root" in split_filename[-1]:
        true_filename = "TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_81.root" in split_filename[-1]:
        true_filename = "DoubleMuon_Run2016B-03Feb2017-ver2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_82.root" in split_filename[-1]:
        true_filename = "HToZATo2L2B_MH-500_MA-400_13TeV-madgraph_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
    elif "input_83.root" in split_filename[-1]:
        true_filename = "TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531_histos.root"
   

    f = ROOT.TFile.Open(filename, "read")
    r_file = ROOT.TFile.Open("rhoSteps_{0}.root".format(true_filename[:-5]), "update")
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

    print "true_filename: ", true_filename
    
    for cat in category:
        print "cat: ", cat
        for ell_index in range(0, 21):
            print "ell_index: ", ell_index
            for syst_string in systematics_string:
           
                histos = getHisto(args.path, cat, ell_index, syst_string, prefix=split_filename[-1])

                #print "syst_string: ", syst_string

                integral=0
                for i, h in enumerate(histos):
                    h.GetXaxis().SetRangeUser(1,2) #true bin
                    h.SetDirectory(0)
                #    print "NAME (WORKFLOW should be at the end): ", h.GetName()
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

                r_file = ROOT.TFile.Open("rhoSteps_{0}.root".format(true_filename[:-5]), "update")
                _rfiles.add(r_file)
                r_file.SaveSelf()
                rho_steps_histo.SetDirectory(0)
                rho_steps_histo.Write()
                r_file.Close()

                del histos
                del rho_steps_histo


#main
if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    main()

