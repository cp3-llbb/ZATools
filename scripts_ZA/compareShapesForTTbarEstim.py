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



def getSingleTop(path):

    Mjj = ROOT.TH1F("Mjj", "Mjj", 40, 10, 1000)
    Mlljj = ROOT.TH1F("Mlljj", "Mlljj", 50, 100, 1500)
    Mll = ROOT.TH1F("Mll", "Mll", 75, 12, 252)
    jet1pt = ROOT.TH1F("jet1pt", "jet1pt", 50, 20, 500)
    jet2pt = ROOT.TH1F("jet2pt", "jet2pt", 50, 20, 300)
    jjDR = ROOT.TH1F("jjDR", "jjDR", 50, 0, 6)
    lep1pt = ROOT.TH1F("lep1pt", "lep1pt", 50, 20, 400)
    lep2pt = ROOT.TH1F("lep2pt", "lep2pt", 50, 10, 200)
    jjpt = ROOT.TH1F("jjpt", "jjpt", 50, 0, 450)
    list_histos = []
    lumi = 35922
    
    # I guess the Single Top should come from the MuEl category, since we are
    # subtracting it to data which is in the MuEl category
    histoMjj_name = "jj_M_MuEl_hZA_lljj_deepCSV_btagM_"
    histoMlljj_name = "lljj_M_MuEl_hZA_lljj_deepCSV_btagM_"
    histoMll_name = "ll_M_MuEl_hZA_lljj_deepCSV_btagM_"
    histojet1pt_name = "jet1_pt_MuEl_hZA_lljj_deepCSV_btagM_"
    histojet2pt_name = "jet2_pt_MuEl_hZA_lljj_deepCSV_btagM_"
    histojjDR_name = "jj_DR_j_j_MuEl_hZA_lljj_deepCSV_btagM_"
    histolep1pt_name = "lep1_pt_MuEl_hZA_lljj_deepCSV_btagM_"
    histolep2pt_name = "lep2_pt_MuEl_hZA_lljj_deepCSV_btagM_"
    histojjpt_name = "jj_pt_MuEl_hZA_lljj_deepCSV_btagM_"

    for filename in glob.glob(os.path.join(path, '*.root')):
        split_filename = filename.split('/')
        if not str(split_filename[-1]).startswith('ST_'):
            continue

        f = ROOT.TFile(filename)
        print filename
        single_Mjj = f.Get(histoMjj_name)
        single_Mjj.SetDirectory(0)
        Mjj.Add(single_Mjj)

        single_Mlljj = f.Get(histoMlljj_name)
        single_Mlljj.SetDirectory(0)
        Mlljj.Add(single_Mlljj)

        single_Mll = f.Get(histoMll_name)
        single_Mll.SetDirectory(0)
        Mll.Add(single_Mll)

        single_jet1pt = f.Get(histojet1pt_name)
        single_jet1pt.SetDirectory(0)
        jet1pt.Add(single_jet1pt)

        single_jet2pt = f.Get(histojet2pt_name)
        single_jet2pt.SetDirectory(0)
        jet2pt.Add(single_jet2pt)

        single_jjDR = f.Get(histojjDR_name)
        single_jjDR.SetDirectory(0)
        jjDR.Add(single_jjDR)

        single_lep1pt = f.Get(histolep1pt_name)
        single_lep1pt.SetDirectory(0)
        lep1pt.Add(single_lep1pt)

        single_lep2pt = f.Get(histolep2pt_name)
        single_lep2pt.SetDirectory(0)
        lep2pt.Add(single_lep2pt)

        single_jjpt = f.Get(histojjpt_name)
        single_jjpt.SetDirectory(0)
        jjpt.Add(single_jjpt)
    
    Mjj.Scale(lumi)
    Mlljj.Scale(lumi)
    Mll.Scale(lumi)
    jet1pt.Scale(lumi)
    jet2pt.Scale(lumi)
    jjDR.Scale(lumi)
    lep1pt.Scale(lumi)
    lep2pt.Scale(lumi)
    jjpt.Scale(lumi)

    list_histos.append(Mjj)
    list_histos.append(Mlljj)
    list_histos.append(Mll)
    list_histos.append(jet1pt)
    list_histos.append(jet2pt)
    list_histos.append(jjDR)
    list_histos.append(lep1pt)
    list_histos.append(lep2pt)
    list_histos.append(jjpt)
    return list_histos


def addHistos(path, data):
    
    Mjj = ROOT.TH1F("Mjj", "Mjj", 40, 10, 1000)
    Mlljj = ROOT.TH1F("Mlljj", "Mlljj", 50, 100, 1500)
    Mll = ROOT.TH1F("Mll", "Mll", 75, 12, 252)
    jet1pt = ROOT.TH1F("jet1pt", "jet1pt", 50, 20, 500)
    jet2pt = ROOT.TH1F("jet2pt", "jet2pt", 50, 20, 300)
    jjDR = ROOT.TH1F("jjDR", "jjDR", 50, 0, 6)
    lep1pt = ROOT.TH1F("lep1pt", "lep1pt", 50, 20, 400)
    lep2pt = ROOT.TH1F("lep2pt", "lep2pt", 50, 10, 200)
    jjpt = ROOT.TH1F("jjpt", "jjpt", 50, 0, 450)
    list_histos = []
    lumi = 35922

    for filename in glob.glob(os.path.join(path, '*.root')):
        split_filename = filename.split('/')
        if data:
            histoMjj_name = "jj_M_MuEl_hZA_lljj_deepCSV_btagM_"
            histoMlljj_name = "lljj_M_MuEl_hZA_lljj_deepCSV_btagM_"
            histoMll_name = "ll_M_MuEl_hZA_lljj_deepCSV_btagM_"
            histojet1pt_name = "jet1_pt_MuEl_hZA_lljj_deepCSV_btagM_"
            histojet2pt_name = "jet2_pt_MuEl_hZA_lljj_deepCSV_btagM_"
            histojjDR_name = "jj_DR_j_j_MuEl_hZA_lljj_deepCSV_btagM_"
            histolep1pt_name = "lep1_pt_MuEl_hZA_lljj_deepCSV_btagM_"
            histolep2pt_name = "lep2_pt_MuEl_hZA_lljj_deepCSV_btagM_"
            histojjpt_name = "jj_pt_MuEl_hZA_lljj_deepCSV_btagM_"
            if not str(split_filename[-1]).startswith('MuonEG'):
                continue
        elif not data:
            histoMjj_name = "jj_M_MuMu_hZA_lljj_deepCSV_btagM_"
            histoMlljj_name = "lljj_M_MuMu_hZA_lljj_deepCSV_btagM_"
            histoMll_name = "ll_M_MuMu_hZA_lljj_deepCSV_btagM_"
            histojet1pt_name = "jet1_pt_MuMu_hZA_lljj_deepCSV_btagM_"
            histojet2pt_name = "jet2_pt_MuMu_hZA_lljj_deepCSV_btagM_"
            histojjDR_name = "jj_DR_j_j_MuMu_hZA_lljj_deepCSV_btagM_"
            histolep1pt_name = "lep1_pt_MuMu_hZA_lljj_deepCSV_btagM_"
            histolep2pt_name = "lep2_pt_MuMu_hZA_lljj_deepCSV_btagM_"
            histojjpt_name = "jj_pt_MuMu_hZA_lljj_deepCSV_btagM_"
            if not str(split_filename[-1]).startswith('TT_TuneCUETP8M2T4'):
                continue
        f = ROOT.TFile(filename)
        print filename
        single_Mjj = f.Get(histoMjj_name)
        single_Mjj.SetDirectory(0)
        Mjj.Add(single_Mjj)

        single_Mlljj = f.Get(histoMlljj_name)
        single_Mlljj.SetDirectory(0)
        Mlljj.Add(single_Mlljj)

        single_Mll = f.Get(histoMll_name)
        single_Mll.SetDirectory(0)
        Mll.Add(single_Mll)

        single_jet1pt = f.Get(histojet1pt_name)
        single_jet1pt.SetDirectory(0)
        jet1pt.Add(single_jet1pt)

        single_jet2pt = f.Get(histojet2pt_name)
        single_jet2pt.SetDirectory(0)
        jet2pt.Add(single_jet2pt)

        single_jjDR = f.Get(histojjDR_name)
        single_jjDR.SetDirectory(0)
        jjDR.Add(single_jjDR)

        single_lep1pt = f.Get(histolep1pt_name)
        single_lep1pt.SetDirectory(0)
        lep1pt.Add(single_lep1pt)

        single_lep2pt = f.Get(histolep2pt_name)
        single_lep2pt.SetDirectory(0)
        lep2pt.Add(single_lep2pt)

        single_jjpt = f.Get(histojjpt_name)
        single_jjpt.SetDirectory(0)
        jjpt.Add(single_jjpt)

    if not data:
        Mjj.Scale(lumi)
        Mlljj.Scale(lumi)
        Mll.Scale(lumi)
        jet1pt.Scale(lumi)
        jet2pt.Scale(lumi)
        jjDR.Scale(lumi)
        lep1pt.Scale(lumi)
        lep2pt.Scale(lumi)
        jjpt.Scale(lumi)
 
    list_histos.append(Mjj)
    list_histos.append(Mlljj)
    list_histos.append(Mll)
    list_histos.append(jet1pt)
    list_histos.append(jet2pt)
    list_histos.append(jjDR)
    list_histos.append(lep1pt)
    list_histos.append(lep2pt)
    list_histos.append(jjpt)
    return list_histos


def main():
    list_histos_data = []
    list_histos_ttbarMC = []
    list_histos_singleTop = []

    path_data = '/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/plots_2017-11-10_v0_deepCSV_MllCut_METCut_for_data/slurm/output/'
    path_MC = '/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/plots_2017-11-10_v0_deepCSV_MllCut_METCut_for_MCbkg/slurm/output/'

    list_histos_data = addHistos(path_data, True)
    list_histos_ttbarMC = addHistos(path_MC, False) 
    list_histos_singleTop = getSingleTop(path_MC)

    legend = []
    c1 = []
    c2 = []
    c3 = []
    pad1 = []
    pad2 = []
    subtractSingleTop = False

    for i in range(0, len(list_histos_data)):

        norm_data = list_histos_data[i].Integral()
        norm_ttbar = list_histos_ttbarMC[i].Integral()
        norm_singletop = list_histos_singleTop[i].Integral()

        print norm_data
        print norm_ttbar
        print norm_singletop


        c1.append(TCanvas("c1","c1",600,600))
        pad1.append(TPad("pad1","pad1",0,0.3,1,0.9))
        pad1[i].SetBottomMargin(0)
        pad1[i].Draw()
        pad1[i].cd()
        list_histos_data[i].SetStats(0)
        list_histos_data[i].SetMarkerColor(ROOT.kRed)
        list_histos_data[i].SetMarkerStyle(20)
        list_histos_ttbarMC[i].SetMarkerColor(ROOT.kBlue)
        list_histos_ttbarMC[i].SetMarkerStyle(22)
        # Subtract the SingleTop background
        if subtractSingleTop:
            list_histos_data[i].Add(list_histos_singleTop[i], -1)
        list_histos_data[i].Scale(1/norm_data)
        list_histos_data[i].Draw("")
        list_histos_ttbarMC[i].Scale(1/norm_ttbar)
        list_histos_ttbarMC[i].Draw("same")
        legend.append(ROOT.TLegend(0.5, 0.7, 0.8, 0.8))
        legend[i].AddEntry(list_histos_data[i], "data (El-Mu category)", "p")
        legend[i].AddEntry(list_histos_ttbarMC[i], "MC ttbar (Mu-Mu category)", "p")
        legend[i].Draw("same")

        c1[i].cd()
        pad2.append(TPad("pad2","pad2",0, 0.05, 1, 0.3))
        pad2[i].SetTopMargin(0)
        pad2[i].SetBottomMargin(0.3)
        pad2[i].Draw()
        pad2[i].cd()
        ratio = list_histos_data[i].Clone("Ratio")
        #ROOT.gStyle.SetOptTitle(0)
        ratio.SetTitle("")
        ratio.Sumw2()
        ratio.Divide(list_histos_ttbarMC[i])
        ratio.SetMarkerColor(ROOT.kBlack)
        ratio.SetMarkerSize(0.8)
        ratio.SetStats(0)
        ratio.GetYaxis().SetRangeUser(0,2)
        ratio.Draw("same")
        line = TLine(ratio.GetXaxis().GetXmin(), 1, ratio.GetXaxis().GetXmax(), 1)
        line.SetLineColor(ROOT.kBlack)
        line.Draw("")

        c1[i].cd()
        if not subtractSingleTop:
            c1[i].SaveAs("compareShapesForTTbar/plot_%i.png" % i)
            #c1[i].SaveAs("compareShapesForTTbar/plot_%i.pdf" % i)
        elif subtractSingleTop:
            c1[i].SaveAs("compareShapesForTTbar/plot_subtractSingleTop%i.png" % i)
            #c1[i].SaveAs("compareShapesForTTbar/plot_%i.pdf" % i)
            

        c3.append(TCanvas("c3","c3",600,600))
        c3[i].cd()
        list_histos_singleTop[i].Draw("")
        c3[i].SaveAs("compareShapesForTTbar/plot_SingleTop_%i.png" % i)

#main
if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    main()
