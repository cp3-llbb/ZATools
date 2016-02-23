from ROOT import TH1F
from ROOT import *
import math
from cp3_llbb.ZATools.ZACnC import *


def main():
    options = options_()

    mg = TMultiGraph() 

    gr_btag = TGraph(4)
    gr_jec = TGraph(4)
    gr_jer = TGraph(4)

 
    mH_tested = 800.0

    syst_list = {"btag":gr_btag,
                 "jec":gr_jec,
                 "jer":gr_jer}

    syst_colors = {"btag":kRed,
                 "jec":kOrange,
                 "jer":kGreen}


    bkg_list = {"ttbar","dy2"}

    n = 0
    for cutkey in options.cut :
        mH = float(options.mH_list[cutkey])
        mA = float(options.mA_list[cutkey])
        #print mH, mA
        if (mH == mH_tested) :
            print mH, mA
            path = "./CARDS/common/"
            ANALYSIS = options.ANALYSIS
            CHANNEL = options.CHANNEL
            ERA = options.ERA
            filepath = path+ANALYSIS+"_"+CHANNEL+"_"+str(mH)+"_"+str(mA)+".input_"+ERA+".root"
            file = TFile(filepath,"READ")

            valC = 0
            for bkg in bkg_list:
                histC = file.Get("mmbbSR"+cutkey+"/"+bkg)
                valC += histC.GetBinContent(1)

            print valC
            for syst, gr_syst in syst_list.iteritems():
                valUp = 0
                valDown = 0
                for bkg in bkg_list:
                    histUp = file.Get("mmbbSR"+cutkey+"/"+bkg+"_"+syst+"Up")
                    valUp += histUp.GetBinContent(1)
                    histDown = file.Get("mmbbSR"+cutkey+"/"+bkg+"_"+syst+"Down")
                    valDown += histDown.GetBinContent(1)
                print "syst", syst, valUp, valC, valDown, " : ", (valUp-valC)/valC
                gr_syst.SetPoint(n,mA,abs(valUp-valDown)/(2*valC))

            n+=1 
            print "n : " , n 

    Cname = "C_"+str(mH)
    C = TCanvas(Cname,Cname,1200,500)
    C.SetLeftMargin(0.13)
    C.SetBottomMargin(0.13)


    #gr_btag.Draw("AC*")

    leg = TLegend(0.7,0.7,0.88,0.88)

    for syst, gr_syst in syst_list.iteritems():
        gr_syst.Sort()
        gr_syst.SetLineWidth(3)
        gr_syst.SetLineColor(syst_colors[syst])
        gr_syst.SetTitle(syst)
        leg.AddEntry(gr_syst,syst,"l")
        mg.Add(gr_syst)

    leg.SetFillColor(0)
    leg.SetLineColor(0)
    
    mg.Draw("ALP")
    mg.GetXaxis().SetTitle("m_{A} [GeV]")
    mg.GetYaxis().SetTitle("uncertainty")
    leg.Draw()
    C.Print("syst_"+str(mH_tested)+".png")


    '''
    C.Draw()
    '''
#
# main
#
if __name__ == '__main__':
    main()

