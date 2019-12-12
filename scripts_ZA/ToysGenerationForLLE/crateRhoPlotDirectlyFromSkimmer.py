import ROOT
import json
import math
import sys
sys.path.insert(0, '/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts')
import cutWindow

#DY
fin_0 = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DY_TT_MuEl_WITHCUT/slurm/output/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_v6.1.0+80X_ZAAnalysis_2018-02-16-3-gd29729a_histos_0.root")
fin_1 = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DY_TT_MuEl_WITHCUT/slurm/output/DYToLL_0J_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_v6.1.0+80X_ZAAnalysis_2018-02-16-3-gd29729a_histos_1.root")
fin_2 = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DY_TT_MuEl_WITHCUT/slurm/output/DYToLL_1J_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_v6.1.0+80X_ZAAnalysis_2018-02-16-3-gd29729a_histos_2.root")
fin_3 = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DY_TT_MuEl_WITHCUT/slurm/output/DYToLL_2J_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_v6.1.0+80X_ZAAnalysis_2018-02-16-3-gd29729a_histos_3.root")

#TTBAR
fin_4 = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DY_TT_MuEl_WITHCUT/slurm/output/TTTo2L2Nu_13TeV-powheg_Summer16MiniAODv2_v6.1.0+80X_ZAAnalysis_2018-02-16-3-gd29729a_histos_4.root")
fin_5 = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DY_TT_MuEl_WITHCUT/slurm/output/TT_Other_TuneCUETP8M2T4_13TeV-powheg-pythia8_extended_ext0_plus_ext1_v6.1.0+80X_ZAAnalysis_2018-02-16-3-gd29729a_histos_5.root")

DY = False 
TT = True 

#smoothed_histo_histos_0.root  #DYJetsToLL_M-10to50, sigma = 18610,    SumEvW = 2.11704792387e+12
#smoothed_histo_histos_1.root  #DYToLL_0J,    sigma = 4620.52,  SumEvW = 5.3846640017e+11
#smoothed_histo_histos_2.root  #DYToLL_1J,    sigma = 859.589 , SumEvW = 4.07544622836e+11
#smoothed_histo_histos_3.root  #DYToLL_2J,    sigma = 338.259,  SumEvW = 2.1875875838e+11
#smoothed_histo_histos_4.root  #TTTo2L2Nu,    sigma = 87.31,    SumEvW = 77215440.0
#smoothed_histo_histos_5.root  #TT_Incl,      sigma = 831.76,   SumEvW = 154384189.0 


if DY:
    tree_0 = fin_0.Get("t")
    tree_1 = fin_1.Get("t")
    tree_2 = fin_2.Get("t")
    tree_3 = fin_3.Get("t")
elif TT:
    tree_4 = fin_4.Get("t")
    tree_5 = fin_5.Get("t")

#filename_mumu  = "/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/fullEllipseParamWindowFit_ElEl.json"
filename_mumu  = "/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/pavementForPValue/pavementForPValue_MuMu_part1.json"

ROOT.gStyle.SetOptStat(0)


print "opening ellipse file"
with open(filename_mumu, "r") as f:
    parameters = json.load(f)

rho_histos = []

for i, (mbb, mllbb, a2, b2, theta, mA, mH) in enumerate(parameters):
    print "Filling ellipse # ", i
    if i>5:
        break
    M11 = math.cos(theta)/math.sqrt(a2)
    M12 = math.sin(theta)/math.sqrt(a2)
    M21 = -math.sin(theta)/math.sqrt(b2)
    M22 = math.cos(theta)/math.sqrt(b2)
    window = cutWindow.massWindow(mbb,mllbb,M11,M12,M21,M22)
    if DY:
        rho_histo_0 = ROOT.TH1F("rho_steps_0", "rho_steps_0", 6, 0, 3)
        rho_histo_1 = ROOT.TH1F("rho_steps_1", "rho_steps_1", 6, 0, 3)
        rho_histo_2 = ROOT.TH1F("rho_steps_2", "rho_steps_2", 6, 0, 3)
        rho_histo_3 = ROOT.TH1F("rho_steps_3", "rho_steps_3", 6, 0, 3)
        for j in range(tree_0.GetEntries()):
            tree_0.GetEntry(j)
            rho = window.radius(tree_0.jjMuEl, tree_0.lljjMuEl)
            rho_histo_0.Fill(rho, tree_0.weightMuEl)
        for k in range(tree_1.GetEntries()):
            tree_1.GetEntry(k)
            rho = window.radius(tree_1.jjMuEl, tree_1.lljjMuEl)
            rho_histo_1.Fill(rho, tree_1.weightMuEl)
        for s in range(tree_2.GetEntries()):
            tree_2.GetEntry(s)
            rho = window.radius(tree_2.jjMuEl, tree_2.lljjMuEl)
            rho_histo_2.Fill(rho, tree_2.weightMuEl)
        for p in range(tree_3.GetEntries()):
            tree_3.GetEntry(p)
            rho = window.radius(tree_3.jjMuEl, tree_3.lljjMuEl)
            rho_histo_3.Fill(rho, tree_3.weightMuEl)
        rho_histo_0.Scale(18610/2117047923870)
        rho_histo_1.Scale(4620.52/538466400170)
        rho_histo_2.Scale(859.589/407544622836)
        rho_histo_3.Scale(338.259/218758758380)
        rho_histo_0.Add(rho_histo_1)
        rho_histo_0.Add(rho_histo_2)
        rho_histo_0.Add(rho_histo_3)
        rho_histos.append(rho_histo_0)
        del rho_histo_0
        del rho_histo_1
        del rho_histo_2
        del rho_histo_3

    elif TT:
        rho_histo_4 = ROOT.TH1F("rho_steps_4", "rho_steps_4", 6, 0, 3)
        rho_histo_5 = ROOT.TH1F("rho_steps_5", "rho_steps_5", 6, 0, 3)
        for j in range(tree_4.GetEntries()):
            tree_4.GetEntry(j)
            rho = window.radius(tree_4.jjMuEl, tree_4.lljjMuEl)
            rho_histo_4.Fill(rho, tree_4.weightMuEl)
        for k in range(tree_5.GetEntries()):
            tree_5.GetEntry(k)
            rho = window.radius(tree_5.jjMuEl, tree_5.lljjMuEl)
            rho_histo_5.Fill(rho, tree_5.weightMuEl)
        rho_histo_4.Scale(87.31/77215440.0)
        rho_histo_5.Scale(831.76/154384189.0)
        rho_histo_4.Add(rho_histo_5)
        rho_histos.append(rho_histo_4)
        del rho_histo_4
        del rho_histo_5
print len(rho_histos)

fout = ROOT.TFile.Open("test_{0}all_directlyFromSkimmed.root".format("DY" if DY else "TT"), "recreate")
for i, h in enumerate(rho_histos):
    h.SetName("rho_steps_MuEl_{0}".format(i))
    h.Write()
    fout.cd()
fout.Close()

for i, h in enumerate(rho_histos):
    c = ROOT.TCanvas("c", "c", 800,800)
    h.Draw()
    c.SaveAs("test_{0}all_directlyFromSkimmed_rho_steps_MuEl_{1}.png".format(("DY" if DY else "TT"), i))
    del c
