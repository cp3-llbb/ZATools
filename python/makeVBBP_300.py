###############
### imports ###
###############

import math
import os
import os.path
import numpy as numpy
from ROOT import *
from ROOT import TMath #as tmath
from ZACnC import *

import CMS_lumi, tdrstyle

#from ROOT.TMath import LorentzVector

#ROOT.gSystem.Load('CMS_label_C')
#ROOT.gSystem.Load("DrawCanvas_C")


def drawTheoryGraph(gr, tb):

    x1 = 160
    lenght = 20
    x2 = x1+20
    y1 = gr.Eval(x1)
    y2 = gr.Eval(x2)

    pente = math.atan( 300/4 *(log10(y2)-log10(y1))/(x2-x1))
    angle = pente*180/math.pi

    x3 = x1 + lenght*math.cos(pente)
    y3 = gr.Eval(x3)

    print angle
    print x1, y1, x3, y3

    size = 10
    x_pl = numpy.array([x1-size, x3+size, x3+size, x1-size, x1-size], dtype=float) #[x1+10, x2+10, x2-10, x1-10, x1+10]
    y_pl = numpy.array([y1+size, y3+size, y3-size, y1-size, y1+size], dtype=float)
    pline = TPolyLine(5,x_pl,y_pl)
    pline.SetFillColor(kWhite)
    pline.Draw("f")

    l = TLatex(x1,y1,"tan #beta = "+str(tb))
    l.SetTextSize(20)
    l.SetTextFont(43)
    l.SetTextAlign(12)
    l.SetTextAngle(angle)
    l.SetTextColor(gr.GetLineColor())
    l.Draw()
    SetOwnership( l, False )
    SetOwnership( pline, False )




###################
### Definitions ###
###################

mH=300

run_combine = 0
run_blind = 0

TGAS_1 = TGraphAsymmErrors(0)
TGAS_2 = TGraphAsymmErrors(0)

myTG_0 = TGraph(2)
myTG_1 = TGraph(2)
myTG_2 = TGraph(2)
myTG_3 = TGraph(2)
myTG_4 = TGraph(2)
myTG_5 = TGraph(2)

myTG_8TeV = TGraph(2)

myTGraph = TGraph2D(9)
#myTGraph.SetNpx(100)
#myTGraph.SetNpy(100)
myTGraph.SetName("p-value")

#DataCards_path = "../cards/"
DataCards_path = "CARDS_combined/"
RootFiles_path = "../rootfiles_combined/"

Signal_path = "/home/fynu/amertens/scratch/cmssw/CMSSW_7_6_3/src/cp3_llbb/ZAAnalysis/"

options = options_()

#######################
### Initializations ###
#######################

n=-1

############################
### Getting 8 TeV limits ###
############################


f = TFile("Limit_XS_eff.root")
h_exp = f.Get("h22_lt")
h_exp.SetDirectory(0)
f.Close()

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
          if run_blind == 1 :
              combine_cmd = "combine -M Asymptotic -m "+str(int(mbb))+" --run=blind "+DataCard
          else :
              combine_cmd = "combine -M Asymptotic -m "+str(int(mbb))+" "+DataCard
          os.system(str(combine_cmd))
          mv_cmd = "mv higgsCombineTest.Asymptotic.mH"+str(int(mbb))+".root "+RootFile
          os.system(str(mv_cmd))
        '''
        eff_file = TFile('eff.root','READ')
        eff_h = eff_file.Get('eff')
        eff = eff_h.Interpolate(mbb,mllbb)
        '''
        # Accessing the rootfile, get the p-value and fill a TGraph2D
        fList = TFile(str(RootFile)) 
        mytree  = fList.Get("limit")
        #for entry in mytree:
        mytree.GetEntry(2)
        limit=mytree.limit
        SignalYields = 1 #eff*2.2

        print 'mbb : ', mbb, ' limit : ', limit #, 'eff : ', eff

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
        
          limit_8TeV = h_exp.Interpolate(int(mbb),int(mllbb))
          print "8TeV : ", limit_8TeV
          myTG_8TeV.SetPoint(n,int(mbb),limit_8TeV)
 
        #n+=1
        #myTGraph.SetPoint(n, mbb, mllbb, mytree.limit)
      except:
          print 'no background events'

gStyle.SetOptStat(0)

'''
Cname = "C_"+str(mH)
C = TCanvas(Cname,Cname,1200,1200)
C.SetLeftMargin(0.2)
C.SetBottomMargin(0.2)
C.SetTitle(" ")
'''

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "2.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 800; 
W_ref = 800; 
W = W_ref
H  = H_ref

iPeriod = 4

# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref

canvas = TCanvas("C_"+str(mH),"C_"+str(mH),50,50,W,H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)
canvas.SetTicky(0)

#draw the lumi text on the canvas
CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)

TGAS_2.SetFillColor(kYellow)
TGAS_2.SetFillStyle(1001)
TGAS_2.SetLineWidth(0)
TGAS_1.SetFillColor(kGreen)
TGAS_1.SetFillStyle(1001)
TGAS_1.SetLineWidth(0)

myTG_2.SetLineColor(kBlack)
myTG_2.SetLineStyle(9)
myTG_2.SetLineWidth(2)

myTG_8TeV.SetLineColor(kBlue)
myTG_8TeV.SetLineWidth(2)

myTG_5.SetLineColor(kBlack)
myTG_5.SetLineWidth(2)
myTG_5.Sort()
TGAS_2.Sort()
TGAS_1.Sort()
myTG_2.Sort()
myTG_8TeV.Sort()

#gPad.SetLogy()

title = "M_{H} = "+str(int(mH))
TGAS_2.SetTitle(title)
TGAS_2.GetXaxis().SetTitle("M_{A}")
#TGAS_2.GetXaxis().SetTitleSize(0.045)
#TGAS_2.GetXaxis().SetTitleOffset(0.8)
#TGAS_2.SetMinimum(0)
TGAS_2.Draw('A E3')
TGAS_1.Draw('E3')
myTG_2.Draw("L*")
myTG_2.SetMarkerStyle(20)
if run_blind == 0 :
    myTG_5.Draw("L*")
    myTG_5.SetMarkerStyle(20)
if run_blind == 1 :
    myTG_8TeV.Draw("L")

TGAS_2.GetXaxis().SetTitle("m_{A} [GeV]")
TGAS_2.GetYaxis().SetTitle("#sigma #times BR [fb]")
TGAS_2.GetYaxis().SetTitleOffset(1.30)
TGAS_2.SetMinimum(10)
TGAS_2.SetMaximum(100000)



xAxis = TGAS_2.GetXaxis()
#xAxis.SetNdivisions(6,5,0)

yAxis = TGAS_2.GetYaxis()
#yAxis.SetNdivisions(6,5,0)
yAxis.SetTitleOffset(1)

## Adding theory curves

file_theory = TFile("xsec.root")
gr_tb1 = file_theory.Get("Xsec_mH"+str(mH)+"_tb1")
gr_tb1_5 = file_theory.Get("Xsec_mH"+str(mH)+"_tb1.5")

gr_tb1.SetLineColor(kGray+1)
gr_tb1.SetLineStyle(2)
gr_tb1.SetLineWidth(3)

gr_tb1_5.SetLineColor(kGray+3)
gr_tb1_5.SetLineStyle(2)
gr_tb1_5.SetLineWidth(3)

gr_tb1.Draw("C")
gr_tb1_5.Draw("C")

drawTheoryGraph(gr_tb1, 1)
drawTheoryGraph(gr_tb1_5, 1.5)

canvas.Update()

#gPad().SetLogy(1)

leg = TLegend(0.59,0.68,0.89,0.88)
leg.SetLineColor(0)
leg.SetFillColor(0)
leg.SetShadowColor(0)
leg.AddEntry(TGAS_1,"CL_{s} Expected #pm 1 #sigma","F")
leg.AddEntry(TGAS_2,"CL_{s} Expected #pm 2 #sigma","F")
leg.AddEntry(myTG_2,"CL_{s} Expected","L")
leg.AddEntry(myTG_5,"CL_{s} Observed","L")
#leg.AddEntry(myTG_8TeV,"8 TeV","L")
leg.Draw()

gPad.SetLogy(1)

#draw the lumi text on the canvas
CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)

canvas.cd()
canvas.Update()
canvas.RedrawAxis()
frame = canvas.GetFrame()
frame.Draw()


if run_blind :
    canvas.Print("BBP"+str(mH)+"_blind_v2.pdf")
    canvas.Print("BBP"+str(mH)+"_blind_v2.png")
    f = TFile("narrow_BBP"+str(mH)+"_blind_v2.root","recreate")
else :
    canvas.Print("BBP"+str(mH)+"_v2.pdf")
    canvas.Print("BBP"+str(mH)+"_v2.png")
    f = TFile("narrow_BBP"+str(mH)+"_v2.root","recreate")

canvas.Write()
f.Close()

###########
### FIN ###
###########
