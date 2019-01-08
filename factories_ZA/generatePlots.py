import copy, sys, os, inspect, yaml

scriptDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(scriptDir)
from basePlotter import *

##### Some helper functions #####

def check_overlap(lst):
    if not any(lst) or sum(lst) != 1:
        raise Exception("Arguments passed to generatePlots.py are not consistent!")

def getBinningStrWithMax(nBins, start, end, max):
    """Return string defining a binning in histFactory, with 'nBins' bins between
    'start' and 'end', but with the upper edge replaced by 'max'."""
    
    bins = [start]
    pos = start
    for i in range(nBins):
        pos += (end-start)/nBins
        bins.append(pos)
    if bins[-1] < max:
        bins[-1] = max

    m_string = str(len(bins)-1) + ", { "
    for b in bins[0:len(bins)-1]:
        m_string += str(b) + ", "
    m_string += str(bins[-1]) + "}"

    return m_string

##### Retrieve config file written by launchHistFactory.py:
config = {}
with open(os.path.join("/tmp", os.getenv("USER") + "_factory.json")) as f:
    # Use YAML because JSON loads strings as unicode by default, and this messes with Factories
    config = yaml.safe_load(f)

def get_cfg(var, default=False):
    if var in config.keys():
        return config[var]
    else:
        return default

for_data = (config['sample_type'] == 'Data')
for_MC = (config['sample_type'] == 'MC')
for_signal = (config['sample_type'] == 'Signal')
check_overlap([for_data, for_MC, for_signal])

use_syst = get_cfg('syst')
syst_split_jec = get_cfg('syst_split_jec', False)
syst_only_jec = get_cfg('syst_only_jec', False)
syst_split_pdf = get_cfg('syst_split_pdf', False)
reweight_DY = get_cfg('reweight_DY', False)

lljj_categories = get_cfg('lljj_categories', ['MuMu', 'ElEl', 'MuEl'])
llbb_categories = get_cfg('llbb_categories', ['MuMu', 'ElEl', 'MuEl'])
lljj_stages = get_cfg('lljj_stages', ['no_cut', 'mll_and_met_cut', 'mbb_cut', 'mll_and_met_cut_and_mbb_cut', 'inverted_met_cut', 'met_cut_and_inverted_mll_cut'])
llbb_stages = get_cfg('llbb_stages', ['no_cut', 'mll_and_met_cut', 'mbb_cut', 'mll_and_met_cut_and_mbb_cut', 'inverted_met_cut', 'met_cut_and_inverted_mll_cut'])
lljj_plot_families = get_cfg('lljj_plots', [])
llbb_plot_families = get_cfg('llbb_plots', [])

# Ask Factories to regroup "similar" plots
optimize_plots = True

####### Configure additional content for factory ####
plots = []
library_directories = []
sample_weights = {}

code_before_loop = default_code_before_loop()
code_in_loop = default_code_in_loop()
code_after_loop = default_code_after_loop()
include_directories = default_include_directories(scriptDir)
headers = default_headers()
libraries = default_libraries()
library_directories = default_library_directories()
sources = default_sources(scriptDir)

######### Plot configuration ###########

#### lljj
weights_lljj = ['trigeff', 'llidiso', 'pu']

if reweight_DY:
    weights_lljj.append('DY_weight11')
    weights_lljj.append('DY_weight12')
    weights_lljj.append('DY_weight13')
    weights_lljj.append('DY_weight14')
    weights_lljj.append('DY_weight15')
    weights_lljj.append('DY_weight16')
    weights_lljj.append('DY_weight17')
    weights_lljj.append('DY_weight21')
    weights_lljj.append('DY_weight22')
    weights_lljj.append('DY_weight23')
    weights_lljj.append('DY_weight24')
    weights_lljj.append('DY_weight25')
    weights_lljj.append('DY_weight26')
    weights_lljj.append('DY_weight27')
    weights_lljj.append('DY_weight31')
    weights_lljj.append('DY_weight32')
    weights_lljj.append('DY_weight33')
    weights_lljj.append('DY_weight34')
    weights_lljj.append('DY_weight35')
    weights_lljj.append('DY_weight36')
    weights_lljj.append('DY_weight37')
    weights_lljj.append('DY_weight41')
    weights_lljj.append('DY_weight42')
    weights_lljj.append('DY_weight43')
    weights_lljj.append('DY_weight44')
    weights_lljj.append('DY_weight45')
    weights_lljj.append('DY_weight46')
    weights_lljj.append('DY_weight47')
    weights_lljj.append('DY_weight51')
    weights_lljj.append('DY_weight52')
    weights_lljj.append('DY_weight53')
    weights_lljj.append('DY_weight54')
    weights_lljj.append('DY_weight55')
    weights_lljj.append('DY_weight56')
    weights_lljj.append('DY_weight57')
    weights_lljj.append('DY_weight61')
    weights_lljj.append('DY_weight62')
    weights_lljj.append('DY_weight63')
    weights_lljj.append('DY_weight64')
    weights_lljj.append('DY_weight65')
    weights_lljj.append('DY_weight66') 
    weights_lljj.append('DY_weight67') 

plots_lljj = []
if "basic" in lljj_plot_families:
    plots_lljj += ["basic"]
if "aFewVar" in lljj_plot_families:
    plots_lljj += ["aFewVar"]
if "other" in lljj_plot_families:
    plots_lljj += ["other"]
if "btag_efficiencies" in lljj_plot_families:
    plots_lljj += ["btag_efficiency_2d"]
if "inEllipse" in lljj_plot_families:
    plots_lljj += ["inEllipse"]
if "outOfEllipse" in lljj_plot_families:
    plots_lljj += ["outOfEllipse"]
if "inOut" in lljj_plot_families:
    plots_lljj += ["inOut"]
if "weights" in lljj_plot_families:
    plots_lljj += ["llidisoWeight", "trigeffWeight", "puWeight"]

#### llbb
weights_llbb = ['trigeff', 'llidiso', 'pu', 'jjbtag_heavy', 'jjbtag_light']

if reweight_DY:
    weights_llbb.append('DY_weight11')
    weights_llbb.append('DY_weight12')
    weights_llbb.append('DY_weight13')
    weights_llbb.append('DY_weight14')
    weights_llbb.append('DY_weight15')
    weights_llbb.append('DY_weight16')
    weights_llbb.append('DY_weight17')
    weights_llbb.append('DY_weight21')
    weights_llbb.append('DY_weight22')
    weights_llbb.append('DY_weight23')
    weights_llbb.append('DY_weight24')
    weights_llbb.append('DY_weight25')
    weights_llbb.append('DY_weight26')
    weights_llbb.append('DY_weight27')
    weights_llbb.append('DY_weight31')
    weights_llbb.append('DY_weight32')
    weights_llbb.append('DY_weight33')
    weights_llbb.append('DY_weight34')
    weights_llbb.append('DY_weight35')
    weights_llbb.append('DY_weight36')
    weights_llbb.append('DY_weight37')
    weights_llbb.append('DY_weight41')
    weights_llbb.append('DY_weight42')
    weights_llbb.append('DY_weight43')
    weights_llbb.append('DY_weight44')
    weights_llbb.append('DY_weight45')
    weights_llbb.append('DY_weight46')
    weights_llbb.append('DY_weight47')
    weights_llbb.append('DY_weight51')
    weights_llbb.append('DY_weight52')
    weights_llbb.append('DY_weight53')
    weights_llbb.append('DY_weight54')
    weights_llbb.append('DY_weight55')
    weights_llbb.append('DY_weight56')
    weights_llbb.append('DY_weight57')
    weights_llbb.append('DY_weight61')
    weights_llbb.append('DY_weight62')
    weights_llbb.append('DY_weight63')
    weights_llbb.append('DY_weight64')
    weights_llbb.append('DY_weight65')
    weights_llbb.append('DY_weight66') 
    weights_llbb.append('DY_weight67') 

plots_llbb = []
if "basic" in llbb_plot_families:
    plots_llbb += ["basic"]
if "aFewVar" in llbb_plot_families:
    plots_llbb += ["aFewVar"]
if "other" in llbb_plot_families:
    plots_llbb += ["other"]
if "inEllipse" in llbb_plot_families:
    plots_llbb += ["inEllipse"]
if "outOfEllipse" in llbb_plot_families:
    plots_llbb += ["outOfEllipse"]
if "inOut" in llbb_plot_families:
    plots_llbb += ["inOut"]
if "weights" in llbb_plot_families:
    plots_llbb += ["llidisoWeight", "trigeffWeight", "puWeight", "jjbtagWeight"]

# No weights for data!
if for_data:
    weights_lljj = []
    weights_llbb = []

##### Systematics ####

split_jec_sources_base = [
        "AbsoluteFlavMap",
        "AbsoluteMPFBias",
        "AbsoluteScale",
        "AbsoluteStat",
        "FlavorQCD",
        "Fragmentation",
        "PileUpDataMC",
        "PileUpPtBB",
        "PileUpPtEC1",
        "PileUpPtEC2",
        "PileUpPtHF",
        "PileUpPtRef",
        "RelativeBal",
        "RelativeFSR",
        "RelativeJEREC1",
        "RelativeJEREC2",
        "RelativeJERHF",
        "RelativePtBB",
        "RelativePtEC1",
        "RelativePtEC2",
        "RelativePtHF",
        "RelativeStatEC",
        "RelativeStatFSR",
        "RelativeStatHF",
        "SinglePionECAL",
        "SinglePionHCAL",
        "TimePtEta"
        ]
split_jec_sources = []
for _s in split_jec_sources_base:
    split_jec_sources.append("jec" + _s.lower() + "up")
    split_jec_sources.append("jec" + _s.lower() + "down")

if not use_syst:
    # No systematics
    systematics = { "modifObjects": ["nominal"] }
else:
    # Main systematics
    systematics = { 
            "modifObjects": [
                "nominal",
                "jecup", "jecdown",
                "jerup", "jerdown"
                ], 
            "SF": [
                "elidisoup", "elidisodown",
                "muidup", "muiddown",
                "muisoup", "muisodown",
                "jjbtaglightup", "jjbtaglightdown",
                "jjbtagheavyup", "jjbtagheavydown",
                "puup", "pudown",
                "trigeffup", "trigeffdown",
                "pdfup", "pdfdown",
                "elrecoup", "elrecodown",
                "mutrackingup", "mutrackingdown"
                #"hdampup", "hdampdown",
                ]
            }

    if reweight_DY:
        systematics["SF"].append("DY_weight11up")
        systematics["SF"].append("DY_weight11down")
        systematics["SF"].append("DY_weight12up")
        systematics["SF"].append("DY_weight12down")
        systematics["SF"].append("DY_weight13up")
        systematics["SF"].append("DY_weight13down")
        systematics["SF"].append("DY_weight14up")
        systematics["SF"].append("DY_weight14down")
        systematics["SF"].append("DY_weight15up")
        systematics["SF"].append("DY_weight15down")
        systematics["SF"].append("DY_weight16up")
        systematics["SF"].append("DY_weight16down")
        systematics["SF"].append("DY_weight17up")
        systematics["SF"].append("DY_weight17down")
        systematics["SF"].append("DY_weight21up")
        systematics["SF"].append("DY_weight21down")
        systematics["SF"].append("DY_weight22up")
        systematics["SF"].append("DY_weight22down")
        systematics["SF"].append("DY_weight23up")
        systematics["SF"].append("DY_weight23down")
        systematics["SF"].append("DY_weight24up")
        systematics["SF"].append("DY_weight24down")
        systematics["SF"].append("DY_weight25up")
        systematics["SF"].append("DY_weight25down")
        systematics["SF"].append("DY_weight26up")
        systematics["SF"].append("DY_weight26down")
        systematics["SF"].append("DY_weight27up")
        systematics["SF"].append("DY_weight27down")
        systematics["SF"].append("DY_weight31up")
        systematics["SF"].append("DY_weight31down")
        systematics["SF"].append("DY_weight32up")
        systematics["SF"].append("DY_weight32down")
        systematics["SF"].append("DY_weight33up")
        systematics["SF"].append("DY_weight33down")
        systematics["SF"].append("DY_weight34up")
        systematics["SF"].append("DY_weight34down")
        systematics["SF"].append("DY_weight35up")
        systematics["SF"].append("DY_weight35down")
        systematics["SF"].append("DY_weight36up")
        systematics["SF"].append("DY_weight36down")
        systematics["SF"].append("DY_weight37up")
        systematics["SF"].append("DY_weight37down")
        systematics["SF"].append("DY_weight41up")
        systematics["SF"].append("DY_weight41down")
        systematics["SF"].append("DY_weight42up")
        systematics["SF"].append("DY_weight42down")
        systematics["SF"].append("DY_weight43up")
        systematics["SF"].append("DY_weight43down")
        systematics["SF"].append("DY_weight44up")
        systematics["SF"].append("DY_weight44down")
        systematics["SF"].append("DY_weight45up")
        systematics["SF"].append("DY_weight45down")
        systematics["SF"].append("DY_weight46up")
        systematics["SF"].append("DY_weight46down")
        systematics["SF"].append("DY_weight47up")
        systematics["SF"].append("DY_weight47down")
        systematics["SF"].append("DY_weight51up")
        systematics["SF"].append("DY_weight51down")
        systematics["SF"].append("DY_weight52up")
        systematics["SF"].append("DY_weight52down")
        systematics["SF"].append("DY_weight53up")
        systematics["SF"].append("DY_weight53down")
        systematics["SF"].append("DY_weight54up")
        systematics["SF"].append("DY_weight54down")
        systematics["SF"].append("DY_weight55up")
        systematics["SF"].append("DY_weight55down")
        systematics["SF"].append("DY_weight56up")
        systematics["SF"].append("DY_weight56down")
        systematics["SF"].append("DY_weight57up")
        systematics["SF"].append("DY_weight57down")
        systematics["SF"].append("DY_weight61up")
        systematics["SF"].append("DY_weight61down")
        systematics["SF"].append("DY_weight62up")
        systematics["SF"].append("DY_weight62down")
        systematics["SF"].append("DY_weight63up")
        systematics["SF"].append("DY_weight63down")
        systematics["SF"].append("DY_weight64up")
        systematics["SF"].append("DY_weight64down")
        systematics["SF"].append("DY_weight65up")
        systematics["SF"].append("DY_weight65down")
        systematics["SF"].append("DY_weight66up")
        systematics["SF"].append("DY_weight66down")
        systematics["SF"].append("DY_weight67up")
        systematics["SF"].append("DY_weight67down")

    # Scale uncertainties
    for i in range(6):
        systematics["SF"].append("scaleUncorr{}".format(i))

    # All JEC sources, if asked
    if syst_split_jec:
        systematics["modifObjects"] += split_jec_sources

    # PDF split by initial state, if asked
    if syst_split_pdf:
        for _s in ["qq", "gg", "qg"]:
            systematics["SF"].append("pdf" + _s + "up")
            systematics["SF"].append("pdf" + _s + "down")

    if syst_only_jec:
        systematics["SF"] = []
        systematics["modifObjects"] = split_jec_sources

# Systematic uncertainties: depends on the stage on what we're running on...
def allowed_systematics_llbb(syst):
    if syst == "nominal":
        return True
    if "dyStat" in syst:
        return False
    if "dyScaleUncorr" in syst:
        return False
    if for_data:
        return False
    return True

def allowed_systematics_lljj(syst):
    if syst == "nominal":
        return True
    if "dyStat" in syst:
        return False
    if "dyScaleUncorr" in syst:
        return False
    if "jjbtag" in syst:
        return False
    if for_data:
        return False
    return True


#### Generate plot list #####
for systematicType in systematics.keys():
    
    for systematic in systematics[systematicType]:
        if systematicType == "modifObjects" and not for_data:
            objects = systematic
        else:
            objects = "nominal" #ensure that we use normal ZA_objects for systematics not modifying obect such as scale factors 


        ###### llbb ######
        
        basePlotter_llbb = BasePlotter(btag=True, objects=objects)
 
        if allowed_systematics_llbb(systematic):
            #This line was not here before
            for stage in llbb_stages:
                this_categories = llbb_categories[:]
                plots.extend(basePlotter_llbb.generatePlots(this_categories, stage, systematic=systematic, weights=weights_llbb, requested_plots=plots_llbb))

        # Signal: only do llbb!
        if for_signal:
            continue


        ##### lljj ######

        basePlotter_lljj = BasePlotter(btag=False, objects=objects)
        
        if allowed_systematics_lljj(systematic):
            #This line was not here before
            for stage in lljj_stages:
                this_categories = lljj_categories[:]
                plots.extend(basePlotter_lljj.generatePlots(this_categories, stage, systematic=systematic, weights=weights_lljj, requested_plots=plots_lljj))


for plot in plots:
    print plot
