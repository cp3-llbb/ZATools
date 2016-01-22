
import ROOT
import sys
#sys.path.insert(0,'/home/fynu/amertens/scratch/cmssw/CMSSW_7_4_15/src/cp3_llbb/CommonTools/histFactory/plots/ZAAnalysis')
from ZACnC import *

#### To be modified by the user

#luminosity
lumi = 1280.23

# directory where the files are located
dir_path = "/home/fynu/amertens/scratch/cmssw/CMSSW_7_4_15/src/cp3_llbb/CommonTools/histFactory/test_CnC/build/"

# write [name, file, xsec, gen events]
bkgFiles = [
  ['TT'      ,"TT_TuneCUETP8M1_13TeV-powheg-pythia8_MiniAODv2_v1.1.0+7415-6-g42bf8af_ZAAnalysis_2398776_histos.root", 831.76, 19757200.0],
  ["DY_10-50","DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX_MiniAODv2_v1.1.0+7415-6-g42bf8af_ZAAnalysis_2398776_histos.root",18610.0, 8.43221e+11],
  ["DY_50","DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX_MiniAODv2_v1.1.0+7415-6-g42bf8af_ZAAnalysis_2398776_histos.root", 6025.2, 432201000000]
]

dataFiles = [
  ['data','DoubleEG_Run2015D-05Oct2015-v1_2015-10-20_v1.1.0+7415-6-g42bf8af_ZAAnalysis_2398776_histos.root'],
  ['data','DoubleEG_Run2015D-PromptReco-v4_2015-10-20_v1.1.0+7415-6-g42bf8af_ZAAnalysis_2398776_histos.root'],
  ['data','DoubleMuon_Run2015D-05Oct2015-v1_2015-10-20_v1.1.0+7415-6-g42bf8af_ZAAnalysis_2398776_histos.root'],
  ['data','DoubleMuon_Run2015D-PromptReco-v4_2015-10-20_v1.1.0+7415-6-g42bf8af_ZAAnalysis_2398776_histos.root']
]

options = options_()

for cutkey in options.cut :
    var = cutkey
    
    #initializations
    totBkg=0
    observed = "-1"
    processes = ""
    yields = ""
    bins = ""
    order = ""
    i = 1
    signal = str("%.9f" % 1)+" "

    print 'var : ', var
    for file_idx in range(len(bkgFiles)) :
        file_path=dir_path+bkgFiles[file_idx][1]
        f=ROOT.TFile.Open(file_path)
        h = f.Get(var)
        Nev = int(h.Integral()) * lumi * bkgFiles[file_idx][2] / bkgFiles[file_idx][3]
        N = str("%.3f" % Nev)
        proc=bkgFiles[file_idx][0]
        print proc, 'expected events:', N
        processes += (15-len(proc))*" "+proc
        yields += (15-len(N))*" "+N
        bins += (15-1)*" "+"1"
        order += (15-len(str(i)))*" "+str(i)
        i += 1
        totBkg+=Nev

    totBkg_str = str("%.3f" %totBkg)
    observed=(15-len(totBkg_str))*" "+totBkg_str
    f = open("template.txt","r")
    newfile = f.read()
    newfile = newfile.replace("NCHANNELS",str(i-1)).replace("OBSERVED",observed).replace("SIGNAL",signal).replace("BINS",bins).replace("PROCESSES",processes).replace("ORDER",order).replace("YIELDS",yields)
    outfile = open("../cards/"+var+".txt","w")
    outfile.write(newfile)
    outfile.close()
 
