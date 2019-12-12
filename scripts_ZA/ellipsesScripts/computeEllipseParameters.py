#! /bin/env python

import sys, os, json
import getopt
import copy
import datetime
import subprocess
import numpy as np
import glob
import ROOT

import argparse


#Compute ellipse parameters for primary map for signal files.

#NOTA BENE: MH,MA       = SIMULATED MASSES
#           mllbb, mbb  = RECONSTRUCTED MASSES
global list_window
global list_histo
list_window = [] 
list_histo = [] 

def get_options():
    parser = argparse.ArgumentParser(description='Computes the ellipse parameters with or without centroid fit')
    parser.add_argument('-fit','--fit', action='store_true', required=False, default=False, 
                        help='If option used, the script will try to find the pol2 fit coefficients and use them to fix the centroid in the fit')
    parser.add_argument('-window','--window', action='store_true', required=False, default=False, 
                        help='If option used, the script will restrict the 2D fit to a window around the centroid (max peak or from the fit)')
    opt = parser.parse_args()
    return opt

def main():

    opt = get_options()

    path = "/home/ucl/cp3/fbury/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/"
    #signal_path = "/home/ucl/cp3/fbury/cp3_llbb/ZATools/factories_ZA/test_for_signal/slurm/output/"
    signal_path = "/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/factories_ZA/new2018prod_massHistosForEllParametrization/slurm/output/"
    categories = ["MuMu", "ElEl"]



    for cat in categories:
        print ("="*80)
        print (cat.center(10,' ').center(80,'*'))
        print ("="*80)
        result = []
        sigmas = []
        for inputfile in os.listdir(signal_path):
            if inputfile.startswith("HToZA") and inputfile.endswith(".root"):
                #Get the simulated masses: MA and MH
                splitPath = inputfile.split('/')
                filename = splitPath[-1]
                splitFilename = filename.replace('_', '-').split('-')

                #MH = int(splitFilename[2])
                #MA = int(splitFilename[4])
                MH = float(splitFilename[1].replace('p','.'))
                MA = float(splitFilename[2].replace('p','.'))
                print ("-"*80)
                print ('Config'.center(10,' ').center(80,'*'))
                print (('MH = '+str(MH)).center(80,' '))
                print (('MA = '+str(MA)).center(80,' '))
                print ("-"*80)
                print (filename)
                print (str(signal_path+inputfile))
                input = ROOT.TFile(signal_path+inputfile,"READ")
            
                histo2D = input.Get("Mjj_vs_Mlljj_{0}_hZA_lljj_deepCSV_btagM_mll_and_met_cut".format(cat))
                histo_mbb = input.Get("jj_M_{0}_hZA_lljj_deepCSV_btagM_mll_and_met_cut".format(cat))
                histo_mllbb = input.Get("lljj_M_{0}_hZA_lljj_deepCSV_btagM_mll_and_met_cut".format(cat))

                print ("-"*80)
                print ('mllbb'.center(10,' ').center(80,'*')) 
                (mllbb, width_llbb, PVal1, fit1) = getMassAndWidth(histo_mllbb, MH, cat='mH_'+cat, centroid='mllbb', use_fit=opt.fit)
                print ("mllbb: ", mllbb, " width_llbb: ", width_llbb, " PVal1: ", PVal1)
                print ("-"*80)
                print ('mbb'.center(10,' ').center(80,'*')) 
                (mbb, width_bb, PVal2, fit2) = getMassAndWidth(histo_mbb, MA, cat='mA_'+cat, centroid='mbb', use_fit=opt.fit)
                print ("mbb: ", mbb, " width_bb: ", width_bb, " PVal2: ", PVal2)
                print ("-"*80)

                
                (a, b, theta) = getEllipseParameters(histo2D,(mbb,mllbb),(MA,MH),sample=cat,use_window=opt.window)

                if MH <= 1000:
                    result.append((mbb, mllbb, a, b, theta, MA, MH))
                    sigmas.append((mbb, mllbb, width_bb, width_llbb))


                json_name_f = path+'fullEllipseParam_{0}.json'.format(cat)
                json_name_f1 = path+'fullSigmas_{0}.json'.format(cat)
                if opt.fit: 
                    json_name_f = json_name_f.replace('EllipseParam','EllipseParamFit')
                    json_name_f1 = json_name_f1.replace('Sigmas','SigmasFit')
                if opt.window:
                    json_name_f = json_name_f.replace('EllipseParam','EllipseParamWindow')
                    json_name_f1 = json_name_f1.replace('Sigmas','SigmasWindow')

                f = open(json_name_f, 'w')   # file containing the reconstructed and the simulated masses + the ellipse parameters
                f1 = open(json_name_f1, 'w')   # file containing the reconstructed masses and the respective sigmas
                json.dump(result, f)
                json.dump(sigmas, f1)
                f.close()
                f1.close()
                

    # save window plot #
    if opt.window:
        ROOT.gStyle.SetOptStat(0)
        root_window = ROOT.TFile("window.root","RECREATE")
        c1 = ROOT.TCanvas()
        pad1 = ROOT.TPad( 'pad1', 'window', 0.03, 0.10, 0.50, 0.85)
        pad2 = ROOT.TPad( 'pad2', 'full', 0.53, 0.10, 0.98, 0.85)
        pad1.Draw()
        pad2.Draw()
        ROOT.SetOwnership(c1, False) # otherwise pyroot crashes, needed for the garbage collector
        ROOT.SetOwnership(pad1, False)
        ROOT.SetOwnership(pad2, False)

        c1.SaveAs("window.pdf[")
        for win,hist in zip(list_window,list_histo):
            win.Write()
            pad1.cd()
            win.Draw('COLZ')
            pad2.cd()
            hist.Draw("COLZ")
            c1.SaveAs("window.pdf")
        c1.SaveAs("window.pdf]")

def getSubHist(histo,centroid,mass,sample):
    
    # Define new histogram #
    x_axis = histo.GetXaxis()
    y_axis = histo.GetYaxis()
    n_bin_x = histo.GetNbinsX()
    n_bin_y = histo.GetNbinsY()
    x_max = x_axis.GetBinLowEdge(n_bin_x)
    y_max = y_axis.GetBinLowEdge(n_bin_y)
    name = '%s_MH_=_%0.2f,_MA_=_%0.2f'%(sample,mass[1],mass[0])
    new_histo = ROOT.TH2F(name,name,n_bin_x,0,x_max,n_bin_y,0,y_max)
    
    # Fill only events into the window #
    width = 0.5
    x_bin_low_window = x_axis.FindBin((1-width)*centroid[0])
    x_bin_high_window = x_axis.FindBin((1+width)*centroid[0])
    y_bin_low_window = y_axis.FindBin((1-width)*centroid[1])
    y_bin_high_window = y_axis.FindBin((1+width)*centroid[1])
    for x in range(1,histo.GetNbinsX() + 1):            # Loop over bins in x axis
        for y in range(1,histo.GetNbinsY() + 1):        # Loop over bins in y axis
            x_val = x_axis.GetBinLowEdge(x)
            y_val = y_axis.GetBinLowEdge(y)
            z_val = histo.GetBinContent(x,y)
            if x<x_bin_low_window or x>x_bin_high_window:
                continue
            if y<y_bin_low_window or y>y_bin_high_window:
                continue
            new_histo.Fill(x_val,y_val,z_val)
    new_histo.Draw()
    new_histo.SetTitle(name.replace('_',' '))
    new_histo.GetXaxis().SetRangeUser(0,1.4*mass[1])
    new_histo.GetYaxis().SetRangeUser(0,1.4*mass[1])
    histo.Draw()
    histo.GetXaxis().SetRangeUser(0,1.4*mass[1])
    histo.GetYaxis().SetRangeUser(0,1.4*mass[1])
    list_window.append(copy.deepcopy(new_histo))
    list_histo.append(copy.deepcopy(histo))
    return new_histo


def getEllipseParameters(histo,centroid,mass,sample,use_window):
    # Reduce the histo to a window around the centroid #
    if use_window: 
        histo = getSubHist(histo,centroid,mass,sample)

    NBrectangle=histo.GetEntries()

    # build the covariance matrix
    m = ROOT.TMatrixDSym(2)
    m[0,0] = histo.GetCovariance(1,1)
    m[1,1] = histo.GetCovariance(2,2)
    m[0,1] = histo.GetCovariance(1,2)
    m[1,0] = histo.GetCovariance(2,1)

    # compute eigen values and eigen vectors
    me = ROOT.TMatrixDSymEigen(m)
    eigenval = me.GetEigenValues()
    eigenvec = me.GetEigenVectors()

    # get the ellipses parameters
    a = eigenval[0]
    b = eigenval[1]
    theta = ROOT.TMath.ACos(eigenvec[0][0])
    
    # return the result
    return (a, b, theta)


def getMassAndWidth(massHisto, mass, cat, centroid, use_fit=False):

    # find the maximum and determine the window
    maximumBin = massHisto.GetMaximumBin()
    print ("maximumBin without fit: ", maximumBin)
    massPeak   = massHisto.GetBinLowEdge(maximumBin)
    print ("massPeak without fit : ", massPeak)
    maximum    = massHisto.GetMaximum()
    print ("maximum: ", maximum)
    if use_fit:
        order = 1
        def func_fit(x,p,m):
            return (1-(2/(1+np.exp(-x/m))-1)*(1-p))*x
        try:
            #coeff = np.loadtxt('pol'+str(order)+'_fit_'+cat+'.txt')
            #p = np.poly1d(coeff)
            #massPeak = p(mass)
            coeff = np.loadtxt('weird_fit_'+cat+'.txt')
            massPeak = func_fit(mass,coeff[0],coeff[1])
        except:
            print ('[ERROR] No coeff file '+'pol'+str(order)+'_fit_'+cat+'.txt found for the pol2 fit')
            print ('Maybe you should use centroidExtrapolation.py first')
            sys.exit()
        maximumBin = massHisto.FindBin(massPeak)
        maximum = massHisto.GetBinContent(maximumBin)
        print ("maximumBin according to fit: ", maximumBin)
        print ("massPeak according to fit: ", massPeak)
        print ("maximum according to fit: ", maximum)
    
    halfWidth  = int(0.50*mass)
    if centroid == 'mllbb':
        if mass<700:
            halfWidth  = int(0.50*mass)
        else:
            halfWidth  = int(0.30*mass)
    print ("halfWidth: ", halfWidth)

    lowMassFit = max(massPeak-halfWidth,0) 
    highMassFit = min(massPeak+halfWidth,massHisto.GetBinLowEdge(massHisto.GetSize()-2))

    print ("lowMassFit : %0.2f"%(lowMassFit))
    print ("highMassFit : %0.2f"%(highMassFit))
    # perform the fit
    fit_gauss = ROOT.TF1('fit','gaus',lowMassFit,highMassFit)
    fit_gauss.SetParameters(maximum,massPeak,halfWidth)
    fit_gauss.SetParNames("norm","centroid","width");
    if use_fit:
        fit_gauss.FixParameter(1,massPeak) # fix the centroid from the fit 
    result_fit = massHisto.Fit("fit","RSB0","",lowMassFit,highMassFit)	# print the parameters
    fit = massHisto.GetFunction("fit")

    if result_fit.IsValid():
        chi2 = result_fit.Chi2()
        ndf = result_fit.Ndf()
        pvalue = ROOT.TMath.Prob(chi2,ndf)
        m_reco = fit.GetParameter(1)      #mu
        sigma = fit.GetParameter(2)       #sigma
    else:
        pvalue = -1
        if use_fit:
            m_reco = massPeak
        else:
            m_reco = 0    
        sigma = 0
    massHisto.SetTitle("MH=800 GeV, MA=100GeV")
    if "lljj_M" in massHisto.GetName():
        massHisto.GetXaxis().SetTitle("mlljj (GeV)")
    else: 
        print massHisto.GetName()
        massHisto.GetXaxis().SetTitle("mjj (GeV)")
    c = ROOT.TCanvas("c", "c", 800,600)
    massHisto.Draw()
    c.SaveAs("{0}.pdf".format(massHisto.GetName()))
    c.SaveAs("{0}.png".format(massHisto.GetName()))
    del c

    # return the result
    return (m_reco, sigma, pvalue, fit)



if __name__ == "__main__":
    #main(sys.argv[1:])
    main()



