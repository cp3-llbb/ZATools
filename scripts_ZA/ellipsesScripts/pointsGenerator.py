#! /bin/env python

from math import sqrt,atan,cos
import ROOT
from array import array
import json
import sys
import os
import numpy as np
import cutWindow

import matplotlib as ml
ml.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc

import time
timestr = time.strftime("%Y%m%d-%H%M%S")

# Global parameters
step_x   = 1.0
step_y   = 1.0
filename  = "/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/ellipseParam_MuMu.json"
sigma_file = "/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/sigmas_MuMu.json"


def get_a2_b2_theta(mbb, mllbb):
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

    return a2_value, b2_value, theta_value

def Points():
    points = []

    #load sigma parameters
    with open(sigma_file) as f1:
        data = json.load(f1)
    sigx = ROOT.TGraph2D(len(data))
    sigx.SetName("sigx")
    sigy = ROOT.TGraph2D(len(data))
    sigy.SetName("sigy")

    for i,s in enumerate(data):
        if float(s[0]) == 0 or float(s[1]) == 0: continue
        #print s[0], s[1], s[2]/s[0], s[3]/s[1]
        #Assume a resolution of 20%
        sigx.SetPoint(i,s[0],s[1],float(s[2])/float(s[0]))  #mbb, mllbb, res_bb=sigma_bb/mbb
        sigy.SetPoint(i,s[0],s[1],float(s[3])/float(s[1]))  #mbb, mllbb, res_llbb=sigma_llbb/mllbb

    # Creation of the pavement
    mA_min = 30
    mA = mA_min
    mH = 132
    sigmaY = 0.1
    sigmaX = 0.1
    while mH < 1000:
        while mA <= (mH-90):
            points.append((mA,mH))
            sigmaX = sigx.Interpolate(mA,mH)
            if sigmaX == 0:
                distance = 1000
                for (m1,m2,s1,s2) in data:
                    if m1 == 0 or m2 == 0: continue
                    d = sqrt((m1-mA)**2+(m2-mH)**2)
                    if d < distance:
                        distance = d
                        sigmaX = s1/m1
            mA = mA*(1+sigmaX*step_x) 
            sigmaY = sigy.Interpolate(mA,mH)
            if sigmaY == 0:
                distance =1000
                for (m1,m2,s1,s2) in data:
                    if m1 == 0 or m2 == 0: continue
                    d = sqrt((m1-mA)**2+(m2-mH)**2)
                    if d < distance:
                        distance = d
                        sigmaY = s2/m2
        mH = mH*(1+sigmaY*step_y) 
        mA = mA_min 

    # Save points
    #print "Number of ellipses: ", len(points)
    f2 = open('points_%f_%f_%s.json'%(round(step_x, 1), round(step_y, 1), timestr), 'w')
    str_stepx = str(round(step_x, 2))
    str_stepx = str_stepx.replace('.', 'p')
    str_stepy = str(round(step_y, 2))
    str_stepy = str_stepy.replace('.', 'p')
    json.dump(points,f2)
    f2.close()
    return points

# control plots: draw the centers
def Control(points):
    canvas = ROOT.TCanvas("canvas","ellipse pavement, step_x = %f, step_y = %f"%(step_x, step_y),200,10,700,500)
    line = ROOT.TLine(0,90,910,1000);
    line.SetLineColor(ROOT.kRed);
    line.SetLineWidth(2)
    hpx = ROOT.TH2F("hpx","MC production points",len(points),0,1000,len(points),0,1000);
    hpx.SetStats(ROOT.kFALSE);   # no statistics
    hpx.GetXaxis().SetTitle("mA (GeV)")
    hpx.GetYaxis().SetTitle("mH (GeV)")

    #print "Number of centers: ", len(points)
    centers = ROOT.TGraph(len(points))
    for i,(mA,mH) in enumerate(points):
        centers.SetPoint(i,mA,mH)
    hpx.Draw();
    line.Draw();
    centers.Draw("p")
    canvas.Update()
    str_stepx = str(round(step_x, 2))
    str_stepx = str_stepx.replace('.', 'p')
    str_stepy = str(round(step_y, 2))
    str_stepy = str_stepy.replace('.', 'p')
    #canvas.SaveAs("control_points_{0}_{1}_{2}.root".format(str_stepx, str_stepy, timestr))
    #canvas.SaveAs("control_points_{0}_{1}_{2}.pdf".format(str_stepx, str_stepy, timestr))
    fig = plt.figure(figsize=(20,20))
    #plt.rcParams['font.family'] = 'sans-serif'
    #plt.rcParams['font.sans-serif'] = 'Arial'
    rc('font',**{'family':'sans-serif','sans-serif':['Arial']})
    rc('text', usetex=True)
    params = {'text.usetex': False, 'mathtext.fontset': 'stixsans'}
    plt.rcParams.update(params)

    mA_list = []
    mH_list = []
    for (x,y) in points:
        mA_list.append(x)
        mH_list.append(y)
    mA_list = np.asarray(mA_list)
    mH_list = np.asarray(mH_list)
    plt.scatter(mA_list, mH_list, marker='o', color='blue', s=90)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.xlabel(r'$\mathrm{m}_{\mathrm{A}}$ [GeV]', fontsize=60)
    plt.ylabel(r'$\mathrm{m}_{\mathrm{H}}$ [GeV]', fontsize=60)
    plt.ylim(0,1050)
    plt.xlim(0,1000)
    plt.show()
    fig.tight_layout()
    fig.savefig("control_points_{0}_{1}_{2}_matplotlib.pdf".format(str_stepx, str_stepy, timestr))

# draw ellipses
#def ellipse(points,w,rho):
#    c = ROOT.TCanvas("c","ellipse pavement",500,500)
#    c.hpx = ROOT.TH2F("hpx","Ellipse pavement control",100,0,1000,100,0,1000);
#    c.hpx.GetXaxis().SetTitle("mA GeV")
#    c.hpx.GetYaxis().SetTitle("mH GeV")
#    c.hpx.Draw()
#    c.e =[]
#    for i,center in enumerate(points):
#        x = center[0]
#        y = center[1]
        #(a,b,t) = w.getParameters(x,y)
#        M11 = w.getValue(0,0, [x,y])
#        M12 = w.getValue(0,1, [x,y])
#        M22 = w.getValue(1,1, [x,y])
#        t = atan(M12/M11)
#        a = cos(t)/M11
#        b = cos(t)/M22
#        theta = t * 57.29
#        c.e.append(ROOT.TEllipse(x,y,a*rho,b*rho,0,360,theta))
#        c.e[i].Draw("same")
#    c.Update()
#    c.Draw()
#    c.SaveAs("test.root")


#main
if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    window = cutWindow.massWindow(filename)
    points = Points()
    control = Control(points)
    #ellipse(points,window,rho)

