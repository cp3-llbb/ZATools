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

mH=500

run_combine = 0

TGAS_1 = TGraphAsymmErrors(0)
TGAS_2 = TGraphAsymmErrors(0)

myTG_0 = TGraph(5)
myTG_1 = TGraph(5)
myTG_2 = TGraph(5)
myTG_3 = TGraph(5)
myTG_4 = TGraph(5)
myTG_5 = TGraph(5)

myTGraph = TGraph2D(9)
#myTGraph.SetNpx(100)
#myTGraph.SetNpy(100)
myTGraph.SetName("p-value")

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
    mbb=float(options.mA_list[cutkey])
    mllbb=float(options.mH_list[cutkey])
   
    DataCard = DataCards_path+str(mllbb)+"_"+str(mbb)+"/"+name+".dat"
    RootFile = RootFiles_path+str(mllbb)+"_"+str(mbb)+"_"+name+".root"
         
    if (mbb < mllbb - 90) and (mllbb > 126.0) and mllbb == mH and os.path.exists(DataCard): 
      print 'entering the loop'
      try :
        if run_combine == 1 :
          # Running combine and moving the output rootfile in the repository

          #combine_cmd = "combine -M ProfileLikelihood --signif -m "+str(int(mbb))+" "+DataCard+" --toysFreq"
          #combine_cmd = "combine -M ProfileLikelihood --significance --pvalue -m "+str(int(mbb))+" "+DataCard
          combine_cmd = "combine -M Asymptotic -m "+str(int(mbb))+" --run=blind "+DataCard
          os.system(str(combine_cmd))
          mv_cmd = "mv higgsCombineTest.Asymptotic.mH"+str(int(mbb))+".root "+RootFile
          os.system(str(mv_cmd))

        eff_file = TFile('eff.root','READ')
        eff_h = eff_file.Get('eff')
        eff = eff_h.Interpolate(mbb,mllbb)

        # Accessing the rootfile, get the p-value and fill a TGraph2D
        fList = TFile(str(RootFile)) 
        mytree  = fList.Get("limit")
        #for entry in mytree:
        mytree.GetEntry(2)
        limit=mytree.limit
        SignalYields = eff*2.2

        print 'mbb : ', mbb, ' limit : ', limit, 'eff : ', eff

        if limit > 0  and SignalYields > 0:
	  n+=1
	  myTG_2.SetPoint(n,int(mbb),mytree.limit/SignalYields)
	  TGAS_1.SetPoint(n,mbb,mytree.limit/SignalYields)
          TGAS_2.SetPoint(n,mbb,mytree.limit/SignalYields)
	  exp_limit = mytree.limit/SignalYields
          mytree.GetEntry(0)
	  TGAS_2.SetPointEYlow(n,abs(mytree.limit/SignalYields-exp_limit))
          mytree.GetEntry(4)
          TGAS_2.SetPointEYhigh(n,abs(mytree.limit/SignalYields-exp_limit))
          mytree.GetEntry(1)
          TGAS_1.SetPointEYlow(n,abs(mytree.limit/SignalYields-exp_limit))
          mytree.GetEntry(3)
          TGAS_1.SetPointEYhigh(n,abs(mytree.limit/SignalYields-exp_limit))


          mytree.GetEntry(5)
          myTG_5.SetPoint(n,int(mbb),mytree.limit/SignalYields) 
        



        #n+=1
        #myTGraph.SetPoint(n, mbb, mllbb, mytree.limit)
      except:
          print 'no background events'

gStyle.SetOptStat(0)

Cname = "C_"+str(mH)
C = TCanvas(Cname,Cname,1200,500)
C.SetLeftMargin(0.2)
C.SetBottomMargin(0.2)
C.SetTitle(" ")

TGAS_2.SetFillColor(kYellow)
TGAS_2.SetFillStyle(1001)
TGAS_2.SetLineWidth(0)
TGAS_1.SetFillColor(kGreen)
TGAS_1.SetFillStyle(1001)
TGAS_1.SetLineWidth(0)

myTG_2.SetLineColor(kBlack)
myTG_2.SetLineStyle(9)
myTG_2.SetLineWidth(2)

myTG_5.SetLineColor(kBlack)
myTG_5.SetLineWidth(2)
myTG_5.Sort()
TGAS_2.Sort()
TGAS_1.Sort()
myTG_2.Sort()

title = "M_{H} = "+str(int(mH))
TGAS_2.SetTitle(title)
TGAS_2.GetXaxis().SetTitle("M_{A}")
TGAS_2.GetXaxis().SetTitleSize(0.045)
TGAS_2.GetXaxis().SetTitleOffset(0.8)
TGAS_2.Draw('A E3')
TGAS_1.Draw('E3')
myTG_2.Draw("L")
#myTG_5.Draw("L")

leg = TLegend(0.59,0.68,0.89,0.88)
leg.SetLineColor(0)
leg.SetFillColor(0)
leg.AddEntry(TGAS_1,"CL_{s} Expected #pm 1 #sigma","F")
leg.AddEntry(TGAS_2,"CL_{s} Expected #pm 2 #sigma","F")
leg.AddEntry(myTG_2,"CL_{s} Expected","L")
leg.AddEntry(myTG_5,"CL_{s} Observed","L")
leg.Draw()

f = TFile("test_BBP.root","recreate")
C.Write()
f.Close()


###########
### FIN ###
###########
