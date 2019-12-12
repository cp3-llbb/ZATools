import glob
import ROOT
from scipy.optimize import fsolve
import math
import json
import numpy as np
import argparse

def get_a2_b2_theta(mbb, mllbb, filename):
    with open(filename) as f1:
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


parser = argparse.ArgumentParser(description='Smooth histograms for toys') 
parser.add_argument('-i', '--skimmedRootFileSuffix', action='store', type=str, help='Suffix of skimmed ROOT file containing Mjj, Mlljj and the weight for the main backgrounds. N.B. This prefix must be unique to the file (e.g. slurm_1.root).')
parser.add_argument('-cat', '--category', action='store', type=str, help='Category that you want to process. Can be either MuMu, ElEl, or MuEl.')

options = parser.parse_args()


ROOT.gStyle.SetOptStat(0)
#filename_mumu  = "/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/fullEllipseParamWindowFit_MuMu.json"
#filename_elel  = "/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/fullEllipseParamWindowFit_ElEl.json"
filename_mumu  = "/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/pavementForPValue/pavementForPValue_0p3_0p3.json"
filename_elel  = "/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/pavementForPValue/pavementForPValue_0p3_0p3.json"

filename = filename_mumu if options.category=="MuMu" else filename_elel

print "Ellipse file used: ", filename

inputDir = '/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/skimmerForToys_DY_TT_{0}_WITHCUT/slurm/output/'.format(options.category)
outputDir = './{0}/output/pointsOfPvalueScan/'.format(options.category)

for f in glob.glob(inputDir+"*gd29729a_histos*.root"):
    if options.skimmedRootFileSuffix in f:
        print "File found: ", f
        fileToOpen = f
        break

fin = ROOT.TFile.Open(fileToOpen, "r")
t = fin.Get("t")

jj = t.GetBranch('jj{0}'.format(options.category))
lljj = t.GetBranch('lljj{0}'.format(options.category))
weight = t.GetBranch('weight{0}'.format(options.category))

#Define the histograms
h2 = ROOT.TH2F("h2","h2",1000,0,1000,1000,0,1000)
h2_smoothed = ROOT.TH2F("h2_smoothed","h2_smoothed",1000,0,1000,1000,0,1000)


c1 = ROOT.TCanvas("c1","c1",800,800)
c2 = ROOT.TCanvas("c2","c2",800,800)
c1.SetRightMargin(0.15)
c2.SetRightMargin(0.15)
c1.SetLeftMargin(0.16)
c2.SetLeftMargin(0.16)

for i in range(t.GetEntries()):
    if i%200==0:
        print "Processing: ", i, " out of ", t.GetEntries()
    t.GetEntry(i)
    jj = t.jjMuMu if options.category=="MuMu" else (t.jjElEl if options.category=="ElEl" else t.jjMuEl)
    lljj = t.lljjMuMu if options.category=="MuMu" else (t.lljjElEl if options.category=="ElEl" else t.lljjMuEl)
    w = t.weightMuMu if options.category=="MuMu" else (t.weightElEl if options.category=="ElEl" else t.weightMuEl)
    ev = (jj, lljj)
    a2_value, b2_value, theta_value = get_a2_b2_theta(jj, lljj, filename)
    a=np.sqrt(a2_value)
    b=np.sqrt(b2_value)
    #Get the parameters of the elliptical gaussian from:
    #https://en.wikipedia.org/wiki/Gaussian_function, where
    # sigmax = b, sigmay = a
    theta_value = 1.5708-theta_value #to stick to the wikipedia definition
    #Skip the event if a and b are still 0:
    if a2_value==0. or b2_value==0.:
        continue
    p1 = (math.cos(theta_value)**2)/(2*b2_value) + (math.sin(theta_value)**2)/(2*a2_value)
    p2 = -(math.sin(2*theta_value))/(4*b2_value) + (math.sin(2*theta_value))/(4*a2_value)
    p3 = (math.sin(theta_value)**2)/(2*b2_value) + (math.cos(theta_value)**2)/(2*a2_value)

    f2_minx = jj-0.4*jj #allow a 40% window for gaussian definition
    f2_maxx = jj+0.4*jj
    f2_miny = lljj-0.5*lljj #allow a 50% window for gaussian definition
    f2_maxy = lljj+0.5*lljj
    
    f2 = ROOT.TF2("Ell2D","[0]*exp(-([1]*(x-[2])*(x-[2])+2*[3]*(x-[2])*(y-[4])+[5]*(y-[4])*(y-[4])))",f2_minx,f2_maxx,f2_miny,f2_maxy)
    f2.SetParameter(0,1) #Amplitude
    f2.SetNpx(int(f2_maxx-f2_minx))
    f2.SetNpy(int(f2_maxy-f2_miny))
    
    f2.SetParameter(1,p1) #p1
    f2.SetParameter(2,jj) #x_c
    f2.SetParameter(3,p2) #p2
    f2.SetParameter(4,lljj) #y_c
    f2.SetParameter(5,p3) #p3

    #if t.jjMuMu>50 and t.jjMuMu<120. and t.lljjMuMu>300. and t.lljjMuMu<400.:
    #    cc = ROOT.TCanvas("cc","cc",800,600)
    #    print "a,b,theta, jj, lljj: ", a,b,theta_value, t.jjMuMu, t.lljjMuMu
    #    print "p1,p2,p3: ", p1, p2, p3
    #    f2.Draw("LEGO")
    #    cc.SaveAs("gaus2D.png")

    h2.Fill(jj, lljj, w)
    #Throw less points in in bulk of bkg:
    if jj > 50 and jj < 150 and lljj > 160 and lljj < 300:
        nThrownPoints=10
    else:
        if options.category == "MuMu" or options.category == "ElEl":
            nThrownPoints=60
        else:
            nThrownPoints=30  #mostly ttbar in MuEl, don't smooth it that much, there's already high stat
    #Do the smoothing:
    for _ in range(nThrownPoints):
        x = ROOT.Double()
        y = ROOT.Double()
        f2.GetRandom2(x,y)
        #print f2.Eval(x,y), x, y
        h2_smoothed.Fill(x, y, w/nThrownPoints)

fileSuff = options.skimmedRootFileSuffix

#Set Axis title
h2.GetXaxis().SetTitle("m_{jj} [GeV]");
h2.GetYaxis().SetTitle("m_{lljj} [GeV]");
h2.GetXaxis().SetTitleOffset(1.2)
h2.GetYaxis().SetTitleOffset(1.6)

h2_smoothed.GetXaxis().SetTitle("m_{jj} [GeV]");
h2_smoothed.GetYaxis().SetTitle("m_{lljj} [GeV]");
h2_smoothed.GetXaxis().SetTitleOffset(1.2)
h2_smoothed.GetYaxis().SetTitleOffset(1.6)

#Give each sample the correct normalization:
# x_sec/SumEventWeights taken from Samadhi
#DY_M10-50
if "0" in fileSuff:
    h2.Scale(18610/2117047923870)
    h2_smoothed.Scale(18610/2117047923870)
#DY_0J
elif "1" in fileSuff:
    h2.Scale(4620.52/538466400170)
    h2_smoothed.Scale(4620.52/538466400170)
#DY_1J
elif "2" in fileSuff:
    h2.Scale(859.589/407544622836)
    h2_smoothed.Scale(859.589/407544622836)
    h2.SetTitle("DY+1jet - nominal")
    h2.SetDirectory(0)
    h2_smoothed.SetTitle("DY+1jet - smoothed")
    h2_smoothed.SetDirectory(0)
#DY_2J
elif "3" in fileSuff:
    h2.Scale(338.259/218758758380)
    h2_smoothed.Scale(338.259/218758758380)
#TT fully lept
elif "4" in fileSuff:
    h2.Scale(87.31/77215440)
    h2_smoothed.Scale(87.31/77215440)
#TT inclusive
elif "5" in fileSuff:
    h2.Scale(831.76/154384189.0)
    h2_smoothed.Scale(831.76/154384189.0)

print "non smoothed integral: ", h2.Integral()
print "smoothed integral: ", h2_smoothed.Integral()

c1.cd()
h2.SetMinimum(0)
h2.Draw("COLZ")
h2.SaveAs(outputDir+"non_smoothed_histo_FORTHESIS_{0}.root".format(options.skimmedRootFileSuffix.split('.')[0]))
c1.SaveAs(outputDir+"non_smoothed_histo_FORTHESIS_{0}.png".format(options.skimmedRootFileSuffix.split('.')[0]))
c1.SaveAs(outputDir+"non_smoothed_histo_FORTHESIS_{0}.pdf".format(options.skimmedRootFileSuffix.split('.')[0]))
del c1

c2.cd()
h2_smoothed.SetMinimum(0)
h2_smoothed.Draw("COLZ")
h2_smoothed.SaveAs(outputDir+"smoothed_histo_FORTHESIS_{0}.root".format(options.skimmedRootFileSuffix.split('.')[0]))
c2.SaveAs(outputDir+"smoothed_histo_FORTHESIS_{0}.png".format(options.skimmedRootFileSuffix.split('.')[0]))
c2.SaveAs(outputDir+"smoothed_histo_FORTHESIS_{0}.pdf".format(options.skimmedRootFileSuffix.split('.')[0]))
del c2

#FROM TH2 use: GetRandom2 (Double_t &x, Double_t &y) 15 times (for 15 toys).
#for i in range(n_events_MuMu_data):
#    h2_smoother.GetRandom2(Double_t &x, Double_t &y)

