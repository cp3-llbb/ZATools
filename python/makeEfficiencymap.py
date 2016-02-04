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

myTGraph = TGraph2D(9)
myTGraph.SetName("efficiency")
eff = TH2D("eff","efficiency",500,0,xmax,500,0,ymax)
myTGraph.SetHistogram(eff)

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
      tree.Draw("1>>tempHist",weight_cut,"")
      tempHist=gDirectory.Get("tempHist")
      n+=1
      eff = tempHist.GetEntries()/tree.GetEntriesFast()
      myTGraph.SetPoint(n, mA, mH, eff)
      print mA, mH, eff


f = TFile("eff.root","recreate")
myTGraph.GetHistogram().Write()
f.Close()

