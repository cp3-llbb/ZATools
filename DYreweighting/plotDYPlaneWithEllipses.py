#! /bin/env python

import sys, os, json
import copy
import datetime
import subprocess
import numpy as np
import glob
import math
import ROOT
from ROOT import gStyle

import argparse



def add2D (path, prefix, cat, btag):
    _files = set()
    histos = []

    Mjj_vs_Mlljj = ROOT.TH2F("Mjj_vs_Mlljj_MC","Mjj_vs_Mlljj_MC", 150, 0, 1500, 150, 0, 1500)
    Mjj_vs_Mlljj.Reset()
    Mjj_vs_Mlljj.Sumw2()
    for i, filename in enumerate(glob.glob(os.path.join(path, '*.root'))):
        split_filename = filename.split('/')
        if not str(split_filename[-1]).startswith(prefix):
            continue
        f = ROOT.TFile.Open(filename)
        _files.add(f)
        histo2D = f.Get("Mjj_vs_Mlljj_" + cat + "_hZA_lljj_deepCSV_btagM_" + "mll_and_met_cut" if btag else "Mjj_vs_Mlljj_" + cat + "_hZA_lljj_deepCSV_nobtag_" + "mll_and_met_cut")
        outputName = (Mjj_vs_Mlljj.GetName() + "_btagM_" + cat if btag else Mjj_vs_Mlljj.GetName() + "_nobtag_" + cat)
        Mjj_vs_Mlljj.Add(histo2D, 1)
        Mjj_vs_Mlljj.SetDirectory(0)
    Mjj_vs_Mlljj.SetName(outputName)
    Mjj_vs_Mlljj.SetDirectory(0)
    histos.append(Mjj_vs_Mlljj)

    return histos



def main():

    global lumi
    lumi = 35922.

    path = '/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/onlyMassPlanesToPlotDYNonReweighted/slurm/output/'

    mjj_array = np.arange(0,1000,1)
    mlljj_array = np.arange(0,1000,1)

    ROOT.gStyle.SetOptStat(0)
    h2 = ROOT.TH2F("h2", "Additional shape uncertainty on DY+Jets", 1000, 0, 1000, 1000, 0, 1000)
    h2.GetXaxis().SetTitle("m_{jj} (GeV)")
    h2.GetYaxis().SetTitle("m_{lljj} (GeV)")
    h2.GetYaxis().SetRangeUser(90,1000)
    h2.GetYaxis().SetTitleOffset(1.6)
    h2.SetMinimum(0)
    h2.SetMaximum(0.3)

    for a in mjj_array:
        for b in mlljj_array:
            DYweight=0.
            mjj_weight=0.
            mlljj_weight=0.
            mjj_weight = (1.13022 + (-0.00206761)*a + (7.0697e-06)*pow(a,2) + (-6.26383e-09)*pow(a,3) + (-2.42928e-12)*pow(a,4) + (3.84415e-15)*pow(a,5))
            mlljj_weight = ((1.3976 + (-0.00503213)*b + (2.31508e-05)*pow(b,2) + (-5.03318e-08)*pow(b,3) + (5.57681e-11)*pow(b,4) + (-3.03564e-14)*pow(b,5) + (6.40372e-18)*pow(b,6)) if (b < 1400.) else 1.)
            DYweight = mjj_weight*mlljj_weight
            h2.Fill(a, b, abs(1-float(DYweight)))

    categories = ["MuMu", "ElEl"]
    MC_histos = {
        "MuMu" : "Mjj_vs_Mlljj_DY_MC_MuMu",
        "ElEl" : "Mjj_vs_Mlljj_DY_MC_ElEl"
    }

    rhos = [0.5, 1, 1.5, 2, 2.5, 3]

    for cat in categories:

        # MC DY 
        MC_histos[cat] = add2D(path, "DY", cat, btag=False)
        xaxis_MC = MC_histos[cat][0].GetXaxis()
        xaxis_MC.SetLimits(0.,1000.)
        yaxis_MC = MC_histos[cat][0].GetYaxis()
        yaxis_MC.SetLimits(0.,1000.)
        #MC_histos[cat][0].SetMaximum(1000.)

        MC_histos[cat][0].Scale(lumi)
        MC_histos[cat][0].SetDirectory(0)

        line_mjj_1 = ROOT.TLine(100,0,100,1000)
        line_mjj_2 = ROOT.TLine(250,0,250,1000)
        line_mjj_3 = ROOT.TLine(400,0,400,1000)
        line_mjj_4 = ROOT.TLine(550,0,550,1000)
        line_mjj_5 = ROOT.TLine(700,0,700,1000)
        line_mjj_6 = ROOT.TLine(850,0,850,1000)
        line_mjj_7 = ROOT.TLine(1000,0,1000,1000)
        line_mlljj_1 = ROOT.TLine(0,150,1000,150)
        line_mlljj_2 = ROOT.TLine(0,300,1000,300)
        line_mlljj_3 = ROOT.TLine(0,450,1000,450)
        line_mlljj_4 = ROOT.TLine(0,600,1000,600)
        line_mlljj_5 = ROOT.TLine(0,750,1000,750)
        line_mlljj_6 = ROOT.TLine(0,1000,1000,1000)
        line_mjj_1.SetLineColor(ROOT.kGreen+1)
        line_mjj_2.SetLineColor(ROOT.kGreen+1)
        line_mjj_3.SetLineColor(ROOT.kGreen+1)
        line_mjj_4.SetLineColor(ROOT.kGreen+1)
        line_mjj_5.SetLineColor(ROOT.kGreen+1)
        line_mjj_6.SetLineColor(ROOT.kGreen+1)
        line_mjj_7.SetLineColor(ROOT.kGreen+1)
        line_mlljj_1.SetLineColor(ROOT.kGreen+1)
        line_mlljj_2.SetLineColor(ROOT.kGreen+1)
        line_mlljj_3.SetLineColor(ROOT.kGreen+1)
        line_mlljj_4.SetLineColor(ROOT.kGreen+1)
        line_mlljj_5.SetLineColor(ROOT.kGreen+1)
        line_mlljj_6.SetLineColor(ROOT.kGreen+1)

        #with open("../scripts_ZA/ellipsesScripts/ellipseParam_{0}.json".format(cat)) as f:
        with open("../scripts_ZA/ellipsesScripts/fullEllipseParamWindowFit_{0}_newSim_old21Points.json".format(cat)) as f:
            parameters = json.load(f)
        
            gStyle.SetOptStat("")
            for (mbb, mllbb, a_squared, b_squared, theta_rad, mA, mH) in parameters:
                print mA, mH
                ell_list = []
                c = ROOT.TCanvas("c","",700,700)
                c2 = ROOT.TCanvas("c2","c2",700,700)
                c.cd()
                MC_histos[cat][0].SetMinimum(0)
                MC_histos[cat][0].Draw("COLZ")
                line_mjj_1.Draw("same")
                line_mjj_2.Draw("same")
                line_mjj_3.Draw("same")
                line_mjj_4.Draw("same")
                line_mjj_5.Draw("same")
                line_mjj_6.Draw("same")
                line_mjj_7.Draw("same")
                line_mlljj_1.Draw("same")
                line_mlljj_2.Draw("same")
                line_mlljj_3.Draw("same")
                line_mlljj_4.Draw("same")
                line_mlljj_5.Draw("same")
                line_mlljj_6.Draw("same")
                c2.cd()
                #Plot weights
                h2.Draw("colz")
                line_mjj_1.Draw("same")
                line_mjj_2.Draw("same")
                line_mjj_3.Draw("same")
                line_mjj_4.Draw("same")
                line_mjj_5.Draw("same")
                line_mjj_6.Draw("same")
                line_mjj_7.Draw("same")
                line_mlljj_1.Draw("same")
                line_mlljj_2.Draw("same")
                line_mlljj_3.Draw("same")
                line_mlljj_4.Draw("same")
                line_mlljj_5.Draw("same")
                line_mlljj_6.Draw("same")
                for rho in rhos:
                    print "rho: ", rho
                    a = math.sqrt(a_squared)
                    b = math.sqrt(b_squared)
                    theta = theta_rad * 57.29
                    ell = ROOT.TEllipse(mbb,mllbb,rho*a,rho*b,0,360,theta)
                    ell.SetFillStyle(0)
                    ell.SetLineColor(ROOT.kMagenta)
                    ell.SetLineWidth(2)
                    ell_list.append(ell)

                for e in ell_list:
                    c.cd()
                    e.Draw("same")
                    c2.cd()
                    e.Draw("same")
                c.SaveAs("DYplusEllipses_nobtag_42weights/DYplane_nobtag_{0}_ell_{1}_{2}.png".format(cat, mH, mA), "png")
                #c.SaveAs("DYplusEllipses_nobtag_36weights/DYplane_nobtag_{0}_ell_{1}_{2}.png".format(cat, mH, mA), "png")
                #c2.SaveAs("DYplusEllipses_nobtag/DYweights_nobtag_{0}_ell_{1}_{2}.png".format(cat, mH, mA), "png")
                del c
                del ell_list[:]
            




#main
if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    main()

