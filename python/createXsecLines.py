#!/usr/bin/python


import math
from cp3_llbb.Calculators42HDM.Calc2HDM import *
from ROOT import *


mode = 'H'
sqrts = 13000
type = 2
tb = 1
m12 = 0
mh = 125
mH = 300
mA = 50
mhc = mH

beta=math.atan(tb)
cba = 0.01
alpha=math.atan(tb)-math.acos(cba)
sba = math.sin(math.atan(tb)-alpha)

print 'sba : ', sba

outputFile = "out.dat"


test = Calc2HDM(mode = 'H', sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sba, outputFile = outputFile)
test.computeBR()

xsec =  test.getXsecFromSusHi()

xsectot_list = []


Xsec_mH500_tb1 = TGraph(50)

n=0

while mA < mH-90:
    test.setmA(mA)
    test.computeBR()
    print "ZA BR", test.HtoZABR
    Xsec_mH500_tb1.SetPoint(n,mA,xsec*test.HtoZABR*test.AtobbBR*0.067)
    mA+=2
    n+=1



file_out = TFile("xsec.root","RECREATE")
Xsec_mH500_tb1.Write()

