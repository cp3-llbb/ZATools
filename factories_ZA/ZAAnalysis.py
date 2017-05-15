import os
import ROOT as R

#### Get all the indices and functions definitions needed to retrieve the IDs/... ####

pathCMS = os.getenv("CMSSW_BASE")
if pathCMS == "":
    raise Exception("CMS environment is not valid!")
pathZA = os.path.join(pathCMS, "src/cp3_llbb/ZAAnalysis/")
pathZAdefs = os.path.join(pathZA, "plugins/Indices.cc")

R.gROOT.ProcessLine(".L " + pathHHdefs + "+")
ZA =  R.ZAAnalysis
