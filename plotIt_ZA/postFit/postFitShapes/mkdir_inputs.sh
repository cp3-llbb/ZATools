#!/usr/bin/env bash

mass_points="MH-800_MA-200 MH-1000_MA-200 MH-800_MA-50 MH-500_MA-400 MH-800_MA-100 MH-650_MA-50 MH-250_MA-50 MH-1000_MA-50 MH-500_MA-50 MH-800_MA-400 MH-500_MA-300 MH-300_MA-100 MH-500_MA-200 MH-250_MA-100 MH-1000_MA-500 MH-300_MA-50 MH-800_MA-700 MH-200_MA-100 MH-200_MA-50 MH-300_MA-200 MH-500_MA-100"

flavors="MuMu ElEl MuEl"

for flavor in $flavors; do
  for mass_point in $mass_points; do
    mkdir -p $mass_point/$flavor
    cp /nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/ZAStatAnalysis/Cards_DYreweightingSplitIn9_sx1_MuEl_fakedata_fakeExcesses/ZA/postfit/fit/$mass_point/plotIt_$flavor/*root ./$mass_point/$flavor
  done
done
