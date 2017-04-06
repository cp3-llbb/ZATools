#! /usr/bin/env python

import os, sys, argparse, math

# to prevent pyroot to hijack argparse we need to go around
tmpargv = sys.argv[:] 
sys.argv = []
# ROOT imports
from ROOT import gROOT, gSystem, PyConfig, TFile
gROOT.Reset()
gROOT.SetBatch()
PyConfig.IgnoreCommandLineOptions = True
sys.argv = tmpargv

def mapping(bkg):
    if bkg == "ttbar":
        return "TTTo2L2Nu_13TeV"
    elif bkg == "dy2":
        return "DYJetsToLL"
    elif bkg == "singletop":
        return "ST_"
    elif bkg == "ttV":
        return "TT(WJets|Z)To"
    elif bkg == "VV":
        return "(VV|ZZ)To"

def prettyName(bkg):
    if bkg == "ttbar":
        return "TT"
    elif bkg == "dy2":
        return "DY"
    elif bkg == "singletop":
        return "ST"
    elif bkg == "ttV":
        return "TT+V"
    elif bkg == "VV":
        return "VV"


parser = argparse.ArgumentParser(description='Compute data/MC scale factors from a MaxLikelihoodFit')

parser.add_argument('-i', '--input', action='store', type=str, dest='input', help='Path to the mlfit ROOT file created by combine', required=True)

options = parser.parse_args()

# Compute scale factors

mlfit = TFile.Open(options.input)

prefit_combine_norm = mlfit.Get('norm_prefit')
postfit_combine_norm = mlfit.Get('norm_fit_b')

channels = []
prefit_shapes = mlfit.Get('shapes_prefit')
for k in prefit_shapes.GetListOfKeys():
    channels.append(k.GetName())

print "Detected channels: ", channels


# Construct the list of backgrounds
# Naming is 'category/bkg_name'

backgrounds = []

all_backgrounds = prefit_combine_norm.contentsString().split(',')
for bkg in all_backgrounds:
    if not bkg.startswith(channels[0]):
        continue

    backgrounds.append(bkg.split('/')[-1])

print 'Detected backgrounds: ', backgrounds

prefit_norm = {}
postfit_norm = {}

for channel in channels:
    for bkg in backgrounds:
        name = channel + '/' + bkg

        prefit = prefit_combine_norm[name]
        postfit = postfit_combine_norm[name]

        if postfit.getVal() == 0 or prefit.getVal() == 0:
            continue

        if not bkg in prefit_norm:
            prefit_norm[bkg] = [prefit.getVal(), prefit.getError()**2]
            postfit_norm[bkg] = [postfit.getVal(), postfit.getError()**2]
        else:
            prefit_norm[bkg][0] += prefit.getVal()
            postfit_norm[bkg][0] += postfit.getVal()

            prefit_norm[bkg][1] += prefit.getError()**2
            postfit_norm[bkg][1] += postfit.getError()**2

scale_factors = {}
print ''
print 'Scale factors: '
for bkg in prefit_norm.keys():
    scale_factors[bkg] = postfit_norm[bkg][0] / prefit_norm[bkg][0]
    print('%s: %f' % (bkg, scale_factors[bkg]))

print("")

print 'Scale factors (for plotIt): '
for bkg, sf in scale_factors.items():
    if sf == 0:
        continue
    print("%s\n\tscale: %f" % (bkg, sf))


print("")
print("Relative post-fit uncertainties")
for bkg, values in postfit_norm.items():
    print "%s: %.4f" % (bkg, math.sqrt(values[1]) / values[0])

print("")
print("Post-fit uncertainties (for plotIt -- YAML)")

print("systematics:")

for bkg, values in postfit_norm.items():
    m = mapping(bkg)
    if not m:
        continue
    print("  - %s: {type: const, value: %.4f, on: '%s', pretty-name: '%s postfit'}" % (bkg + "_postfit", 1 + math.sqrt(values[1]) / values[0], m, prettyName(bkg)))
