import ROOT
import json
import argparse
import numpy as np
import time
import os
import sys
sys.path.insert(0, '/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts')
import cutWindow

#TO TEST

parser = argparse.ArgumentParser(description='Generate toys from smoothed histogram') 
parser.add_argument('-cat', '--category', action='store', type=str, help='Category that you want to process. Can be either MuMu, ElEl, or MuEl.')
parser.add_argument('-sindex', '--slurmIndex', action='store', type=str, help='Slurm index for job submission')

options = parser.parse_args()

#ROOT.gRandom.SetSeed(0)
ROOT.gRandom = ROOT.TRandom3(0)
ROOT.gStyle.SetOptStat(0)

#h2 = ROOT.TH2F("h2","h2",100,-20,20,100,-20,20)
#f2 = ROOT.TF2("f2","[0]*TMath::Gaus(x,[1],[2])*TMath::Gaus(y,[3],[4])",0,10,0,10)
#f2.SetParameters(1,0,5,0,7)
#h2.FillRandom("f2", 10000)


baseDir = "/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ToysGenerationForLLE/"

fin = ROOT.TFile.Open(baseDir+"{0}/output/smoothed_{0}.root".format(options.category), "r")

h2 = fin.Get("h2_smoothed")


print h2.GetEntries(), h2.Integral()
neg_counter=0
pos_counter=0
for binx in np.arange(1,h2.GetNbinsX()+1,1):
    for biny in np.arange(1,h2.GetNbinsY()+1,1):
        bincontent = h2.GetBinContent(binx,biny)
        if bincontent < 0.:
            h2.SetBinContent(binx,biny,0)
            neg_counter = neg_counter+1
        else:
            #print "In smoothed histo: ", bincontent, binx,biny
            pos_counter = pos_counter+1

x = ROOT.Double()
y = ROOT.Double()
print "# negative bins: ", neg_counter, ", out of ", neg_counter+pos_counter

randomh2 = ROOT.TH2F("randomh2","randomh2",1000,0,1000,1000,0,1000)
#From count_events_inData.py script:
#FINAL MUMU EVENTS:  32886.0
#-----------
#FINAL ELEL EVENTS:  14288.0
#-----------
#FINAL MUEL EVENTS:  13051.0
#-----------
#FINAL NUMBER OF EVENTS:  60225.0
if options.category == "MuMu":
    n_events_forToy = 32886
elif options.category == "ElEl":
    n_events_forToy = 14288
else:
    n_events_forToy =  13051
for i in range(n_events_forToy):
    h2.GetRandom2(x,y)
    #if i%20==0.:
    #    print x,y
    randomh2.Fill(x,y)

print "randomh2: ", randomh2.GetEntries(), randomh2.Integral()

outputDir = baseDir+"{0}/toys/".format(options.category)
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

#Fill rho histograms
for fileIndex in range(0,9): #part0 to part8 of ellipse file
    filename  = "/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/fullEllipseParamWindowFit_{0}_part{1}.json".format(options.category if options.category == "MuMu" else "ElEl", fileIndex) #Use ElEl ellipse file for MuEl category 
    window = cutWindow.massWindow(filename)

    print "Working on: ", filename
    with open(filename, "r") as f:
        parameters = json.load(f)

    rho_histos = []
    for i, param in enumerate(parameters):
        rho_histo = ROOT.TH1F("rho_steps", "rho_steps", 6, 0, 3)
        center = (param[0], param[1])
        print "Filling histo # ", i
        for binx in np.arange(1,randomh2.GetNbinsX()+1,1):
            for biny in np.arange(1,randomh2.GetNbinsY()+1,1):
                x = randomh2.GetXaxis().GetBinCenter(binx)
                y = randomh2.GetYaxis().GetBinCenter(biny)
                bincontent = randomh2.GetBinContent(binx,biny)
                #if bincontent != 0.:
                #    print "Non-negative bincontent: ", bincontent
                event = (x,y)
                rho = window.getRho(center, event)
                rho_histo.Fill(rho, bincontent)
        rho_histos.append(rho_histo)
        del rho_histo

        

    fout = ROOT.TFile.Open(outputDir+"toy{0}_part{1}_histos.root".format(options.slurmIndex, fileIndex), "recreate")
    for i, h in enumerate(rho_histos):
        h.SetName("rho_steps_histo_{0}_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{1}".format(options.category, i))
        h.Write()
        #Append empy histograms to reproduce the original final structure
        if options.category=="MuMu":
            nameelel = "rho_steps_histo_ElEl_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{0}".format(i)
            h1 = ROOT.TH1F(nameelel, nameelel, 6, 0, 3)
            h1.Write()
            del h1
            namemuel = "rho_steps_histo_MuEl_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{0}".format(i)
            h1 = ROOT.TH1F(namemuel, namemuel, 6, 0, 3)
            h1.Write()
            del h1
        
        elif options.category=="ElEl":
            namemumu = "rho_steps_histo_MuMu_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{0}".format(i)
            h1 = ROOT.TH1F(namemumu, namemumu, 6, 0, 3)
            h1.Write()
            del h1
            namemuel = "rho_steps_histo_MuEl_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{0}".format(i)
            h1 = ROOT.TH1F(namemuel, namemuel, 6, 0, 3)
            h1.Write()
            del h1
        
        elif options.category=="MuEl":
            namemumu = "rho_steps_histo_MuMu_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{0}".format(i)
            h1 = ROOT.TH1F(namemumu, namemumu, 6, 0, 3)
            h1.Write()
            del h1
            nameelel = "rho_steps_histo_ElEl_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{0}".format(i)
            h1 = ROOT.TH1F(nameelel, nameelel, 6, 0, 3)
            h1.Write()
            del h1
        fout.cd()
    fout.Close()

print "End."
