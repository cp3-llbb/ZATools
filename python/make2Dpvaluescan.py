###############
### imports ###
###############

import math
import os
from ROOT import *
from ROOT import TMath as tmath
from ZACnC import *

#ROOT.gSystem.Load('CMS_label_C')
#ROOT.gSystem.Load("DrawCanvas_C")


###################
### Definitions ###
###################

run_combine = 1

xmax = 1200
ymax = 1200

myTGraph = TGraph2D(9)
#myTGraph.SetNpx(100)
#myTGraph.SetNpy(100)
myTGraph.SetName("p-value")
h = TH2D("h","p-value",500,0,xmax,500,0,ymax)
myTGraph.SetHistogram(h)

DataCards_path = "../cards/"
RootFiles_path = "../rootfiles/"

#######################
### Initializations ###
#######################

n=-1

#######################
### Running Combine ###
#######################

options = options_()

for cutkey in options.cut :

    name = cutkey
    DataCard = DataCards_path+name+".txt"
    RootFile = RootFiles_path+name+".root"
    mbb=options.mA_list[cutkey]
    mllbb=options.mH_list[cutkey]
         
    if (mbb < mllbb - 90) and (mllbb > 126.0) and os.path.exists(DataCard): 

      if run_combine == 1 :
        # Running combine and moving the output rootfile in the repository

        #combine_cmd = "combine -M ProfileLikelihood --signif -m "+str(int(mbb))+" "+DataCard+" --toysFreq"
        combine_cmd = "combine -M ProfileLikelihood --significance --pvalue -m "+str(int(mbb))+" "+DataCard
        os.system(str(combine_cmd))
        mv_cmd = "mv higgsCombineTest.ProfileLikelihood.mH"+str(int(mbb))+".root "+RootFile
        os.system(str(mv_cmd))

      # Accessing the rootfile, get the p-value and fill a TGraph2D

      fList = TFile(str(RootFile)) 
      mytree  = fList.Get("limit")
      for entry in mytree:
        print "p-value(",int(mbb) , ", " , int(mllbb),") = ", mytree.limit
        n+=1
        myTGraph.SetPoint(n, mbb, mllbb, mytree.limit)
        '''
        nSigma = tmath.sqrt(2)*tmath.ErfInverse(1-2*mytree.limit)
        print mbb, mllbb, mytree.limit, nSigma
        myTGraph_sigma.SetPoint(n, mbb, mllbb, nSigma)
        '''

gStyle.SetOptStat(0)



C2=TCanvas("C2","C2",600,600)
gStyle.SetPalette(52)
#ROOT.setTDRStyle()
C2.SetTopMargin(0.05)
C2.SetRightMargin(0.2)
C2.SetLeftMargin(0.2)
C2.SetBottomMargin(0.2)
C2.SetLogz()
myTGraph.GetHistogram().Draw("colz")
myTGraph.SetTitle("p-value")
myTGraph.GetXaxis().SetRangeUser(0,1200)
myTGraph.GetYaxis().SetRangeUser(0,1200)
myTGraph.GetHistogram().GetXaxis().SetTitle("m_{bb} (GeV)")
myTGraph.GetHistogram().GetYaxis().SetTitle("m_{llbb} (GeV)")
myTGraph.GetHistogram().GetZaxis().SetTitle("p-value")


f = TFile("pvalue.root","recreate")
myTGraph.GetHistogram().Write()
f.Close()


###########
### FIN ###
###########
