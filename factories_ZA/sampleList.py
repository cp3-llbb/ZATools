####### Warning: put most recent tags first! ###### 
analysis_tags = [
        'v6.1.0+80X_ZAAnalysis_2017-12-12.v0-2-gf03f531' # back to cut based id for electrons
        #'v6.1.0+80X_ZAAnalysis_2017-12-12.v0-1-g21432f5' # --> back to cut based id for electrons (wrong, iso cut still included)
        #'v6.1.0+80X_ZAAnalysis_2017-12-12.v0' # --> m_electron_mva_wp80_name bug fixed, JEC and JER as systematics, new trigger eff files for electrons from hww 
        #'v6.1.0+80X_ZAAnalysis_2017-11-10.v0' # --> m_electron_mva_wp80_name bug
        #'v6.0.0+80X_ZAAnalysis_2017-09-27.v1' --> cmva bug, no METsignificance
        #'v5.0.1+80X-7-g03c2b54_ZAAnalysis_Moriond2015-7-g08c899b' # --> electrons are good
        #'v5.0.1+80X-2-g909e9e2_ZAAnalysis_Moriond2015-5-g0d38378'
        #'v5.0.1+80X-2-g909e9e2_ZAAnalysis_Moriond2015-1-gd479ab9'
        ]

samples_dict = {}


# Data
samples_dict["Data"] = [
    'DoubleEG',
    'MuonEG',
    'DoubleMuon'
]

# DY NLO
samples_dict["DY_NLO"] = [
    'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1',
    'DYToLL_0J_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1',
    'DYToLL_1J_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1',
    'DYToLL_2J_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1'
]

# TTBar
samples_dict["TTBar"] = [
    'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_extended_ext0_plus_ext1',
    'TTTo2L2Nu_13TeV-powheg_Summer16MiniAODv2'
]

# ZZ
samples_dict["ZZ"] = [
#     'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8',
     'ZZTo2L2Nu_13TeV_powheg_pythia8'
#     'ZZTo4L_13TeV_powheg_pythia8'
]

# ZH
samples_dict["ZH"] = [
    'HZJ_HToWW_M125_13TeV_powheg_pythia8_Summer16MiniAODv2',
    'GluGluZH_HToWWTo2L2Nu_ZTo2L_M125_13TeV_powheg_pythia8_Summer16MiniAODv2',
    'ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8_Summer16MiniAODv2',
    'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8_Summer16MiniAODv2',
    'ggZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8_Summer16MiniAODv2'
]

#WGamma
#samples_dict["WGamma"] = [
#    'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_plus_ext2_plus_ext3'
#]

# VV
samples_dict["VV"] = [
    # WW
    'WWToLNuQQ_13TeV-powheg_Summer16MiniAODv2',
    #'WWTo2L2Nu_13TeV-powheg_Summer16MiniAODv2',
    # WZ
    #'WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8_Summer16MiniAODv2',
    #'WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8_Summer16MiniAODv2',
    #'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8_Summer16MiniAODv2',
    'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8_Summer16MiniAODv2',
    # WZZ
    'WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_Summer16MiniAODv2',
    # WWZ
    'WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_Summer16MiniAODv2',
    # WWW
    'WWW_TuneCUETP8M1_13TeV-amcatnlo-pythia8_Summer16MiniAODv2',
    # ZZZ
    'ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_Summer16MiniAODv2'
]

# WJets 
#samples_dict["WJets"] = [
#    'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_Summer16MiniAODv2'
#]

# TTV
samples_dict["TTV"] = [
    'TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_Summer16MiniAODv2',
    'TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_Summer16MiniAODv2',
    'TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_Summer16MiniAODv2',
    'TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8_Summer16MiniAODv2'
]

# TTH
samples_dict["TTH"] = [
    'ttHToNonbb_M125_TuneCUETP8M2_13TeV_powheg_pythia8_Summer16MiniAODv2',
    'ttHTobb_M125_TuneCUETP8M2_13TeV_powheg_pythia8_Summer16MiniAODv2'
]

# Single top
samples_dict["SingleTop"] = [
    'ST_tW_antitop_5f_noFullyHadronicDecays_13TeV-powheg_Summer16MiniAODv2',
    'ST_tW_top_5f_noFullyHadronicDecays_13TeV-powheg_Summer16MiniAODv2',
    'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo_Summer16MiniAODv2',
    'ST_t-channel_top_4f_inclusiveDecays_13TeV-powheg-pythia8_Summer16MiniAODv2',
    'ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powheg-pythia8_Summer16MiniAODv'
]

# QCD
samples_dict["QCD"] = [
    #'QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8_Summer16MiniAODv2',
    #'QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8_extended_ext0_plus_ext1',
    'QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8_extended_ext0_plus_ext1',
    'QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8_extended_ext0_plus_ext1',
    'QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8_extended_ext0_plus_ext1',
    'QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8_Summer16MiniAODv2',
    'QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8_Faill15MiniAODv2',   #keep it?
    'QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8_Summer16MiniAODv2'
]

## Signals
samples_dict["Signal"] = [
    'HToZATo2L2B_MH-200_MA-50_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-200_MA-100_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-250_MA-50_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-250_MA-100_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-300_MA-50_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-300_MA-100_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-300_MA-200_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-500_MA-50_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-500_MA-100_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-500_MA-200_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-500_MA-300_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-500_MA-400_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-650_MA-50_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-800_MA-50_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-800_MA-100_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-800_MA-200_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-800_MA-400_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-800_MA-700_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-1000_MA-50_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-1000_MA-200_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-1000_MA-500_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-2000_MA-1000_13TeV-madgraph_Summer16MiniAODv2',
    'HToZATo2L2B_MH-3000_MA-2000_13TeV-madgraph_Summer16MiniAODv2'
]

# Number of samples used as basis for the reweighting
number_of_bases = 14

