import ROOT
import json
import sys
sys.path.insert(0, '/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts')
import cutWindow

#h2 = ROOT.TH2F("h2","h2",100,-20,20,100,-20,20)
#f2 = ROOT.TF2("f2","[0]*TMath::Gaus(x,[1],[2])*TMath::Gaus(y,[3],[4])",0,10,0,10)
#f2.SetParameters(1,0,5,0,7)
#h2.FillRandom("f2", 10000)


#fin = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DT_TT_ZZ_MuMu/slurm/output/non_smoothed_histo_histos_5.root", "r")
#h2 = fin.Get("h2")



#DY10-50 NAN
#fin = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DT_TT_ZZ_MuMu/slurm/output/smoothed_histo_variableN_histos_0.root", "r")
fin = ROOT.TFile.Open("smoothed_histo_variableN_histos_0.root", "r")

#DY0J NAN
#fin = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DT_TT_ZZ_MuMu/slurm/output/smoothed_histo_variableN_histos_1.root", "r")

#DY1J NAN
#fin = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DT_TT_ZZ_MuMu/slurm/output/smoothed_histo_variableN_histos_2.root", "r")

#DY2J NAN
#fin = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DT_TT_ZZ_MuMu/slurm/output/smoothed_histo_variableN_histos_3.root", "r")

#TTToLNu OK
#fin = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DT_TT_ZZ_MuMu/slurm/output/smoothed_histo_variableN_histos_4.root", "r")

#TT_Other OK
#fin = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DT_TT_ZZ_MuMu/slurm/output/smoothed_histo_variableN_histos_5.root", "r")

#OK
#fin = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DT_TT_ZZ_MuMu/slurm/output/smoothed_histo_variableN_histos_6.root", "r")

#NAN
#fin = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DT_TT_ZZ_MuMu/slurm/output/smoothed_histo_variableN_histos_7.root", "r")

#OK
#fin = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DT_TT_ZZ_MuMu/slurm/output/smoothed_histo_variableN_histos_8.root", "r")
h2 = fin.Get("h2_smoothed")


print h2.GetEntries(), h2.Integral()
neg_counter=0
pos_counter=0
for binx in range(h2.GetNbinsX()):
    for biny in range(h2.GetNbinsY()):
        bincontent = h2.GetBinContent(binx,biny)
        if bincontent < 0.:
            neg_counter = neg_counter+1
        else:
            #print "In smoothed histo: ", bincontent, binx,biny
            pos_counter = pos_counter+1

x = ROOT.Double()
y = ROOT.Double()
print "# negative bins: ", neg_counter, ", out of ", neg_counter+pos_counter

randomh2 = ROOT.TH2F("randomh2","randomh2",1000,0,1000,1000,0,1000)
for i in range(int(h2.GetEntries())):  #FIXME put #events in data
    h2.GetRandom2(x,y)
    #if i%20==0.:
    #    print x,y
    randomh2.Fill(x,y)

print "randomh2: ", randomh2.GetEntries(), randomh2.Integral()

c1 = ROOT.TCanvas("c1","c1",800,600)
h2.Draw("COLZ")
c1.SaveAs("h2_base_DY2J.png")
del c1

c2 = ROOT.TCanvas("c2","c2",800,600)
randomh2.Draw("COLZ")
c2.SaveAs("h2_random_from_base_DY2J.png")
del c2


#Fill rho histograms
filename_mumu  = "/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/fullEllipseParamWindowFit_MuMu.json"
filename_elel  = "/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/fullEllipseParamWindowFit_ElEl.json"

print "defining massWindow"
window = cutWindow.massWindow(filename_mumu)

print "opening ellipse file"
with open(filename_mumu, "r") as f:
    parameters = json.load(f)

rho_histos = []

for i, param in enumerate(parameters):
    if i>2:
        break
    "inside ellipse loop"
    rho_histo = ROOT.TH1F("rho_steps", "rho_steps", 6, 0, 3)
    "rho histo defined"
    center = (param[0], param[1])
    print center
    for binx in range(randomh2.GetNbinsX()):
        for biny in range(randomh2.GetNbinsY()):
            x = randomh2.GetXaxis().GetBinCenter(binx)
            y = randomh2.GetYaxis().GetBinCenter(biny)
            bincontent = randomh2.GetBinContent(binx,biny)
            if bincontent != 0.:
                print "Non-negative bincontent: ", bincontent
            event = (x,y)
            rho = window.getRho(center, event)
            rho_histo.Fill(rho, bincontent)
    print "Filling histo #", i
    rho_histos.append(rho_histo)
    del rho_histo

print len(rho_histos)

fout = ROOT.TFile.Open("test_DY2J_toys_fromsmoothed.root", "recreate")
for i, h in enumerate(rho_histos):
    h.SetName("rho_steps_histo_MuMu_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{0}".format(i))
    h.Write()
    fout.cd()
fout.Close()

print "End."
