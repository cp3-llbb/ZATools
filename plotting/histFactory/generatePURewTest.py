from cp3_llbb.ZATools.ZACnC import *

def printInJsonNoVar(f, g, obj, objName, cut, cutName, weights, binnings, isLastEntry):
    f.write( "        {\n")
    f.write( "        'name': '"+objName+"_"+cutName+"',\n")
    f.write( "        'variable': '"+obj+"',\n")
    f.write( "        'plot_cut': '"+cut+"',\n")
    f.write( "        'weight': '"+weights+"',\n")
    f.write( "        'binning': '"+binnings[0]+"'\n")
    if (isLastEntry == False) :
        f.write( "        },\n")
    if (isLastEntry == True) :
        f.write( "        }]\n")

    g.write("'"+objName+"_"+cutName+"':\n")
    g.write("  x-axis: '"+objName+"_"+cutName+"'\n")
    g.write("  y-axis: 'Evt'\n")
    g.write("  y-axis-format: '%1% / %2$.0f GeV'\n")
    g.write("  normalized: false\n")
    g.write("  log-y: both\n")
    g.write("  save-extensions: ['png','pdf']\n")
    g.write("  show-ratio: true\n")

def printInPyWithSyst(f, g, name = '', variable = '', cut = '', weight = '', binning = '', writeInPlotIt = 0):
    f.write( "        {\n")
    f.write( "        'name': '"+name+"',\n")
    f.write( "        'variable': '"+variable+"',\n")
    f.write( "        'plot_cut': '"+cut+"',\n")
    f.write( "        'weight': '"+weight+"',\n")
    f.write( "        'binning': '"+binning+"'\n")
    f.write( "        },\n")
    if writeInPlotIt == 1 :
      g.write("'"+name+"':\n")
      g.write("  x-axis: '"+name+"'\n")
      g.write("  y-axis: 'Evt'\n")
      g.write("  y-axis-format: '%1% / %2$.0f GeV'\n")
      g.write("  normalized: false\n")
      g.write("  log-y: both\n")
      g.write("  save-extensions: ['png','pdf']\n")
      g.write("  show-ratio: true\n")

def printInJson(f, g, obj, objName, variables, variableNames, cut, cutName, weights, binnings, isLastEntry):
    for i in range(0, len(variables)) :
        f.write( "        {\n")
        f.write( "        'name': '"+objName+"_"+variableNames[i]+"_"+cutName+"',\n")
        f.write( "        'variable': '"+obj+"."+variables[i]+"',\n")
        f.write( "        'plot_cut': '"+cut+"',\n")
        f.write( "        'weight': '"+weights+"',\n")
        f.write( "        'binning': '"+binnings[i]+"'\n")
        if (isLastEntry == False or i < len(variables)-1) : 
            f.write( "        },\n")
        else : 
            f.write( "        }\n")
    if (isLastEntry == True) :
        f.write( "        ]\n")

    for i in range(0, len(variables)) :
        g.write("'"+objName+"_"+variableNames[i]+"_"+cutName+"':\n")
        g.write("  x-axis: '"+objName+"_"+variableNames[i]+"_"+cutName+"'\n")
        g.write("  y-axis: 'Evt'\n")
        g.write("  y-axis-format: '%1% / %2$.0f GeV'\n")
        g.write("  normalized: false\n")
        g.write("  log-y: both\n")
        g.write("  save-extensions: ['png','pdf','root']\n")
        g.write("  show-ratio: true\n")

def printInPy(f, g, cut, cutName, weights, binning, isLastEntry):
    f.write( "        {\n")
    f.write( "        'name': '"+cutName+"',\n")
    f.write( "        'variable': '"+cut+"',\n")
    f.write( "        'plot_cut': '"+cut+"',\n")
    f.write( "        'weight': '"+weights+"',\n")
    f.write( "        'binning': '"+binning+"'\n")
    if (isLastEntry == False or i < len(variables)-1) :
        f.write( "        },\n")
    else :
        f.write( "        }\n")
    if (isLastEntry == True) :
        f.write( "        ]\n")

    g.write("'"+cutName+"':\n")
    g.write("  x-axis: '"+cutName+"'\n")
    g.write("  y-axis: 'Evt'\n")
    g.write("  y-axis-format: '%1% / %2$.0f GeV'\n")
    g.write("  normalized: false\n")
    g.write("  log-y: both\n")
    g.write("  save-extensions: ['png','pdf']\n")
    g.write("  show-ratio: true\n")


# binnings

nPV_binning = "(50,0,50)"

# PV N

nPV = "vertex_ndof.size()"
nPVName = "nVX"

# Cuts

weights = "event_pu_weight * event_weight"
weights_puup = "event_pu_weight_up * event_weight"
weights_pudown = "event_pu_weight_down * event_weight"

ll_weights = "( event_run < 200000 ? (za_diLeptons[0].triggerSF * event_pu_weight * event_weight) : 1.)"

twoLCond = []
twoLCondName = []
twoLCond.append("za_mumu_Mll_cut")
twoLCond.append("za_elel_Mll_cut")
twoLCond.append("(za_mumu_Mll_cut ||  za_elel_Mll_cut)")
twoLCond.append("(za_muel_Mll_cut ||  za_elmu_Mll_cut)")
twoLCondName.append("mm")
twoLCondName.append("ee")
twoLCondName.append("ll")
twoLCondName.append("me")

twoLtwoJCond = []
twoLtwoJCondName = []
twoLtwoBCond = []
twoLtwoBCondName = []
twoLthreeBCond = []
twoLthreeBCondName = []
twoLtwoSubJCond = []
twoLtwoSubJCondName = []
twoLOneBFatJetTCond = []
twoLOneBFatJetTCondName = []
twoLTwoBSubJetsLLCond = []
twoLTwoBSubJetsLLCondName = []
twoLTwoBSubJetsMMCond = []
twoLTwoBSubJetsMMCondName = []
twoLTwoBHighMassCond = []
twoLTwoBHighMassCondName = []

basicJcond="(elel_TwoJets_cut || mumu_TwoJets_cut || muel_TwoJets_cut || elmu_TwoJets_cut)"
basicTwoBcond="(Length$(za_diJets) > 0) && ((elel_TwoBjets_cut || mumu_TwoBjets_cut || muel_TwoBjets_cut || elmu_TwoBjets_cut) "
basicThreeBcond="(elel_ThreeBjets_cut || mumu_ThreeBjets_cut || muel_ThreeBjets_cut || elmu_ThreeBjets_cut)"
basicSubJcond="(elel_TwoSubJets_cut || mumu_TwoSubJets_cut || muel_TwoSubJets_cut || elmu_TwoSubJets_cut)"
basicOneBFatJetTcond="((elel_OneBFatJetT_cut || mumu_OneBFatJetT_cut || muel_OneBFatJetT_cut || elmu_OneBFatJetT_cut) && (Length$(za_diLepFatJets) > 0))"
#basicOneBFatJetTcond="(Length$(za_diLepFatJets) > 0)"
basicTwoBSubJetsLLcond="(elel_TwoBSubJetsLL_cut || mumu_TwoBSubJetsLL_cut )"
basicTwoBSubJetsMMcond="(elel_TwoSubJetsMM_cut || mumu_TwoSubJetsMM_cut || muel_TwoSubJetsMM_cut || elmu_TwoSubJetsMM_cut)"
basictwoLTwoBHighMasscond="(Length$(za_diJets) > 0 && Length$(za_diLeptons) > 0 && za_diJets[0].p4.Pt() > 200 && za_diLeptons[0].p4.Pt() > 200)"
basicJcondName="jj"
basicTwoBcondName="bb"
basicThreeBcondName="bbb"
basicSubJcondName="fj"
basicOneBFatJetTcondName="bfj"
basicTwoBSubJetsLLcondName="sbjsbj"
basictwoLTwoBHighMasscondName="highmass"

for x in range(0,4):
	twoLtwoJCond.append("("+twoLCond[x]+" && "+basicJcond+")")
	twoLtwoBCond.append("("+twoLCond[x]+" && "+basicTwoBcond+")")
	twoLthreeBCond.append("("+twoLCond[x]+" && "+basicThreeBcond+")")
	twoLtwoSubJCond.append("("+twoLCond[x]+" && "+basicSubJcond+")")
	twoLOneBFatJetTCond.append("("+twoLCond[x]+" && "+basicOneBFatJetTcond+")")
	twoLTwoBSubJetsLLCond.append("("+twoLCond[x]+" && "+basicTwoBSubJetsLLcond+")")
	twoLTwoBHighMassCond.append("("+twoLCond[x]+" && "+basictwoLTwoBHighMasscond+")")
	twoLtwoJCondName.append(twoLCondName[x]+basicJcondName)
	twoLtwoBCondName.append(twoLCondName[x]+basicTwoBcondName)
        twoLthreeBCondName.append(twoLCondName[x]+basicThreeBcondName)
	twoLtwoSubJCondName.append(twoLCondName[x]+basicSubJcondName)
	twoLOneBFatJetTCondName.append(twoLCondName[x]+basicOneBFatJetTcondName)
        twoLTwoBSubJetsLLCondName.append(twoLCondName[x]+basicTwoBcondName+basicTwoBSubJetsLLcondName)
	twoLTwoBHighMassCondName.append(twoLCondName[x]+basicTwoBcondName+basictwoLTwoBHighMasscondName)
	print twoLtwoJCond[x]


#test_highMass_cond = "(Length$(za_diJets) > 0 && Length$(za_diLeptons) > 0 && za_diJets[0].p4.Pt() > 200 && za_diLeptons[0].p4.Pt() > 200)"
#test_highMass =  twoL_cond + " * " + twoB_cond + " * " + test_highMass_cond + weights
#test_highMassName = "highPt"


# Writing the JSON

## 2 Muons 2 Jets :

fjson = open('plots_test.py', 'w')
fjson.write( "plots = [\n")
fyml = open('plots_test.yml', 'w')


llweights = {'': weights,
             '__puup': weights_puup,
             '__pudown': weights_pudown
    }

## Control Plots :

for x in range(0,4):
    for s,w in llweights.iteritems() : 
	print x, s, w 
	#printInJsonNoVar(fjson, fyml, nPV, nPVName, twoLCond[x]+weights, twoLCondName[x], nPV_binning, 0)
        printInPyWithSyst(fjson, fyml, name=nPVName+'_'+twoLCondName[x]+s, variable=nPV, cut=twoLCond[x], weight=w, binning=nPV_binning, writeInPlotIt= (1 if s==''  else 0))
        #printInPyWithSyst(f, g, name = '', variable = '', cut = '', weight = '', binning = '', isLastEntry=0):

fjson.write( "        ]\n")

'''
for line in fjson:
    pass
last = line
last.replace(',',']')
'''
