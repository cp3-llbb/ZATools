import glob
import ROOT
from scipy.optimize import fsolve
import math
import json
import numpy as np

def get_a2_b2_theta(mbb, mllbb, filename_mumu):
    with open(filename_mumu) as f1:
        data = json.load(f1)
    a2 = ROOT.TGraph2D(len(data))
    a2.SetName("a2")
    b2 = ROOT.TGraph2D(len(data))
    b2.SetName("b2")
    theta = ROOT.TGraph2D(len(data))
    theta.SetName("theta")

    for i, line in enumerate(data):
        a2.SetPoint(i,line[5],line[6],line[2])
        b2.SetPoint(i,line[5],line[6],line[3])
        theta.SetPoint(i,line[5],line[6],line[4])
    
    a2_value = a2.Interpolate(mbb,mllbb)
    b2_value = b2.Interpolate(mbb,mllbb)
    theta_value = theta.Interpolate(mbb,mllbb)
    if a2_value==0.:
        for k in np.arange(0.005,100,0.005):
            if mbb>800 and mllbb>800:
                k = -k
            a2_value = a2.Interpolate(mbb+k*mbb,mllbb+k*mllbb)
            if b2_value==0.:
                b2_value = b2.Interpolate(mbb+k*mbb,mllbb+k*mllbb)
            if theta_value==0.:
                theta_value = theta.Interpolate(mbb+k*mbb,mllbb+k*mllbb)
            if a2_value != 0. and b2_value != 0. and theta_value != 0.:
                #print "k in first if: ", k, "a,b,theta: ", a2_value, b2_value, theta_value
                break
    elif b2_value==0.:
        for k in np.arange(0.005,100,0.005):
            if mbb>800 and mllbb>800:
                k = -k
            b2_value = b2.Interpolate(mbb+k*mbb,mllbb+k*mllbb)
            if theta_value==0.:
                theta_value = theta.Interpolate(mbb+k*mbb,mllbb+k*mllbb)
            if b2_value != 0. and theta_value != 0.:
                #print "k in second if: ", k, "a,b,theta: ", a2_value, b2_value, theta_value
                break

    return a2_value, b2_value, theta_value


filename_mumu  = "/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/fullEllipseParamWindowFit_MuMu.json"
filename_elel  = "/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/fullEllipseParamWindowFit_ElEl.json"

fin = ROOT.TFile.Open("DYToLL_2J_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_v6.1.0+80X_ZAAnalysis_2018-02-16-3-gd29729a_histos.root", "r")

t = fin.Get("t")

jjMuMu = t.GetBranch('jjMuMu')
lljjMuMu = t.GetBranch('lljjMuMu')
weightMuMu = t.GetBranch('weightMuMu')

print t.GetEntries()

h2 = ROOT.TH2F("h2","h2",1000,0,1000,1000,0,1000)
h2_smoothed = ROOT.TH2F("h2_smoothed","h2_smoothed",1000,0,1000,1000,0,1000)

c1 = ROOT.TCanvas("c1","c1",800,600)
c2 = ROOT.TCanvas("c2","c2",800,600)

for i in range(t.GetEntries()):
    if i%200==0:
        print "Processing: ", i, " out of ", t.GetEntries()
    t.GetEntry(i)
    ev = (t.jjMuMu, t.lljjMuMu)
    w = t.weightMuMu
    a2_value, b2_value, theta_value = get_a2_b2_theta(t.jjMuMu, t.lljjMuMu, filename_mumu)
    a=np.sqrt(a2_value)
    b=np.sqrt(b2_value)
    #Get the parameters of the elliptical gaussian from:
    #https://en.wikipedia.org/wiki/Gaussian_function, where
    # sigmax = b, sigmay = a
    #Skip the event if a and b are still 0:
    if a2_value==0. or b2_value==0.:
        continue
    p1 = (math.cos(theta_value)**2)/(2*b2_value) + (math.sin(theta_value)**2)/(2*a2_value)
    p2 = -(math.sin(2*theta_value))/(4*b2_value) + (math.sin(2*theta_value))/(4*a2_value)
    p3 = (math.sin(theta_value)**2)/(2*b2_value) + (math.cos(theta_value)**2)/(2*a2_value)
    
    f2 = ROOT.TF2("Ell2D","[0]*exp(-([1]*(x-[2])*(x-[2])+2*[3]*(x-[2])*(y-[4])+[5]*(y-[4])*(y-[4])))",0,1000,0,1000)
    f2.SetParameter(0,1) #Amplitude
    f2.SetParameter(1,p1) #p1
    f2.SetParameter(2,t.jjMuMu) #x_c
    f2.SetParameter(3,p2) #p2
    f2.SetParameter(4,t.lljjMuMu) #y_c
    f2.SetParameter(5,p3) #p3

    h2.Fill(t.jjMuMu, t.lljjMuMu, w)
    h2_smoothed.Fill(t.jjMuMu, t.lljjMuMu, w)
    for _ in range(40):
        x = ROOT.Double()
        y = ROOT.Double()
        f2.GetRandom2(x,y)
        #print f2.Eval(x,y), x, y
        #print w
        h2_smoothed.Fill(x, y, w/40)

c1.cd()
h2.SetMinimum(0)
h2.Draw("COLZ")
c1.SaveAs("non_smoothed_histo.png")
c1.SaveAs("non_smoothed_histo.root")
del c1

c2.cd()
h2_smoothed.SetMinimum(0)
h2_smoothed.Draw("COLZ")
c2.SaveAs("smoothed_histo.png")
c2.SaveAs("smoothed_histo.root")
del c2
    #f2.Draw("LEGO")
    #canvas.SaveAs("gaus2D.png")
    #del canvas

#FROM TH2 use: GetRandom2 (Double_t &x, Double_t &y) 15 times (for 15 toys).
#for i in range(n_events_MuMu_data):
#    h2_smoother.GetRandom2(Double_t &x, Double_t &y)



#for i in range(5):
#    f2.GetRandom2(x,y)
#    #Apply variable tranformation to x,y
#    
#    z = f2.Eval(x,y)
#    #print z, x, y
















