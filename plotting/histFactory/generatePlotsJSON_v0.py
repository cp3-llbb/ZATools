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

pt_binning  = "(30, 0, 600)"
eta_binning = "(30, -3, 3)"
phi_binning = "(30, -3.1416, 3.1416)"
lepiso_binning = "(30, 0, 0.3)"
dca_binning = "(50, -5.0, 5.0)"
mj_binning = "(30, 0, 30)"
csv_binning = "(20,0,1)"
DR_binning = "(15, 0, 6)"
DPhi_binning = "(10, 0, 3.1416)"
ptZ_binning = "(80,0,800)"
MZ_binning = "(80,0,400)"
MZzoomed_binning = "(60,60,120)"
Mjj_binning = "(30,0,600)"
Mlljj_binning = "(40,0,2400)"
met_binning = "(40,0,400)"
Nj_binning = "(8,0,8)"
nPV_binning = "(50,0,50)"
fj_mass_binning = "(20,0,400)"
tau_binning = "(10,0,1)"
subjetDR_binning = "(20,0,1)"


# Leptons variables

l1 = "za_dilep_ptOrdered[0]"
l2 = "za_dilep_ptOrdered[1]"

l1Name = "lep_pt1"
l2Name = "lep_pt2"

l_var = ["p4.Pt()", "p4.Eta()", "p4.Phi()", "isoValue","dca"]
l_varName = ["Pt", "Eta", "Phi", "isoValue","dca"]

l_binning = [pt_binning, eta_binning, phi_binning, lepiso_binning,dca_binning]

# Jets variables

j1pt = "za_dijet_ptOrdered[0]"
j2pt = "za_dijet_ptOrdered[1]"
j1csv = "za_dijet_CSVv2Ordered[0]"
j2csv = "za_dijet_CSVv2Ordered[1]"

j1ptName = "jet_pt1"
j2ptName = "jet_pt2"
j1csvName = "jet_CSV1"
j2csvName = "jet_CSV2"

j_var = ["p4.Pt()", "p4.Eta()", "p4.Phi()", "p4.M()", "CSVv2", "minDRjl" ]
j_varName = ["Pt", "Eta", "Phi", "M", "CSVv2", "minDRjl"]
j_binning = [pt_binning, eta_binning, phi_binning, mj_binning, csv_binning, DR_binning]

# FAT jets

fj = "za_selFatJets[0]"
fjName = "fat-Jet"

fj_var = ["softdrop_mass","trimmed_mass","pruned_mass","filtered_mass","tau1","tau2","tau3","subjetDR"]
fj_varName = ["softdrop_mass","trimmed_mass","pruned_mass","filtered_mass","tau1","tau2","tau3","subjetDR"]

fj_binning = [fj_mass_binning,fj_mass_binning,fj_mass_binning,fj_mass_binning,tau_binning,tau_binning,tau_binning,subjetDR_binning]

# MET variables

met = "met_p4"
metName = "met"

met_var = ["Pt()"]
met_varName = ["Pt"]
met_binning = [met_binning]
# Dilep variables

dilep = "za_diLeptons[0]"
dilepName = "ll"
dilep_var = ["p4.Pt()", "p4.Eta()", "p4.Phi()", "p4.M()","p4.M()", "DR", "DEta", "DPhi"]
dilep_varName = ["Pt", "Eta", "Phi", "M", "M", "DR", "DEta", "DPhi"]
dilep_binning = [ptZ_binning, eta_binning, phi_binning, MZ_binning, MZzoomed_binning, DR_binning, DR_binning, DPhi_binning]

# Dijet variables

dijet = "za_diJets[0]"
dijetName = "jj"
dijet_var = ["p4.Pt()", "p4.Eta()", "p4.Phi()", "p4.M()", "DR", "DEta", "DPhi"]
dijet_varName = ["Pt", "Eta", "Phi", "M", "DR", "DEta", "DPhi"]
dijet_binning = [ptZ_binning, eta_binning, phi_binning, Mjj_binning, DR_binning, DR_binning, DPhi_binning]

# Dilep-Dijet variables

dijetdilep = "za_diLepDiJets[0]"
dijetdilepName = "lljj"
dijetdilep_var = ["p4.Pt()", "p4.Eta()", "p4.Phi()", "p4.M()"]
dijetdilep_varName = ["Pt", "Eta", "Phi", "M"]
dijetdilep_binning = [pt_binning, eta_binning, phi_binning, Mlljj_binning]

# Dilep_fatjet variables

dilepFatjet = "za_diLepFatJets[0]"
dilepFatjetName = "llj"
dilepFatjet_var = ["p4.M()", "p4.Eta()", "p4.Phi()", "p4.M()"]
dilepFatjet_varName = ["M", "Eta", "Phi", "M"]
dilepFatjet_binning = [Mlljj_binning, pt_binning, eta_binning, phi_binning, Mlljj_binning]

# (B-)Jets Counting

selJets = "za_selJets"
selJetsName = "jets"
selJets_var = ["size()"]
selJets_varName = ["N"]
selJets_binning = [Nj_binning]

selBjets = "za_selBjetsM"
selBjetsName = "BjetsM"

# PV N

nPV = "vertex_ndof.size()"
nPVName = "nVX"
nPV_binning = [nPV_binning]

# Cuts

ERewID = "1" # " * (electron_sf_id_loose[za_diLeptons[0].idxLep1][0]*electron_sf_id_loose[za_diLeptons[0].idxLep2][0])"
MRewID = "1" #" * (muon_sf_id_loose[za_diLeptons[0].idxLep1][0]*muon_sf_id_loose[za_diLeptons[0].idxLep2][0])"
MRewIso = "1" #" * (muon_sf_iso_02_loose[za_diLeptons[0].idxLep1][0]*muon_sf_iso_02_loose[za_diLeptons[0].idxLep2][0])"

twoCSVV2_medium_SF_weight = " (jet_sf_csvv2_medium[za_diJets[0].idxJet1][0] * jet_sf_csvv2_medium[za_diJets[0].idxJet2][0] )"

ll_weights = "(event_is_data !=1 ?( za_diLeptons[0].triggerSF * event_pu_weight * event_weight * za_diLeptons[0].triggerMatched) : 1.0)"

twoLCond = []
twoLCondName = []
twoLCond.append("(za_mumu_Mll_cut  && (za_mumu_fire_trigger_Mu17_Mu8_cut || za_mumu_fire_trigger_Mu17_TkMu8_cut || za_mumu_fire_trigger_IsoMu27_cut) && za_diLeptons[0].isMM)")
twoLCond.append("(za_elel_Mll_cut && za_elel_fire_trigger_Ele17_Mu12_cut && za_diLeptons[0].isTT)")
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

basicJcond="(za_elel_TwoJets_cut || za_mumu_TwoJets_cut || za_muel_TwoJets_cut || za_elmu_TwoJets_cut)"
basicTwoBcond="(Length$(za_diJets) > 0) && (za_elel_TwoBjets_cut || za_mumu_TwoBjets_cut || za_muel_TwoBjets_cut || za_elmu_TwoBjets_cut) "
basicThreeBcond="(za_elel_ThreeBjets_cut || za_mumu_ThreeBjets_cut || za_muel_ThreeBjets_cut || za_elmu_ThreeBjets_cut)"
basicSubJcond="(za_elel_TwoSubJets_cut || za_mumu_TwoSubJets_cut || za_muel_TwoSubJets_cut || za_elmu_TwoSubJets_cut)"
basicOneBFatJetTcond="((za_elel_OneBFatJetT_cut || za_mumu_OneBFatJetT_cut || za_muel_OneBFatJetT_cut || za_elmu_OneBFatJetT_cut) && (Length$(za_diLepFatJets) > 0))"
#basicOneBFatJetTcond="(Length$(za_diLepFatJets) > 0)"
basicTwoBSubJetsLLcond="(za_elel_TwoBSubJetsLL_cut || za_mumu_TwoBSubJetsLL_cut )"
basicTwoBSubJetsMMcond="(za_elel_TwoSubJetsMM_cut || za_mumu_TwoSubJetsMM_cut || za_muel_TwoSubJetsMM_cut || za_elmu_TwoSubJetsMM_cut)"
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


# Writing the JSON

## 2 Muons 2 Jets :

fjson = open('plots_all.py', 'w')
fjson.write( "plots = [\n")
fyml = open('plots_all.yml', 'w')


## CandCount variables :

options = options_()


#printInPy(fjson, fyml, " ( Length$(za_diJets) > 0 && TMath::Abs(za_diJets[0].p4.M()-90) < 30) && "+twoLtwoBCond[0]+" )", "SR" , ll_weights ,"(2, 0, 2)", 0)
#printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, "( Length$(za_diJets) > 0 && TMath::Abs(za_diJets[0].p4.M()-90) > 30) && "+twoLtwoBCond[0]+" )", "CR", ll_weights, dilep_binning, 1)

## Control Plots :


# 1) 2L stage


for x in range(0,1):
	print x
       
	printInJson(fjson, fyml, l1, l1Name, l_var, l_varName, twoLCond[x], twoLCondName[x], ll_weights, l_binning, 0)
	printInJson(fjson, fyml, l2, l2Name, l_var, l_varName, twoLCond[x], twoLCondName[x], ll_weights, l_binning, 0)
	printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, twoLCond[x], twoLCondName[x], ll_weights , dilep_binning, 0)
	printInJson(fjson, fyml, selJets, selJetsName, selJets_var, selJets_varName, twoLCond[x], twoLCondName[x],ll_weights, selJets_binning, 0)
	printInJson(fjson, fyml, selBjets, selBjetsName, selJets_var, selJets_varName, twoLCond[x], twoLCondName[x],ll_weights, selJets_binning, 0)
	printInJsonNoVar(fjson, fyml, nPV, nPVName, twoLCond[x], twoLCondName[x],ll_weights, nPV_binning, 0)
        
	# 2L2J
	printInJson(fjson, fyml, l1, l1Name, l_var, l_varName, twoLtwoJCond[x], twoLtwoJCondName[x],ll_weights, l_binning, 0)
	printInJson(fjson, fyml, l2, l2Name, l_var, l_varName, twoLtwoJCond[x], twoLtwoJCondName[x],ll_weights, l_binning, 0)
	printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, twoLtwoJCond[x], twoLtwoJCondName[x],ll_weights, dilep_binning, 0)
	printInJson(fjson, fyml, selJets, selJetsName, selJets_var, selJets_varName, twoLtwoJCond[x], twoLtwoJCondName[x],ll_weights, selJets_binning, 0)
	printInJson(fjson, fyml, selBjets, selBjetsName, selJets_var, selJets_varName, twoLtwoJCond[x], twoLtwoJCondName[x],ll_weights, selJets_binning, 0)
	printInJson(fjson, fyml, j1pt, j1ptName, j_var, j_varName, twoLtwoJCond[x], twoLtwoJCondName[x], ll_weights,j_binning,0)
	printInJson(fjson, fyml, j2pt, j2ptName, j_var, j_varName, twoLtwoJCond[x], twoLtwoJCondName[x], ll_weights,j_binning,0)
	# 2L2B
	printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, twoLtwoBCond[x], twoLtwoBCondName[x], ll_weights+"*"+twoCSVV2_medium_SF_weight, dilep_binning, 0)
	printInJson(fjson, fyml, j1pt, j1ptName, j_var, j_varName, twoLtwoBCond[x], twoLtwoBCondName[x],ll_weights+"*"+twoCSVV2_medium_SF_weight, j_binning, 0)
	printInJson(fjson, fyml, j2pt, j2ptName, j_var, j_varName, twoLtwoBCond[x], twoLtwoBCondName[x],ll_weights+"*"+twoCSVV2_medium_SF_weight, j_binning, 0)
	printInJson(fjson, fyml, dijet, dijetName, dijet_var, dijet_varName, twoLtwoBCond[x], twoLtwoBCondName[x],ll_weights+"*"+twoCSVV2_medium_SF_weight, dijet_binning, 0)
	printInJson(fjson, fyml, dijetdilep, dijetdilepName, dijetdilep_var, dijetdilep_varName, twoLtwoBCond[x], twoLtwoBCondName[x],ll_weights+"*"+twoCSVV2_medium_SF_weight, dijetdilep_binning, 0)
	# 2L3B
        printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, twoLthreeBCond[x], twoLthreeBCondName[x],ll_weights, dilep_binning, 0)
        printInJson(fjson, fyml, j1pt, j1ptName, j_var, j_varName, twoLthreeBCond[x], twoLthreeBCondName[x],ll_weights, j_binning, 0)
        printInJson(fjson, fyml, j2pt, j2ptName, j_var, j_varName, twoLthreeBCond[x], twoLthreeBCondName[x],ll_weights, j_binning, 0)
        printInJson(fjson, fyml, dijet, dijetName, dijet_var, dijet_varName, twoLthreeBCond[x], twoLthreeBCondName[x],ll_weights, dijet_binning, 0)
        printInJson(fjson, fyml, dijetdilep, dijetdilepName, dijetdilep_var, dijetdilep_varName, twoLthreeBCond[x], twoLthreeBCondName[x],ll_weights, dijetdilep_binning, 0)
	# 2L2SJ
	printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, twoLtwoSubJCond[x] , twoLtwoSubJCondName[x],ll_weights, dilep_binning, 0)
	printInJson(fjson, fyml, fj, fjName, j_var, j_varName, twoLtwoSubJCond[x] , twoLtwoSubJCondName[x],ll_weights, j_binning, 0)
	printInJson(fjson, fyml, fj, fjName, fj_var, fj_varName, twoLtwoSubJCond[x] , twoLtwoSubJCondName[x],ll_weights, fj_binning, 0)
        printInJson(fjson, fyml, dilepFatjet, dilepFatjetName, dilepFatjet_var, dilepFatjet_varName, twoLtwoSubJCond[x] , twoLtwoSubJCondName[x],ll_weights,dilepFatjet_binning, 0)
	# 2L1BF
	printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, twoLOneBFatJetTCond[x] , twoLOneBFatJetTCondName[x],ll_weights, dilep_binning, 0)
	printInJson(fjson, fyml, fj, fjName, j_var, j_varName, twoLOneBFatJetTCond[x] , twoLOneBFatJetTCondName[x],ll_weights, j_binning, 0)
	printInJson(fjson, fyml, fj, fjName, fj_var, fj_varName, twoLOneBFatJetTCond[x] , twoLOneBFatJetTCondName[x],ll_weights, fj_binning, 0)
        #printInJson(fjson, fyml, dilepFatjet, dilepFatjetName, dilepFatjet_var, dilepFatjet_varName, twoLOneBFatJetTCond[x]+weights , twoLOneBFatJetTCondName[x], dilepFatjet_binning, 0)
	# 6) 2L2BSJ
	printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, twoLTwoBSubJetsLLCond[x], twoLTwoBSubJetsLLCondName[x],ll_weights, dilep_binning, 0)
	printInJson(fjson, fyml, fj, fjName, j_var, j_varName, twoLTwoBSubJetsLLCond[x] , twoLTwoBSubJetsLLCondName[x],ll_weights, j_binning, 0)
	printInJson(fjson, fyml, fj, fjName, fj_var, fj_varName, twoLTwoBSubJetsLLCond[x] , twoLTwoBSubJetsLLCondName[x],ll_weights, fj_binning, 0)
        #printInJson(fjson, fyml, dilepFatjet, dilepFatjetName, dilepFatjet_var, dilepFatjet_varName, twoLTwoBSubJetsMMCond[x]+weights , twoLTwoBSubJetsMMCondName[x],ll_weights, dilepFatjet_binning, 0)
	## test high mass
	printInJson(fjson, fyml, dijetdilep, dijetdilepName, dijetdilep_var, dijetdilep_varName, twoLTwoBHighMassCond[x],twoLTwoBHighMassCondName[x],ll_weights+"*"+twoCSVV2_medium_SF_weight, dijetdilep_binning, 0)
	printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, twoLTwoBHighMassCond[x],twoLTwoBHighMassCondName[x],ll_weights+"*"+twoCSVV2_medium_SF_weight, dilep_binning, 0)
	printInJson(fjson, fyml, dijet, dijetName, dijet_var, dijet_varName, twoLTwoBHighMassCond[x],twoLTwoBHighMassCondName[x],ll_weights+"*"+twoCSVV2_medium_SF_weight, dijet_binning, 0)
        
        printInJson(fjson, fyml, met, metName, met_var, met_varName, twoLTwoBHighMassCond[x],twoLTwoBHighMassCondName[x],ll_weights+"*"+twoCSVV2_medium_SF_weight, met_binning, 1 if x==0 else 0)

