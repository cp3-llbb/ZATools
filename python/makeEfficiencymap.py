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

run_combine = 0

xmax = 400
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
      weight_cut = options.cut[cutkey]+" * mumu_Mll_cut"
      tree.Draw("1>>tempHist",weight_cut,"")
      tempHist=gDirectory.Get("tempHist")
      n+=1
      myTGraph.SetPoint(n, mA, mH, tempHist.GetEntries()/100000.0)


f = TFile("eff.root","recreate")
myTGraph.GetHistogram().Write()
f.Close()

