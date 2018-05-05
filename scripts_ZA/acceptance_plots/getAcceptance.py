#! /bin/env python

import sys, os, json
import copy
import datetime
import subprocess
import numpy as np
import glob
import ROOT

import argparse


def getSelectedEvents(filename):
    _files = set()
    histos = []

    f = ROOT.TFile.Open(filename)
    _files.add(f)
    hist_selected_MuMu = f.Get("jj_M_MuMu_hZA_lljj_deepCSV_btagM_no_cut") #with no btag?
    hist_selected_ElEl = f.Get("jj_M_ElEl_hZA_lljj_deepCSV_btagM_no_cut") #with no btag?
    hist_selected_MuMu.Add(hist_selected_ElEl, 1)
    events_selected = hist_selected_MuMu.GetEntries()

    return events_selected


def main():

    parser = argparse.ArgumentParser() 
    parser.add_argument('-p', '--path', required=True, help='Path to files')
    args = parser.parse_args()

    categories = ['MuMu', 'ElEl']

    ROOT.gStyle.SetOptStat(0)
    acc_graph = ROOT.TGraph2D(21)
    #acc_hist = ROOT.TH2F("acceptance", "acceptance", 70,0,1000,30,0,1000)
    index = 0

    #loop over categories
    #for cat in categories:
        #print cat
    for i, filename in enumerate(glob.glob(os.path.join(args.path, '*.root'))):
        split_filename = filename.split('/')
        if "HToZATo2L2B" not in split_filename[-1]:
            continue
        #print split_filename[-1]
        masses = split_filename[-1].split('-')
        MH = masses[1].split('_')[0]
        MA = masses[2].split('_')[0]
        if float(MH) > 1000 or float(MA) > 1000:
            continue
        gen_path = "/storage/data/cms/store/user/asaggio/HToZATo2L2B_MH-{0}_MA-{1}_13TeV-madgraph-pythia8/HToZATo2L2B_MH-{0}_MA-{1}_13TeV-madgraph_Summer16MiniAODv2/".format(MH, MA)
        for fold in glob.glob(os.path.join(gen_path, '180301*')):
            new_fold = fold.split('/')[-1]
            gen_path_new = ""
            gen_path_new = gen_path + new_fold + "/0000/output_mc_1.root"
        f_gen = ROOT.TFile.Open(gen_path_new, 'read')
        tree = f_gen.Get("t")
        gen_events = tree.GetEntries()
        print gen_events
        selected_events = getSelectedEvents(filename)
        print selected_events
        print "-----"

        acceptance = selected_events/gen_events*100
        print acceptance, MA, MH
        #acc_hist.SetBinContent(acc_hist.GetXaxis().FindBin(float(MA)), acc_hist.GetYaxis().FindBin(float(MH)), acceptance)
        #acc_graph.SetPoint(index, float(MA), float(MH), acceptance)
        #index = index+1

    #c1 = ROOT.TCanvas("c1", "c1", 600, 400)
    #acc_hist.Draw("COLZ")
    #acc_graph.Draw("")
    #c1.cd()
    #c1.SaveAs("accGraph.pdf")

#main
if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    main()

