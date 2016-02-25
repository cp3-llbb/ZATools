###############
### imports ###
###############

import math
import os
import os.path
from ROOT import *
from ROOT import TMath #as tmath
from ZACnC import *
#from ROOT.TMath import LorentzVector

#ROOT.gSystem.Load('CMS_label_C')
#ROOT.gSystem.Load("DrawCanvas_C")


###################
### Definitions ###
###################


xmax = 1000
ymax = 1000

myTGraph = TGraph2D(9)
#myTGraph.SetNpx(100)
#myTGraph.SetNpy(100)
myTGraph.SetName("p-value")
h = TH2D("h","p-value",500,0,xmax,500,0,ymax)
myTGraph.SetHistogram(h)

#DataCards_path = "../cards/"
DataCards_path = "CARDS/"
RootFiles_path = "../rootfiles/"

Signal_path = "/home/fynu/amertens/scratch/cmssw/CMSSW_7_6_3/src/cp3_llbb/ZAAnalysis/"


options = options_()

effmmGr = TGraph2D(9)
effmmGr.SetName("efficiency_mumu")
effmm = TH2D("effmm","efficiency_mm",500,0,xmax,500,0,ymax)
effmmGr.SetHistogram(effmm)

effeeGr = TGraph2D(9)
effeeGr.SetName("efficiency_ee")
effee = TH2D("effee","efficiency_ee",500,0,xmax,500,0,ymax)
effeeGr.SetHistogram(effee)

eff_300 = TGraph(3)
eff_500 = TGraph(3)
eff_800 = TGraph(3)

n=-1
n3=-1
n5=-1
n8=-1

######################
### Efficiency Map ###
######################

for cutkey in options.cut :
    mH = float(options.mH_list[cutkey])
    mA = float(options.mA_list[cutkey])

    file_name = "output_signal_"+str(int(mH))+"_"+str(int(mA))+".root"
    if os.path.isfile(Signal_path+file_name) :
      sigfile = TFile(Signal_path+file_name,"READ")
      tree = sigfile.Get("t")
      #print options.cut[cutkey]
      weight_cut = options.cut[cutkey]+" * mumu_LooseZCandidate_cut"
      tree.Draw("1>>tempHistmm",weight_cut,"")
      tempHistmm=gDirectory.Get("tempHistmm")
      eff_mm = tempHistmm.GetEntries()/tree.GetEntriesFast()

      weight_cut = options.cut[cutkey]+" * elel_LooseZCandidate_cut"
      tree.Draw("1>>tempHistee",weight_cut,"")
      tempHistee=gDirectory.Get("tempHistee")
      eff_ee = tempHistee.GetEntries()/tree.GetEntriesFast()


      n+=1 
      effmmGr.SetPoint(n, mA, mH, eff_mm)
      effeeGr.SetPoint(n, mA, mH, eff_ee)

      if mH == 300 :
          n3+=1
          eff_300.SetPoint(n3,mA,eff_mm+eff_ee)

      if mH == 500 :
          n5+=1
          eff_500.SetPoint(n5,mA,eff_mm+eff_ee)

      if mH == 800 :
          n8+=1
          eff_800.SetPoint(n8,mA,eff_mm+eff_ee)


      print mA, mH, eff_mm, eff_ee


Cname = "C_"+str(mH)
C = TCanvas(Cname,Cname,1200,500)
C.SetLeftMargin(0.13)
C.SetBottomMargin(0.13)

mg = TMultiGraph()
leg = TLegend(0.7,0.2,0.88,0.5)

eff_300.Sort()
eff_300.SetLineWidth(3)
eff_300.SetLineColor(kRed)
eff_500.Sort()
eff_500.SetLineWidth(3)
eff_500.SetLineColor(kOrange)
eff_800.Sort()
eff_800.SetLineWidth(3)
eff_800.SetLineColor(kOrange+2)

leg.AddEntry(eff_300,"m_{H} = 300","l")
leg.AddEntry(eff_500,"m_{H} = 500","l")
leg.AddEntry(eff_800,"m_{H} = 800","l")

mg.Add(eff_300)
mg.Add(eff_500)
mg.Add(eff_800)

leg.SetFillColor(0)
leg.SetLineColor(0)

mg.Draw("ALP")

mg.GetXaxis().SetTitle("m_{A} [GeV]")
mg.GetYaxis().SetTitle("#epsilon ")
mg.GetXaxis().SetTitleSize(0.06)
mg.GetYaxis().SetTitleSize(0.06)
mg.GetYaxis().SetTitleOffset(0.6)


leg.Draw()
C.Print("efficiency.png")

f = TFile("eff.root","recreate")
effmmGr.GetHistogram().Write()
effeeGr.GetHistogram().Write()
f.Close()

