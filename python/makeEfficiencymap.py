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


xmax = 500
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

n=-1

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

      print mA, mH, eff


f = TFile("eff.root","recreate")
effmmGr.GetHistogram().Write()
effeeGr.GetHistogram().Write()
f.Close()

