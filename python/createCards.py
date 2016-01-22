#! /usr/bin/env python

# Python imports
#import os, sys, argparse, getpass
from datetime import datetime
# User imports
from classes import *
import CombineHarvester.CombineTools.ch as ch
# ROOT imports
import ROOT
from ROOT import gROOT
from ROOT import TChain, TFile, TCanvas
#gROOT.Reset()
#gROOT.SetBatch()
#ROOT.PyConfig.IgnoreCommandLineOptions = True



def main():
    """Main function"""
    # start the timer
    tstart = datetime.now()
    print 'starting...'
    # get the options
    #options = get_options()

    intL = 2245.792 # in pb-1    
    tag = 'v1.1.0+7415-23-g22d44c6_ZAAnalysis_919cd18'
    path = '/nfs/scratch/fynu/amertens/cmssw/CMSSW_7_4_15/src/cp3_llbb/CommonTools/histFactory/16_01_21/build'
    CHANNEL = 'mumu'
    ERA = '13TeV'
    MASS = '90'
    ANALYSIS = 'HtoZAtoLLBB'
    DEBUG = 0

    c = ch.CombineHarvester()
    cats = [(0, 'SR'),
            (1, 'll_M_CR')
            ]

    bins = {}
    bins['signalregion'] = 'SR'
    bins['mll_bkgregion'] = 'll_M_CR'

    processes = {}
    p = Process('data_obs')
    p.prepare_process(path, 'data_obs', 'DoubleMuon_Run2015D-PromptReco-v4_2015-10-20', tag)
    processes['data_obs'] = p
    if DEBUG: print p
    # define signal
    p = Process('zz')
    p.prepare_process(path, 'zz', 'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8_MiniAODv2', tag)
    processes['zz'] = p
    if DEBUG: print p
    # define backgrounds
    # ttbar
    p = Process('ttbar')
    p.prepare_process(path, 'ttbar', 'TTTo2L2Nu_13TeV-powheg_MiniAODv2', tag)
    processes['ttbar'] = p
    p = Process('ttbar')
    if DEBUG: print p
    # drell-yan
    p = Process('dy1')
    p.prepare_process(path, 'dy1', 'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX_MiniAODv2', tag)
    processes['dy1'] = p
    if DEBUG: print p
    p = Process('dy2')
    p.prepare_process(path, 'dy2', 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX_MiniAODv2', tag)
    processes['dy2'] = p
    if DEBUG: print p




    c.AddObservations([MASS], [ANALYSIS], [ERA], [CHANNEL], cats)
    c.AddProcesses([MASS], [ANALYSIS], [ERA], [CHANNEL], ['zz'], cats, True)
    c.AddProcesses([MASS], [ANALYSIS], [ERA], [CHANNEL], ['ttbar', 'dy1', 'dy2'], cats, False)
    c.cp().process(['ttbar', 'dy1', 'dy2', 'zz']).AddSyst(
        c, "lumi", "lnN", ch.SystMap('channel', 'era', 'bin_id')
        ([CHANNEL], [ERA],  [0,1,2,3], 1.046))

    nChannels = len(bins)
    nBackgrounds = len([processes[x] for x in processes if processes[x].type > 0])
    nNuisances = 1


    outputRoot = "shapes.root"
    f = TFile(outputRoot, "recreate")
    f.Close()
    for b in bins:
        print bins[b]
        for p in processes:
            print processes[p]
            #hname = "hist_%s_%s" % (b, p)
            #chain = TChain("t")
            #chain.Add(processes[p].file)
            #chain.Draw("jj_M>>%s(60,0,600)" % hname, "((%s) && (%s))" % (cleaningCut, bins[b]))
            file_in = TFile(processes[p].file,"READ")
            h = file_in.Get(bins[b])
            h.SetDirectory(0)
            file_in.Close()
            f = TFile(outputRoot, "update")
            h.SetName("hist_"+bins[b]+"_"+p)
#           print processes[p].xsection * intL / processes[p].sumW
            if p == 'data_obs' :
                h.Write()
            else :
                h.Sumw2()
                h.Scale(processes[p].xsection * intL / processes[p].sumW)
                h.Write()
            f.Write()
            f.Close()

    c.cp().backgrounds().ExtractShapes(
        outputRoot, "hist_$BIN_$PROCESS", "hist_$BIN_$PROCESS_$SYSTEMATIC")
    c.cp().signals().ExtractShapes(
        outputRoot, "hist_$BIN_$PROCESS", "hist_$BIN_$PROCESS_$SYSTEMATIC")
    writer = ch.CardWriter('$TAG/$MASS/$ANALYSIS_$CHANNEL_$ERA.dat',
                   '$TAG/common/$ANALYSIS_$CHANNEL_$MASS.input_$ERA.root')
    writer.WriteCards('CARDS/', c)

#
# main
#
if __name__ == '__main__':
    main()
