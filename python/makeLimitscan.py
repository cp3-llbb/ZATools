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

ROOT.gSystem.Load('/home/fynu/amertens/scratch/cmssw/CMSSW_7_1_5/src/LorentzVectorDict_cc.so')

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

#######################
### Initializations ###
#######################

n=-1

#######################
### Running Combine ###
#######################

for cutkey in options.cut :

    name = "HtoZAtoLLBB_mumu_13TeV"
    mH = float(options.mH_list[cutkey])
    mA = float(options.mA_list[cutkey])
    
    DataCard = DataCards_path+str(mH)+"_"+str(mA)+"/"+name+".dat"
    RootFile = RootFiles_path+str(mH)+"_"+str(mA)+"_"+name+".root"
    mbb=options.mA_list[cutkey]
    mllbb=options.mH_list[cutkey]
         
    if (mbb < mllbb - 90) and (mllbb > 126.0) and os.path.exists(DataCard): 

      try :
        if run_combine == 1 :
          # Running combine and moving the output rootfile in the repository

          #combine_cmd = "combine -M ProfileLikelihood --signif -m "+str(int(mbb))+" "+DataCard+" --toysFreq"
          #combine_cmd = "combine -M ProfileLikelihood --significance --pvalue -m "+str(int(mbb))+" "+DataCard
          combine_cmd = "combine -M Asymptotic -m "+str(int(mbb))+" --run=blind "+DataCard
          os.system(str(combine_cmd))
          mv_cmd = "mv higgsCombineTest.Asymptotic.mH"+str(int(mbb))+".root "+RootFile
          os.system(str(mv_cmd))

        # Accessing the rootfile, get the p-value and fill a TGraph2D
        fList = TFile(str(RootFile)) 
        mytree  = fList.Get("limit")

        #for entry in mytree:
        mytree.GetEntry(2)
        limit=mytree.limit

        n+=1
        myTGraph.SetPoint(n, mbb, mllbb, mytree.limit)
      except:
          print 'no background events'

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
myTGraph.GetHistogram().GetZaxis().SetTitle("Limit on N of events")


f = TFile("limits.root","recreate")
myTGraph.GetHistogram().Write()
f.Close()


###########
### FIN ###
###########
