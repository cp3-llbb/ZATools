import copy, sys, os
import numpy as np
import json

def get_scram_tool_info(tool, tag):
    import subprocess

    cmd = ['scram', 'tool', 'tag', tool, tag]

    return subprocess.check_output(cmd).strip()

def default_code_before_loop():
    return r"""
    std::ifstream ifile_mumu("/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/pavementForPValue/pavementForPValue_MuMu_part42.json");
    Json::Reader reader_mumu;
    Json::Value text_mumu;
    std::vector<massWindow> windows_MuMu;
    if (!ifile_mumu) std::cout << "ERROR OPENING FILE" << std::endl;
    if (ifile_mumu && reader_mumu.parse(ifile_mumu, text_mumu)) {
        for (int i=0; i<text_mumu.size(); i++) {
            const double a = text_mumu[i][2].asDouble();
            const double b = text_mumu[i][3].asDouble();
            const double theta = text_mumu[i][4].asDouble();
            double M11 = cos(theta)/sqrt(a);
            double M12 = sin(theta)/sqrt(a);
            double M21 = -sin(theta)/sqrt(b);
            double M22 = cos(theta)/sqrt(b);
            windows_MuMu.push_back(massWindow(text_mumu[i][0].asDouble(), text_mumu[i][1].asDouble(), M11, M12, M21, M22)); 
        }   
    }
    
    std::ifstream ifile_elel("/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/pavementForPValue/pavementForPValue_ElEl_part42.json");
    Json::Reader reader_elel;
    Json::Value text_elel;
    std::vector<massWindow> windows_ElEl;
    if (!ifile_elel) std::cout << "ERROR OPENING FILE" << std::endl;
    if (ifile_elel && reader_elel.parse(ifile_elel, text_elel)) {
        for (int i=0; i<text_elel.size(); i++) {
            const double a = text_elel[i][2].asDouble();
            const double b = text_elel[i][3].asDouble();
            const double theta = text_elel[i][4].asDouble();
            double M11 = cos(theta)/sqrt(a);
            double M12 = sin(theta)/sqrt(a);
            double M21 = -sin(theta)/sqrt(b);
            double M22 = cos(theta)/sqrt(b);
            windows_ElEl.push_back(massWindow(text_elel[i][0].asDouble(), text_elel[i][1].asDouble(), M11, M12, M21, M22)); 
        
        }
    }
    """

def default_code_in_loop():
    return ""

def default_code_after_loop():
    return ""

def default_headers():
    return [
            "massWindow.h",
            "reweightDY.h",
            "TLorentzVector.h"
            ]

def default_include_directories(scriptDir):
    paths = [
            os.path.join(scriptDir, "..", "common", "include"),
            ]
    return paths

def default_sources(scriptDir):
    files = [
            "massWindow.cc",
            "reweightDY.cc",
            ]
    files = [ os.path.join(scriptDir, "..", "common", "src", f) for f in files ]
    return files

def default_libraries():
    libs = []
    return libs

def default_library_directories():
    dirs = []
    return dirs


class BasePlotter:
    def __init__(self, btag, objects="nominal"):
        # systematic should be jecup, jecdown, jerup or jerdown. The one for lepton, btag, etc, have to be treated with the "weight" parameter in generatePlots.py (so far)

        self.baseObjectName_cmva = "hZA_lljj_cmva"
        self.baseObject_cmva = self.baseObjectName_cmva + "[0]"
        self.baseObjectName_deepCSV = "hZA_lljj_deepCSV"
        self.baseObject_deepCSV = self.baseObjectName_deepCSV + "[0]"
        self.btag = btag
        self.prefix = "hZA_"

        # For backwards compatibility with other tools:
        # FIXME: baseObjects to be modified in the next production
        self.baseObjectName = self.baseObjectName_deepCSV
        self.baseObject = self.baseObject_deepCSV
        if btag:
            self.suffix = self.baseObjectName + "" + ("_btagM")
        elif not btag:
            self.suffix = self.baseObjectName + "" + ("_nobtag")

        self.lep1_str = "hZA_leptons[%s.ilep1]" % self.baseObject
        self.lep2_str = "hZA_leptons[%s.ilep2]" % self.baseObject
        self.jet1_str = "hZA_jets[%s.ijet1]" % self.baseObject
        self.jet2_str = "hZA_jets[%s.ijet2]" % self.baseObject
        self.ll_str = "%s.ll_p4" % self.baseObject 
        self.jj_str = "%s.jj_p4" % self.baseObject
        self.met_str = "met_p4"
        self.metSig_str = "met_significance"
        self.jet_coll_str = "hZA_jets"
        self.lepton_coll_str = "hZA_leptons"
        self.sys_fwk = ""
        self.rho = 1. #put here the desired value of rho (from 0.5 to 3)


        if objects != "nominal":
            self.baseObjectName = self.baseObjectName.replace("hZA_", "hZA_" + objects + "_")
            self.baseObject = self.baseObject.replace("hZA_", "hZA_" + objects + "_")
            self.prefix += objects + "_"
            self.lep1_str = self.lep1_str.replace("hZA_", "hZA_" + objects + "_")
            self.lep2_str = self.lep2_str.replace("hZA_", "hZA_" + objects + "_")
            self.jet1_str = self.jet1_str.replace("hZA_", "hZA_" + objects + "_")
            self.jet2_str = self.jet2_str.replace("hZA_", "hZA_" + objects + "_")
            self.ll_str = self.ll_str.replace("hZA_", "hZA_" + objects + "_")
            self.jj_str = self.jj_str.replace("hZA_", "hZA_" + objects + "_")
            self.jet_coll_str = self.jet_coll_str.replace("hZA_", "hZA_" + objects + "_")
            self.lepton_coll_str = self.lepton_coll_str.replace("hZA_", "hZA_" + objects + "_")
            self.sys_fwk = "_" + objects
            self.met_str = "met_" + objects + "_p4"

        # needed to get scale factors (needs to be after the object modification due to systematics)
        self.lep1_fwkIdx = self.lep1_str + ".idx"
        self.lep2_fwkIdx = self.lep2_str + ".idx"
        self.jet1_fwkIdx = self.jet1_str + ".idx"
        self.jet2_fwkIdx = self.jet2_str + ".idx"

        # Ensure we have one candidate, works also for jecup etc
        self.sanityCheck = "Length$({}) > 0".format(self.baseObjectName)
        if self.btag:
            self.sanityCheck += " && {}.btag_deepCSV_MM".format(self.baseObject)

        # Categories (lepton flavours)
        self.dict_cat_cut =  {
            "ElEl": "({0}.isElEl && (runOnMC || (hZA_elel_fire_trigger_cut && runOnElEl)) && {1}.M() > 12)".format(self.baseObject, self.ll_str),
            "MuMu": "({0}.isMuMu && (runOnMC || (hZA_mumu_fire_trigger_cut && runOnMuMu)) && {1}.M() > 12)".format(self.baseObject, self.ll_str),
            "MuEl": "(({0}.isElMu || {0}.isMuEl) && (runOnMC || ((hZA_muel_fire_trigger_cut || hZA_elmu_fire_trigger_cut) && runOnElMu)) && {1}.M() > 12)".format(self.baseObject, self.ll_str)
                        }
        self.dict_cat_cut["SF"] = "(" + self.dict_cat_cut["ElEl"] + "||" + self.dict_cat_cut["MuMu"] + ")"
        self.dict_cat_cut["All"] = "(" + self.dict_cat_cut["ElEl"] + "||" + self.dict_cat_cut["MuMu"] + "||" + self.dict_cat_cut["MuEl"] + ")"

        # Possible stages (selection)
        mll_cut = "({0}.M() > 70) && ({0}.M() < 110)".format(self.ll_str, self.ll_str)
        met_cut = "({0}.Pt() > 0) && ({0}.Pt() < 80)".format(self.met_str, self.met_str)
        mbb_cut = "({0}.M() > 30)".format(self.jj_str)
        mll_and_met_cut = "({0} && {1})".format(mll_cut, met_cut)
        mll_and_met_cut_and_mbb_cut = "({0} && {1} && {2})".format(mll_cut, met_cut, mbb_cut)
        inverted_mll_cut = "({0}.M() <= 70 || {0}.M() >= 110)".format(self.ll_str, self.ll_str)
        inverted_met_cut = "({0}.Pt() >= 80)".format(self.met_str, self.met_str)
        inverted_mll_and_met_cut = "({0} && {1})".format(inverted_mll_cut, inverted_met_cut)
        met_cut_and_inverted_mll_cut = "({0} && {1})".format(inverted_mll_cut, met_cut)
        mll_cut_and_inverted_met_cut = "({0} && {1})".format(mll_cut, inverted_met_cut)

        self.dict_stage_cut = {
            "no_cut": "", 
            "mll_cut": mll_cut,
            "met_cut": met_cut,
            "mll_and_met_cut": mll_and_met_cut,
            "mll_and_met_cut_and_mbb_cut": mll_and_met_cut_and_mbb_cut,
            "inverted_mll_cut": inverted_mll_cut,
            "inverted_met_cut": inverted_met_cut,
            "inverted_mll_and_met_cut": inverted_mll_and_met_cut,
            "met_cut_and_inverted_mll_cut": met_cut_and_inverted_mll_cut,
            "mll_cut_and_inverted_met_cut": mll_cut_and_inverted_met_cut
        }


    def generatePlots(self, categories, stage, requested_plots, weights, systematic="nominal", extraString="", prependCuts=[], appendCuts=[], allowWeightedData=False): 

        # Protect against the fact that data do not have jecup collections, in the nominal case we still have to check that data have one candidate 
        sanityCheck = self.sanityCheck
        if systematic != "nominal" and not allowWeightedData:
            sanityCheck = self.joinCuts("!event_is_data", self.sanityCheck)

        cuts = self.joinCuts(*(prependCuts + [sanityCheck]))

        electron_1_id_cut = '({0}.isEl ? ( {0}.ele_hlt_id && !(std::abs({0}.p4.Eta()) > 1.444 && std::abs({0}.p4.Eta()) < 1.566) ) : 1)'.format(self.lep1_str)
        electron_2_id_cut = '({0}.isEl ? ( {0}.ele_hlt_id && !(std::abs({0}.p4.Eta()) > 1.444 && std::abs({0}.p4.Eta()) < 1.566) ) : 1)'.format(self.lep2_str)
        
        cuts = self.joinCuts(cuts, electron_1_id_cut, electron_2_id_cut)

        ###########
        # Weights #
        ###########

        # Lepton ID and Iso Scale Factors
        electron_id_branch = "electron_sf_id_mediumplushltsafe_hh"
        electron_reco_branch = "electron_sf_reco_moriond17"
        muon_tracking_branch = "muon_sf_tracking"
        muon_id_branch = "muon_sf_id_tight"
        muon_iso_branch = "muon_sf_iso_tight_id_tight"
        llIdIso_sf_dict = {
                "sf_lep1_el": "{id}[{0}][0] * {reco}[{0}][0]".format(self.lep1_fwkIdx, id=electron_id_branch, reco=electron_reco_branch),
                "sf_lep2_el": "{id}[{0}][0] * {reco}[{0}][0]".format(self.lep2_fwkIdx, id=electron_id_branch, reco=electron_reco_branch),
                "sf_lep1_mu": "{tracking}[{0}][0] * {id}[{0}][0] * {iso}[{0}][0]".format(self.lep1_fwkIdx, tracking=muon_tracking_branch, id=muon_id_branch, iso=muon_iso_branch),
                "sf_lep2_mu": "{tracking}[{0}][0] * {id}[{0}][0] * {iso}[{0}][0]".format(self.lep2_fwkIdx, tracking=muon_tracking_branch, id=muon_id_branch, iso=muon_iso_branch),
                "err_lep1_el": "0.",
                "err_lep1_mu": "0.",
                "err_lep2_el": "0.",
                "err_lep2_mu": "0.",
            }
        llIdIso_var = "NOMINAL"

        for sf in ["elidiso", "elreco", "mutracking", "muid", "muiso"]:
            if sf in systematic:
                if "up" in systematic:
                    llIdIso_var = "UP"
                    var_index = "2"
                elif "down" in systematic:
                    llIdIso_var = "DOWN"
                    var_index = "1"
                else:
                    raise Exception("Could not find up or down variation")

                if sf == "elidiso":
                    llIdIso_sf_dict["err_lep1_el"] = "{id}[{0}][{1}] * {reco}[{0}][0]".format(self.lep1_fwkIdx, var_index, id=electron_id_branch, reco=electron_reco_branch)
                    llIdIso_sf_dict["err_lep2_el"] = "{id}[{0}][{1}] * {reco}[{0}][0]".format(self.lep2_fwkIdx, var_index, id=electron_id_branch, reco=electron_reco_branch)

                if sf == "elreco": 
                    llIdIso_sf_dict["err_lep1_el"] = "{id}[{0}][0] * {reco}[{0}][{1}]".format(self.lep1_fwkIdx, var_index, id=electron_id_branch, reco=electron_reco_branch)
                    llIdIso_sf_dict["err_lep2_el"] = "{id}[{0}][0] * {reco}[{0}][{1}]".format(self.lep2_fwkIdx, var_index, id=electron_id_branch, reco=electron_reco_branch)

                if sf == "mutracking":
                    llIdIso_sf_dict["err_lep1_mu"] = "{tracking}[{0}][{1}] * {id}[{0}][0] * {iso}[{0}][0]".format(self.lep1_fwkIdx, var_index, tracking=muon_tracking_branch, id=muon_id_branch, iso=muon_iso_branch)
                    llIdIso_sf_dict["err_lep2_mu"] = "{tracking}[{0}][{1}] * {id}[{0}][0] * {iso}[{0}][0]".format(self.lep2_fwkIdx, var_index, tracking=muon_tracking_branch, id=muon_id_branch, iso=muon_iso_branch)

                if sf == "muid":
                    llIdIso_sf_dict["err_lep1_mu"] = "{tracking}[{0}][0] * {id}[{0}][{1}] * {iso}[{0}][0]".format(self.lep1_fwkIdx, var_index, tracking=muon_tracking_branch, id=muon_id_branch, iso=muon_iso_branch)
                    llIdIso_sf_dict["err_lep2_mu"] = "{tracking}[{0}][0] * {id}[{0}][{1}] * {iso}[{0}][0]".format(self.lep2_fwkIdx, var_index, tracking=muon_tracking_branch, id=muon_id_branch, iso=muon_iso_branch)

                if sf == "muiso":
                    llIdIso_sf_dict["err_lep1_mu"] = "{tracking}[{0}][0] * {id}[{0}][0] * {iso}[{0}][{1}]".format(self.lep1_fwkIdx, var_index, tracking=muon_tracking_branch, id=muon_id_branch, iso=muon_iso_branch)
                    llIdIso_sf_dict["err_lep2_mu"] = "{tracking}[{0}][0] * {id}[{0}][0] * {iso}[{0}][{1}]".format(self.lep2_fwkIdx, var_index, tracking=muon_tracking_branch, id=muon_id_branch, iso=muon_iso_branch)

        llIdIso_sf = """( common::combineScaleFactors<2>( {{ {{ 
                {{ 
                    ({lep1}.isEl) ? {sf_lep1_el} : {sf_lep1_mu},
                    ({lep1}.isEl) ? {err_lep1_el} : {err_lep1_mu}
                }},
                {{
                    ({lep2}.isEl) ? {sf_lep2_el} : {sf_lep2_mu},
                    ({lep2}.isEl) ? {err_lep2_el} : {err_lep2_mu}
                }}
            }} }}, common::Variation::{var} ) )""".format(lep1=self.lep1_str, lep2=self.lep2_str, var=llIdIso_var, **llIdIso_sf_dict)

        # BTAG SF, only applied if requesting b-tags
        if self.btag:
            jjBtag_light_sfIdx = "[0]"
            jjBtag_light_strCommon="NOMINAL"
            if systematic == "jjbtaglightup":
                jjBtag_light_sfIdx = "[2]" 
                jjBtag_light_strCommon="UP"
            if systematic == "jjbtaglightdown":
                jjBtag_light_sfIdx = "[1]"
                jjBtag_light_strCommon="DOWN"

            jjBtag_heavy_sfIdx = "[0]"
            jjBtag_heavy_strCommon="NOMINAL"
            if systematic == "jjbtagheavyup":
                jjBtag_heavy_sfIdx = "[2]" 
                jjBtag_heavy_strCommon="UP"
            if systematic == "jjbtagheavydown":
                jjBtag_heavy_sfIdx = "[1]"
                jjBtag_heavy_strCommon="DOWN"

            jjBtag_heavyjet_sf = "(common::combineScaleFactors<2>({{ {{ {{ jet{0}_sf_deepCSV_heavyjet_{1}[{2}][0] , jet{0}_sf_deepCSV_heavyjet_{1}[{2}]{3} }}, {{ jet{0}_sf_deepCSV_heavyjet_{1}[{4}][0], jet{0}_sf_deepCSV_heavyjet_{1}[{4}]{3} }} }} }}, common::Variation::{5}) )".format(self.sys_fwk, "medium", self.jet1_fwkIdx, jjBtag_heavy_sfIdx, self.jet2_fwkIdx, jjBtag_heavy_strCommon)

            jjBtag_lightjet_sf = "(common::combineScaleFactors<2>({{ {{ {{ jet{0}_sf_deepCSV_lightjet_{1}[{2}][0] , jet{0}_sf_deepCSV_lightjet_{1}[{2}]{3} }},{{ jet{0}_sf_deepCSV_lightjet_{1}[{4}][0], jet{0}_sf_deepCSV_lightjet_{1}[{4}]{3} }} }} }}, common::Variation::{5}) )".format(self.sys_fwk, "medium", self.jet1_fwkIdx, jjBtag_light_sfIdx, self.jet2_fwkIdx, jjBtag_light_strCommon)

        else:
            jjBtag_heavyjet_sf = "1."
            jjBtag_lightjet_sf = "1."

        # PU WEIGHT
        puWeight = "event_pu_weight"
        if systematic == "puup":
            puWeight = "event_pu_weight_up"
        if systematic == "pudown":
            puWeight = "event_pu_weight_down"

        # PDF, HDAMP weight
        pdfWeight = ""
        normalization = "nominal"
        for pdf in ["", "qq", "gg", "qg"]:
            for var in ["up", "down"]:
                if systematic == "pdf" + pdf + var:
                    _pdf = pdf + "_" if pdf != "" else ""
                    pdfWeight = "event_pdf_weight_" + _pdf + var
                    normalization = "pdf_" + _pdf + var
        for var in ["up", "down"]:
            if systematic == "hdamp" + var:
                pdfWeight = "event_hdamp_weight_" + var
                normalization = "hdamp_" + var

        # TRIGGER EFFICIENCY
        trigEff = "({0}.trigger_efficiency)".format(self.baseObject)
        if systematic == "trigeffup":
            trigEff = "({0}.trigger_efficiency_upVariated)".format(self.baseObject)
        if systematic == "trigeffdown":
            trigEff = "({0}.trigger_efficiency_downVariated)".format(self.baseObject)


        #100%: w_up=2*w-1
        #      w_down=1
        #50%: w_up=(3*w-1)/2
        #     w_down=(w+1)/2
        #200%: w_up=3*w-2
        #      w_down=2-w
        # DY REWEIGHTING - TO BE USED ONLY FOR DRELL-YAN, ENABLE IT IN THE CONFIG FILE

        DY_weight11 = "(({0}>0 && {0}<100 && {1}>750 && {1}<1000) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight11up":
            DY_weight11 = "( ({0}>0 && {0}<100 && {1}>750 && {1}<1000) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight11down":
            DY_weight11 = "( ({0}>0 && {0}<100 && {1}>750 && {1}<1000) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
           
        DY_weight12 = "(({0}>=100 && {0}<250 && {1}>750 && {1}<1000) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight12up":
            DY_weight12 = "( ({0}>=100 && {0}<250 && {1}>750 && {1}<1000) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight12down":
            DY_weight12 = "( ({0}>=100 && {0}<250 && {1}>750 && {1}<1000) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight13 = "(({0}>=250 && {0}<400 && {1}>750 && {1}<1000) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight13up":
            DY_weight13 = "( ({0}>=250 && {0}<400 && {1}>750 && {1}<1000) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight13down":
            DY_weight13 = "( ({0}>=250 && {0}<400 && {1}>750 && {1}<1000) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight14 = "(({0}>=400 && {0}<550 && {1}>750 && {1}<1000) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight14up":
            DY_weight14 = "( ({0}>=400 && {0}<550 && {1}>750 && {1}<1000) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight14down":
            DY_weight14 = "( ({0}>=400 && {0}<550 && {1}>750 && {1}<1000) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight15 = "(({0}>=550 && {0}<700 && {1}>750 && {1}<1000) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight15up":
            DY_weight15 = "( ({0}>=550 && {0}<700 && {1}>750 && {1}<1000) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight15down":
            DY_weight15 = "( ({0}>=550 && {0}<700 && {1}>750 && {1}<1000) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight16 = "(({0}>=700 && {0}<850 && {1}>750 && {1}<1000) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight16up":
            DY_weight16 = "( ({0}>=700 && {0}<850 && {1}>750 && {1}<1000) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight16down":
            DY_weight16 = "( ({0}>=700 && {0}<850 && {1}>750 && {1}<1000) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight17 = "(({0}>=850 && {0}<1000 && {1}>750 && {1}<1000) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight17up":
            DY_weight17 = "( ({0}>=850 && {0}<1000 && {1}>750 && {1}<1000) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight17down":
            DY_weight17 = "( ({0}>=850 && {0}<1000 && {1}>750 && {1}<1000) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")


        DY_weight21 = "(({0}>0 && {0}<100 && {1}>600 && {1}<=750) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight21up":
            DY_weight21 = "( ({0}>0 && {0}<100 && {1}>600 && {1}<=750) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight21down":
            DY_weight21 = "( ({0}>0 && {0}<100 && {1}>600 && {1}<=750) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
           
        DY_weight22 = "(({0}>=100 && {0}<250 && {1}>600 && {1}<=750) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight22up":
            DY_weight22 = "( ({0}>=100 && {0}<250 && {1}>600 && {1}<=750) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight22down":
            DY_weight22 = "( ({0}>=100 && {0}<250 && {1}>600 && {1}<=750) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight23 = "(({0}>=250 && {0}<400 && {1}>600 && {1}<=750) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight23up":
            DY_weight23 = "( ({0}>=250 && {0}<400 && {1}>600 && {1}<=750) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight23down":
            DY_weight23 = "( ({0}>=250 && {0}<400 && {1}>600 && {1}<=750) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight24 = "(({0}>=400 && {0}<550 && {1}>600 && {1}<=750) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight24up":
            DY_weight24 = "( ({0}>=400 && {0}<550 && {1}>600 && {1}<=750) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight24down":
            DY_weight24 = "( ({0}>=400 && {0}<550 && {1}>600 && {1}<=750) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight25 = "(({0}>=550 && {0}<700 && {1}>600 && {1}<=750) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight25up":
            DY_weight25 = "( ({0}>=550 && {0}<700 && {1}>600 && {1}<=750) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight25down":
            DY_weight25 = "( ({0}>=550 && {0}<700 && {1}>600 && {1}<=750) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight26 = "(({0}>=700 && {0}<850 && {1}>600 && {1}<=750) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight26up":
            DY_weight26 = "( ({0}>=700 && {0}<850 && {1}>600 && {1}<=750) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight26down":
            DY_weight26 = "( ({0}>=700 && {0}<850 && {1}>600 && {1}<=750) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight27 = "(({0}>=850 && {0}<1000 && {1}>600 && {1}<=750) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight27up":
            DY_weight27 = "( ({0}>=850 && {0}<1000 && {1}>600 && {1}<=750) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight27down":
            DY_weight27 = "( ({0}>=850 && {0}<1000 && {1}>600 && {1}<=750) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight31 = "(({0}>0 && {0}<100 && {1}>450 && {1}<=600) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight31up":
            DY_weight31 = "( ({0}>0 && {0}<100 && {1}>450 && {1}<=600) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight31down":
            DY_weight31 = "( ({0}>0 && {0}<100 && {1}>450 && {1}<=600) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
           
        DY_weight32 = "(({0}>=100 && {0}<250 && {1}>450 && {1}<=600) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight32up":
            DY_weight32 = "( ({0}>=100 && {0}<250 && {1}>450 && {1}<=600) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight32down":
            DY_weight32 = "( ({0}>=100 && {0}<250 && {1}>450 && {1}<=600) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight33 = "(({0}>=250 && {0}<400 && {1}>450 && {1}<=600) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight33up":
            DY_weight33 = "( ({0}>=250 && {0}<400 && {1}>450 && {1}<=600) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight33down":
            DY_weight33 = "( ({0}>=250 && {0}<400 && {1}>450 && {1}<=600) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight34 = "(({0}>=400 && {0}<550 && {1}>450 && {1}<=600) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight34up":
            DY_weight34 = "( ({0}>=400 && {0}<550 && {1}>450 && {1}<=600) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight34down":
            DY_weight34 = "( ({0}>=400 && {0}<550 && {1}>450 && {1}<=600) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight35 = "(({0}>=550 && {0}<700 && {1}>450 && {1}<=600) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight35up":
            DY_weight35 = "( ({0}>=550 && {0}<700 && {1}>450 && {1}<=600) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight35down":
            DY_weight35 = "( ({0}>=550 && {0}<700 && {1}>450 && {1}<=600) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight36 = "(({0}>=700 && {0}<850 && {1}>450 && {1}<=600) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight36up":
            DY_weight36 = "( ({0}>=700 && {0}<850 && {1}>450 && {1}<=600) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight36down":
            DY_weight36 = "( ({0}>=700 && {0}<850 && {1}>450 && {1}<=600) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight37 = "(({0}>=850 && {0}<1000 && {1}>450 && {1}<=600) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight37up":
            DY_weight37 = "( ({0}>=850 && {0}<1000 && {1}>450 && {1}<=600) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight37down":
            DY_weight37 = "( ({0}>=850 && {0}<1000 && {1}>450 && {1}<=600) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight41 = "(({0}>0 && {0}<100 && {1}>300 && {1}<=450) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight41up":
            DY_weight41 = "( ({0}>0 && {0}<100 && {1}>300 && {1}<=450) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight41down":
            DY_weight41 = "( ({0}>0 && {0}<100 && {1}>300 && {1}<=450) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
           
        DY_weight42 = "(({0}>=100 && {0}<250 && {1}>300 && {1}<=450) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight42up":
            DY_weight42 = "( ({0}>=100 && {0}<250 && {1}>300 && {1}<=450) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight42down":
            DY_weight42 = "( ({0}>=100 && {0}<250 && {1}>300 && {1}<=450) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight43 = "(({0}>=250 && {0}<400 && {1}>300 && {1}<=450) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight43up":
            DY_weight43 = "( ({0}>=250 && {0}<400 && {1}>300 && {1}<=450) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight43down":
            DY_weight43 = "( ({0}>=250 && {0}<400 && {1}>300 && {1}<=450) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight44 = "(({0}>=400 && {0}<550 && {1}>300 && {1}<=450) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight44up":
            DY_weight44 = "( ({0}>=400 && {0}<550 && {1}>300 && {1}<=450) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight44down":
            DY_weight44 = "( ({0}>=400 && {0}<550 && {1}>300 && {1}<=450) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight45 = "(({0}>=550 && {0}<700 && {1}>300 && {1}<=450) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight45up":
            DY_weight45 = "( ({0}>=550 && {0}<700 && {1}>300 && {1}<=450) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight45down":
            DY_weight45 = "( ({0}>=550 && {0}<700 && {1}>300 && {1}<=450) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight46 = "(({0}>=700 && {0}<850 && {1}>300 && {1}<=450) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight46up":
            DY_weight46 = "( ({0}>=700 && {0}<850 && {1}>300 && {1}<=450) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight46down":
            DY_weight46 = "( ({0}>=700 && {0}<850 && {1}>300 && {1}<=450) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight47 = "(({0}>=850 && {0}<1000 && {1}>300 && {1}<=450) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight47up":
            DY_weight47 = "( ({0}>=850 && {0}<1000 && {1}>300 && {1}<=450) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight47down":
            DY_weight47 = "( ({0}>=850 && {0}<1000 && {1}>300 && {1}<=450) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight51 = "(({0}>0 && {0}<100 && {1}>150 && {1}<=300) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight51up":
            DY_weight51 = "( ({0}>0 && {0}<100 && {1}>150 && {1}<=300) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight51down":
            DY_weight51 = "( ({0}>0 && {0}<100 && {1}>150 && {1}<=300) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
           
        DY_weight52 = "(({0}>=100 && {0}<250 && {1}>150 && {1}<=300) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight52up":
            DY_weight52 = "( ({0}>=100 && {0}<250 && {1}>150 && {1}<=300) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight52down":
            DY_weight52 = "( ({0}>=100 && {0}<250 && {1}>150 && {1}<=300) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight53 = "(({0}>=250 && {0}<400 && {1}>150 && {1}<=300) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight53up":
            DY_weight53 = "( ({0}>=250 && {0}<400 && {1}>150 && {1}<=300) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight53down":
            DY_weight53 = "( ({0}>=250 && {0}<400 && {1}>150 && {1}<=300) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight54 = "(({0}>=400 && {0}<550 && {1}>150 && {1}<=300) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight54up":
            DY_weight54 = "( ({0}>=400 && {0}<550 && {1}>150 && {1}<=300) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight54down":
            DY_weight54 = "( ({0}>=400 && {0}<550 && {1}>150 && {1}<=300) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight55 = "(({0}>=550 && {0}<700 && {1}>150 && {1}<=300) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight55up":
            DY_weight55 = "( ({0}>=550 && {0}<700 && {1}>150 && {1}<=300) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight55down":
            DY_weight55 = "( ({0}>=550 && {0}<700 && {1}>150 && {1}<=300) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight56 = "(({0}>=700 && {0}<850 && {1}>150 && {1}<=300) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight56up":
            DY_weight56 = "( ({0}>=700 && {0}<850 && {1}>150 && {1}<=300) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight56down":
            DY_weight56 = "( ({0}>=700 && {0}<850 && {1}>150 && {1}<=300) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight57 = "(({0}>=850 && {0}<1000 && {1}>150 && {1}<=300) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight57up":
            DY_weight57 = "( ({0}>=850 && {0}<1000 && {1}>150 && {1}<=300) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight57down":
            DY_weight57 = "( ({0}>=850 && {0}<1000 && {1}>150 && {1}<=300) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight61 = "(({0}>0 && {0}<100 && {1}>0 && {1}<=150) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight61up":
            DY_weight61 = "( ({0}>0 && {0}<100 && {1}>0 && {1}<=150) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight61down":
            DY_weight61 = "( ({0}>0 && {0}<100 && {1}>0 && {1}<=150) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
           
        DY_weight62 = "(({0}>=100 && {0}<250 && {1}>0 && {1}<=150) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight62up":
            DY_weight62 = "( ({0}>=100 && {0}<250 && {1}>0 && {1}<=150) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight62down":
            DY_weight62 = "( ({0}>=100 && {0}<250 && {1}>0 && {1}<=150) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight63 = "(({0}>=250 && {0}<400 && {1}>0 && {1}<=150) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight63up":
            DY_weight63 = "( ({0}>=250 && {0}<400 && {1}>0 && {1}<=150) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight63down":
            DY_weight63 = "( ({0}>=250 && {0}<400 && {1}>0 && {1}<=150) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight64 = "(({0}>=400 && {0}<550 && {1}>0 && {1}<=150) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight64up":
            DY_weight64 = "( ({0}>=400 && {0}<550 && {1}>0 && {1}<=150) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight64down":
            DY_weight64 = "( ({0}>=400 && {0}<550 && {1}>0 && {1}<=150) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight65 = "(({0}>=550 && {0}<700 && {1}>0 && {1}<=150) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight65up":
            DY_weight65 = "( ({0}>=550 && {0}<700 && {1}>0 && {1}<=150) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight65down":
            DY_weight65 = "( ({0}>=550 && {0}<700 && {1}>0 && {1}<=150) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight66 = "(({0}>=700 && {0}<850 && {1}>0 && {1}<=150) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight66up":
            DY_weight66 = "( ({0}>=700 && {0}<850 && {1}>0 && {1}<=150) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight66down":
            DY_weight66 = "( ({0}>=700 && {0}<850 && {1}>0 && {1}<=150) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")

        DY_weight67 = "(({0}>=850 && {0}<1000 && {1}>0 && {1}<=150) ? computeDYweight({0}, {1}) : 1.)".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight67up":
            DY_weight67 = "( ({0}>=850 && {0}<1000 && {1}>0 && {1}<=150) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})+std::max(1.03,computeDYweight({0},{1}))-1.) : (computeDYweight({0},{1})+std::min(0.97,computeDYweight({0},{1}))-1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")
        if systematic == "DY_weight67down":
            DY_weight67 = "( ({0}>=850 && {0}<1000 && {1}>0 && {1}<=150) ? ( (computeDYweight({0},{1})>=1.) ? (computeDYweight({0},{1})-std::max(1.03,computeDYweight({0},{1}))+1.) : (computeDYweight({0},{1})-std::min(0.97,computeDYweight({0},{1}))+1.) ) : 1. )".format(self.jj_str+".M()", self.baseObject+".p4.M()")


        
        
        available_weights = {
                'trigeff': trigEff,
                'jjbtag_heavy': jjBtag_heavyjet_sf,
                'jjbtag_light': jjBtag_lightjet_sf,
                'llidiso': llIdIso_sf,
                'pu': puWeight,
                'DY_weight11': DY_weight11,
                'DY_weight12': DY_weight12,
                'DY_weight13': DY_weight13,
                'DY_weight14': DY_weight14,
                'DY_weight15': DY_weight15,
                'DY_weight16': DY_weight16,
                'DY_weight17': DY_weight17,
                'DY_weight21': DY_weight21,
                'DY_weight22': DY_weight22,
                'DY_weight23': DY_weight23,
                'DY_weight24': DY_weight24,
                'DY_weight25': DY_weight25,
                'DY_weight26': DY_weight26,
                'DY_weight27': DY_weight27,
                'DY_weight31': DY_weight31,
                'DY_weight32': DY_weight32,
                'DY_weight33': DY_weight33,
                'DY_weight34': DY_weight34,
                'DY_weight35': DY_weight35,
                'DY_weight36': DY_weight36,
                'DY_weight37': DY_weight37,
                'DY_weight41': DY_weight41,
                'DY_weight42': DY_weight42,
                'DY_weight43': DY_weight43,
                'DY_weight44': DY_weight44,
                'DY_weight45': DY_weight45,
                'DY_weight46': DY_weight46,
                'DY_weight47': DY_weight47,
                'DY_weight51': DY_weight51,
                'DY_weight52': DY_weight52,
                'DY_weight53': DY_weight53,
                'DY_weight54': DY_weight54,
                'DY_weight55': DY_weight55,
                'DY_weight56': DY_weight56,
                'DY_weight57': DY_weight57,
                'DY_weight61': DY_weight61,
                'DY_weight62': DY_weight62,
                'DY_weight63': DY_weight63,
                'DY_weight64': DY_weight64,
                'DY_weight65': DY_weight65,
                'DY_weight66': DY_weight66,
                'DY_weight67': DY_weight67
                }
        
        # Append the proper extension to the name plot if needed
        self.systematicString = ""
        if not systematic == "nominal":
            self.systematicString = "__" + systematic

        #########
        # PLOTS #
        #########
        self.basic_plot = []
        self.aFewVar_plot = []
        self.csv_plot = []
        self.isElEl_plot = []
 
        self.gen_plot = []
        self.evt_plot = []

        self.other_plot = []
        self.vertex_plot = []
        self.genht_plot = []
        self.inEllipse_plot = []
        self.outOfEllipse_plot = []
        self.inOut_plot = []

        self.forSkimmer_plot = []

        for cat in categories:

            catCut = self.dict_cat_cut[cat]
            self.totalCut = self.joinCuts(cuts, catCut, self.dict_stage_cut[stage], *appendCuts)
            self.cutWithoutCat = self.joinCuts(cuts, self.dict_stage_cut[stage], *appendCuts)

            self.llFlav = cat
            self.extraString = stage + extraString

            # Plot to compute yields (ensure we have not over/under flow)
            #self.isElEl_plot.append({
            #            'name': 'isElEl_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
            #            'variable': "%s.isElEl"%self.baseObject,
            #            'plot_cut': self.totalCut,
            #            'binning': '(2, 0, 2)'
            #    })
            
            
            def get_jet_flavour_cut(flav, jet_idx):
                if flav == "g":
                    return "{jets}[{idx}].gen_l && jet{sys}_partonFlavor[{jets}[{idx}].idx] == 21".format(sys=self.sys_fwk, jets=self.jet_coll_str, idx=jet_idx)
                elif flav == "q":
                    return "{jets}[{idx}].gen_l && std::abs(jet{sys}_partonFlavor[{jets}[{idx}].idx]) >= 1 && std::abs(jet{sys}_partonFlavor[{jets}[{idx}].idx]) <= 3".format(sys=self.sys_fwk, jets=self.jet_coll_str, idx=jet_idx)
                elif flav == "n":
                    return "{jets}[{idx}].gen_l && jet{sys}_partonFlavor[{jets}[{idx}].idx] == 0".format(sys=self.sys_fwk, jets=self.jet_coll_str, idx=jet_idx)
                else:
                    return "{jets}[{idx}].gen_{flav}".format(jets=self.jet_coll_str, idx=jet_idx, flav=flav)
            
            mll_plot_binning = '(75, 12, 252)'


            self.aFewVar_plot.extend([
                #{
                #        'name': 'll_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.ll_str+".M()",
                #        'plot_cut': self.totalCut,
                #        'binning': mll_plot_binning
                #},
                #{
                #        'name': 'met_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.met_str + ".Pt()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, 0, 500)'
                #}
                #{
                #        'name': 'Mjj_vs_Mlljj_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.jj_str + '.M() ::: '+self.baseObject + '.p4.M()',
                #        'plot_cut': self.totalCut,
                #        'binning': '(150, 0, 1500, 150, 0, 1500)'
                #},
                {
                        'name': 'lljj_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".p4.M()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 100, 1500)'
                },
                {
                        'name': 'jj_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jj_str + ".M()",
                        'plot_cut': self.totalCut,
                        'binning': '(40, 0, 1000)'
                }
                #{
                #        'name': 'll_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.ll_str+".Pt()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, 0, 450)'
                #},
                #{
                #        'name': 'jj_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.jj_str+".Pt()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, 0, 450)'
                #},
                #{
                #        'name': 'lep1_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.lep1_str+".p4.Pt()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, 20, 400)'
                #},
                #{
                #        'name': 'lep2_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.lep2_str+".p4.Pt()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, 10, 200)'
                #},
                #{
                #        'name': 'jet1_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.jet1_str+".p4.Pt()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, 20, 500)'
                #},
                #{
                #        'name': 'jet2_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.jet2_str+".p4.Pt()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, 20, 300)'
                #},
                #{
                #        'name': 'lep1_eta_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.lep1_str+".p4.Eta()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, -4, 4)'
                #},
                #{
                #        'name': 'lep2_eta_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.lep2_str+".p4.Eta()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, -4, 4)'
                #},
                #{
                #        'name': 'jet1_eta_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.jet1_str+".p4.Eta()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, -4, 4)'
                #},
                #{
                #        'name': 'jet2_eta_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.jet2_str+".p4.Eta()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, -4, 4)'
                #},
                #{
                #        'name': 'lep1_phi_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.lep1_str+".p4.Phi()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, -4, 4)'
                #},
                #{
                #        'name': 'lep2_phi_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.lep2_str+".p4.Phi()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, -4, 4)'
                #},
                #{
                #        'name': 'jet1_phi_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.jet1_str+".p4.Phi()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, -4, 4)'
                #},
                #{
                #        'name': 'jet2_phi_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.jet2_str+".p4.Phi()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, -4, 4)'
                #},
                #{
                #        'name': 'll_DPhi_l_l_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': "abs("+self.baseObject+".DPhi_l_l)",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, 0, 3.1416)'
                #},
                
            ])




            # BASIC PLOTS
            self.basic_plot.extend([
                {
                        'name': 'Mjj_vs_Mlljj_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jj_str + '.M() ::: '+self.baseObject + '.p4.M()',
                        'plot_cut': self.totalCut,
                        'binning': '(150, 0, 1500, 150, 0, 1500)'
                },
                {
                        'name': 'lep1_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.lep1_str+".p4.Pt()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 20, 400)'
                },
                {
                        'name': 'lep2_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.lep2_str+".p4.Pt()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 10, 200)'
                },
                {
                        'name': 'jet1_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet1_str+".p4.Pt()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 20, 500)'
                },
                {
                        'name': 'jet2_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet2_str+".p4.Pt()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 20, 300)'
                },
                {
                        'name': 'lep1_eta_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.lep1_str+".p4.Eta()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, -4, 4)'
                },
                {
                        'name': 'lep2_eta_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.lep2_str+".p4.Eta()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, -4, 4)'
                },
                {
                        'name': 'jet1_eta_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet1_str+".p4.Eta()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, -4, 4)'
                },
                {
                        'name': 'jet2_eta_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet2_str+".p4.Eta()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, -4, 4)'
                },
                {
                        'name': 'lep1_phi_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.lep1_str+".p4.Phi()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, -4, 4)'
                },
                {
                        'name': 'lep2_phi_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.lep2_str+".p4.Phi()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, -4, 4)'
                },
                {
                        'name': 'jet1_phi_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet1_str+".p4.Phi()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, -4, 4)'
                },
                {
                        'name': 'jet2_phi_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet2_str+".p4.Phi()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, -4, 4)'
                },
                {
                        'name': 'lljj_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".p4.M()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 100, 1500)'
                },
                #{
                #        'name': 'llbb_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': "(" + self.ll_str + "+" + self.jj_str + ").M()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, 100, 1500)'
                #},
                {
                        'name': 'jj_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jj_str + ".M()",
                        'plot_cut': self.totalCut,
                        'binning': '(40, 10, 1000)'
                },
                {
                        'name': 'll_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.ll_str+".M()",
                        'plot_cut': self.totalCut,
                        'binning': mll_plot_binning
                },
                {
                        'name': 'll_DR_l_l_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".DR_l_l",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 6)'
                },
                {
                        'name': 'jj_DR_j_j_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".DR_j_j",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 6)'
                },
                {
                        'name': 'll_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.ll_str+".Pt()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 450)'
                },
                {
                        'name': 'jj_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jj_str+".Pt()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 450)'
                },
                {
                        'name': 'll_DPhi_l_l_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "abs("+self.baseObject+".DPhi_l_l)",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 3.1416)'
                },
                {
                        'name': 'jj_DPhi_j_j_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "abs("+self.baseObject+".DPhi_j_j)",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 3.1416)'
                },
                {
                        'name': 'met_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.met_str + ".Pt()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 500)'
                }
                #{
                #        'name': 'met_E_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.met_str + ".E()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, 0, 500)'
                #},
                #{
                #        'name': 'met_significance_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.metSig_str,
                #        'plot_cut': self.totalCut,
                #        'binning': '(300, 0, 500)'
                #}
            ])
                

#            if self.btag:
#                self.basic_plot.extend([
#                    {
#                            'name': 'jet1_deepCSV_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
#                            'variable': self.jet1_str+".deepCSV",
#                            'plot_cut': self.totalCut,
#                            'binning': '(50, -1, 1)'
#                    },
#                    {
#                            'name': 'jet2_deepCSV_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
#                            'variable': self.jet2_str+".deepCSV",
#                            'plot_cut': self.totalCut,
#                            'binning': '(50, -1, 1)'
#                    },
#                    {
#                            'name': 'jj_deepCSV_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
#                            'variable': self.baseObject+".sumDeepCSV",
#                            'plot_cut': self.totalCut,
#                            'binning': '(50, -2, 2)'
#                    },
#                    {
#                            'name': 'jet1_deepCSV_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
#                            'variable': self.jet1_str+".btag_deepCSV_M",
#                            'plot_cut': self.totalCut,
#                            'binning': '(50, -1, 1)'
#                    },
#                    {
#                            'name': 'jj_deepCSV_MM_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
#                            'variable': self.baseObject+".btag_deepCSV_MM",
#                            'plot_cut': self.totalCut,
#                            'binning': '(50, -1, 1)'
#                    }
#                ])

            #PLOTS IN ELLIPSE
            if cat=='MuEl':  #Load the ElEl file for the MuEl category
                with open('/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/pavementForPValue/pavementForPValue_ElEl_part42.json') as f:
                    parameters = json.load(f)
            elif cat=='MuMu' or cat=='ElEl':
                with open('/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ellipsesScripts/pavementForPValue/pavementForPValue_{0}_part42.json'.format(cat)) as f:
                    parameters = json.load(f)
            else:
                continue
            for j, line in enumerate(parameters, 0): 
                if cat=='MuEl':
                    inWindowCut = "window_ElEl.isInEllipse({0}, {1}, {2}, {3}, {4})".format(float(line[0]), float(line[1]), self.rho, self.jj_str + ".M()", self.baseObject + ".p4.M()")
                    
                    inWindowCut0p5 = "window_ElEl.isInEllipse({1}, {2}, {3}, {4}, {5})".format(cat, float(line[0]), float(line[1]), 0.5, self.jj_str + ".M()", self.baseObject + ".p4.M()")
                    inWindowCut1p0 = "window_ElEl.isInEllipse({1}, {2}, {3}, {4}, {5})".format(cat, float(line[0]), float(line[1]), 1., self.jj_str + ".M()", self.baseObject + ".p4.M()")
                    inWindowCut1p5 = "window_ElEl.isInEllipse({1}, {2}, {3}, {4}, {5})".format(cat, float(line[0]), float(line[1]), 1.5, self.jj_str + ".M()", self.baseObject + ".p4.M()")
                    inWindowCut2p0 = "window_ElEl.isInEllipse({1}, {2}, {3}, {4}, {5})".format(cat, float(line[0]), float(line[1]), 2., self.jj_str + ".M()", self.baseObject + ".p4.M()")
                    inWindowCut2p5 = "window_ElEl.isInEllipse({1}, {2}, {3}, {4}, {5})".format(cat, float(line[0]), float(line[1]), 2.5, self.jj_str + ".M()", self.baseObject + ".p4.M()")
                    inWindowCut3p0 = "window_ElEl.isInEllipse({1}, {2}, {3}, {4}, {5})".format(cat, float(line[0]), float(line[1]), 3., self.jj_str + ".M()", self.baseObject + ".p4.M()")
                else:
                    inWindowCut = "window_{0}.isInEllipse({1}, {2}, {3}, {4}, {5})".format(cat, float(line[0]), float(line[1]), self.rho, self.jj_str + ".M()", self.baseObject + ".p4.M()")

                    inWindowCut0p5 = "window_{0}.isInEllipse({1}, {2}, {3}, {4}, {5})".format(cat, float(line[0]), float(line[1]), 0.5, self.jj_str + ".M()", self.baseObject + ".p4.M()")
                    inWindowCut1p0 = "window_{0}.isInEllipse({1}, {2}, {3}, {4}, {5})".format(cat, float(line[0]), float(line[1]), 1., self.jj_str + ".M()", self.baseObject + ".p4.M()")
                    inWindowCut1p5 = "window_{0}.isInEllipse({1}, {2}, {3}, {4}, {5})".format(cat, float(line[0]), float(line[1]), 1.5, self.jj_str + ".M()", self.baseObject + ".p4.M()")
                    inWindowCut2p0 = "window_{0}.isInEllipse({1}, {2}, {3}, {4}, {5})".format(cat, float(line[0]), float(line[1]), 2., self.jj_str + ".M()", self.baseObject + ".p4.M()")
                    inWindowCut2p5 = "window_{0}.isInEllipse({1}, {2}, {3}, {4}, {5})".format(cat, float(line[0]), float(line[1]), 2.5, self.jj_str + ".M()", self.baseObject + ".p4.M()")
                    inWindowCut3p0 = "window_{0}.isInEllipse({1}, {2}, {3}, {4}, {5})".format(cat, float(line[0]), float(line[1]), 3., self.jj_str + ".M()", self.baseObject + ".p4.M()")

                self.ellCut = self.joinCuts(self.cutWithoutCat, self.dict_cat_cut[cat], inWindowCut)
                
                self.ellCut0p5 = self.joinCuts(self.cutWithoutCat, self.dict_cat_cut[cat], inWindowCut0p5)
                self.ellCut1p0 = self.joinCuts(self.cutWithoutCat, self.dict_cat_cut[cat], inWindowCut1p0)
                self.ellCut1p5 = self.joinCuts(self.cutWithoutCat, self.dict_cat_cut[cat], inWindowCut1p5)
                self.ellCut2p0 = self.joinCuts(self.cutWithoutCat, self.dict_cat_cut[cat], inWindowCut2p0)
                self.ellCut2p5 = self.joinCuts(self.cutWithoutCat, self.dict_cat_cut[cat], inWindowCut2p5)
                self.ellCut3p0 = self.joinCuts(self.cutWithoutCat, self.dict_cat_cut[cat], inWindowCut3p0)
                rho_string = str(self.rho).replace('.','p')
                #Labelling each of the 21 ellipses with its index. Will need to write down which ellipse corresponds to which index.
                #self.tempExtraString = "_inEllipse_{0}_rho{1}".format(j, rho_string) 
                self.tempExtraString = "_inEllipse_{0}".format(j) 
                self.ellExtraString = self.extraString + self.tempExtraString

                self.inEllipse_plot.extend([
                    #{
                    #    'name': 'll_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.ellExtraString, self.systematicString),
                    #    'variable': self.ll_str+".M()",
                    #    'plot_cut': self.ellCut,
                    #    'binning': mll_plot_binning
                    #},
                    #{
                    #    'name': 'Mjj_vs_Mlljj_%s_%s_%s%s'%(self.llFlav, self.suffix, self.ellExtraString, self.systematicString),
                    #    'variable': self.jj_str + '.M() ::: '+self.baseObject + '.p4.M()',
                    #    'plot_cut': self.ellCut,
                    #    'binning': '(150, 0, 1500, 150, 0, 1500)'
                    #},
                    {
                        'name': 'jj_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.ellExtraString+"_inrho"+rho_string, self.systematicString),
                        'variable': self.jj_str + ".M()",
                        'plot_cut': self.ellCut,
                        'binning': '(40, 10, 1000)'
                    },
                    {
                        'name': 'lljj_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.ellExtraString+"_inrho"+rho_string, self.systematicString),
                        'variable': self.baseObject+".p4.M()",
                        'plot_cut': self.ellCut,
                        'binning': '(50, 100, 1500)'
                    },
                    {
                        'name': 'DYweight_%s_%s_%s%s_inrho0p5'%(self.llFlav, self.suffix, self.ellExtraString, self.systematicString),
                        'variable': "computeDYweight({0}, {1})".format(self.jj_str+".M()", self.baseObject+".p4.M()"),
                        'plot_cut': self.ellCut0p5,
                        'binning': '(100, 0.5, 1.5)'
                    },
                    {
                        'name': 'DYweight_%s_%s_%s%s_inrho1p0'%(self.llFlav, self.suffix, self.ellExtraString, self.systematicString),
                        'variable': "computeDYweight({0}, {1})".format(self.jj_str+".M()", self.baseObject+".p4.M()"),
                        'plot_cut': self.ellCut1p0,
                        'binning': '(100, 0.5, 1.5)'
                    },
                    {
                        'name': 'DYweight_%s_%s_%s%s_inrho1p5'%(self.llFlav, self.suffix, self.ellExtraString, self.systematicString),
                        'variable': "computeDYweight({0}, {1})".format(self.jj_str+".M()", self.baseObject+".p4.M()"),
                        'plot_cut': self.ellCut1p5,
                        'binning': '(100, 0.5, 1.5)'
                    },
                    {
                        'name': 'DYweight_%s_%s_%s%s_inrho2p0'%(self.llFlav, self.suffix, self.ellExtraString, self.systematicString),
                        'variable': "computeDYweight({0}, {1})".format(self.jj_str+".M()", self.baseObject+".p4.M()"),
                        'plot_cut': self.ellCut2p0,
                        'binning': '(100, 0.5, 1.5)'
                    },
                    {
                        'name': 'DYweight_%s_%s_%s%s_inrho2p5'%(self.llFlav, self.suffix, self.ellExtraString, self.systematicString),
                        'variable': "computeDYweight({0}, {1})".format(self.jj_str+".M()", self.baseObject+".p4.M()"),
                        'plot_cut': self.ellCut2p5,
                        'binning': '(100, 0.5, 1.5)'
                    },
                    {
                        'name': 'DYweight_%s_%s_%s%s_inrho3p0'%(self.llFlav, self.suffix, self.ellExtraString, self.systematicString),
                        'variable': "computeDYweight({0}, {1})".format(self.jj_str+".M()", self.baseObject+".p4.M()"),
                        'plot_cut': self.ellCut3p0,
                        'binning': '(100, 0.5, 1.5)'
                    },
                ])

                self.tempExtraStringForInOut =  "_{0}".format(j)
                self.extraStringForInOut = self.extraString + self.tempExtraStringForInOut
                self.inOut_plot.extend([
                    #{
                    #    'name': 'rho_steps_histo_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraStringForInOut, self.systematicString),
                    #    'variable': "window_{0}.isInEllipse_noSize({1}, {2}, {3}, {4})".format((cat if cat!='MuEl' else 'ElEl'), line[0], line[1], self.jj_str + ".M()", self.baseObject + ".p4.M()"),
                    #    'plot_cut': self.totalCut,
                    #    'binning': '(6, 0, 3)'
                    #}
                    {
                        'name': 'rho_steps_histo_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraStringForInOut, self.systematicString),
                        'variable': "windows_{0}.at({1}).radius({2}, {3})".format((cat if cat!='MuEl' else 'ElEl'), j, self.jj_str + ".M()", self.baseObject + ".p4.M()"),
                        'plot_cut': self.totalCut,
                        'binning': '(6, 0, 3)'
                    }
            ])

            # FOR SKIMMER
            totalWeight = "event_weight * (%s) * (%s) * (%s) * (%s) * (%s)" % (available_weights["llidiso"], available_weights["pu"], available_weights["trigeff"], available_weights["jjbtag_heavy"], available_weights["jjbtag_light"])
            self.forSkimmer_plot.extend([
                {
                        'name': 'jet1_p4_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet1_str+".p4",
                        'cut': self.totalCut,
                        'type': 'ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiE4D<float>>'
                },
                {
                        'name': 'jet2_p4_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet2_str+".p4",
                        'cut': self.totalCut,
                        'type': 'ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiE4D<float>>'
                },
                {
                        'name': 'lep1_p4_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.lep1_str+".p4",
                        'cut': self.totalCut,
                        'type': 'ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiE4D<float>>'
                },
                {
                        'name': 'lep2_p4_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.lep2_str+".p4",
                        'cut': self.totalCut,
                        'type': 'ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiE4D<float>>'
                },
                {
                        'name': 'lep1_charge_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.lep1_str+".charge",
                        'cut': self.totalCut,
                },
                {
                        'name': 'lep2_charge_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.lep2_str+".charge",
                        'cut': self.totalCut,
                },
                {
                        'name': 'lljj_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".p4.M()",
                        'cut': self.totalCut,
                },
                {
                        'name': 'jj_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jj_str + ".M()",
                        'cut': self.totalCut,
                },
                {
                        'name': 'll_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.ll_str+".M()",
                        'cut': self.totalCut,
                },
                {
                        'name': 'met_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.met_str + ".Pt()",
                        'cut': self.totalCut,
                },
                {
                        'name': 'met_phi_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.met_str+".Phi()",
                        'cut': self.totalCut,
                },
                {
                        'name': 'total_weight_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': totalWeight,
                        'cut': self.totalCut,
                },
            ])


        plotsToReturn = []
        
        for plotFamily in requested_plots:
            
            #if "scaleUncorr" in systematic or "dyScale" in systematic:
            if "scaleUncorr" in systematic:

                # will fail if we can't find the scale index
                scaleIndex = str(int(systematic[-1]))
                
                scaleWeight = "event_scale_weights[%s]" % scaleIndex
                
                for plot in getattr(self, plotFamily + "_plot"):
                    # Two different ways to normalise the variations
                    if "Uncorr" not in systematic:
                        # The normalisation is never applied on data, so we're safe even when applying DY reweighting
                        plot["normalize-to"] = "scale_%s" % scaleIndex
                    if not "Weight" in plotFamily:
                        # Be careful to use 1 for data when applying DY reweighting
                        plot["weight"] = "event_weight" + " * (runOnMC ? " + scaleWeight + " : 1. )"
                        for weight in weights:
                            plot["weight"] += " * " + available_weights[weight]
                    else:
                        print "No other weight than event_weight for ", plotFamily 
                    plotsToReturn.append(plot)
                
            elif "pdf" in systematic:
                
                for plot in getattr(self, plotFamily + "_plot"):
                    if not "Weight" in plotFamily:
                        # Be careful to use 1 for data when applying DY reweighting
                        plot["weight"] = "event_weight" + " * (runOnMC ? " + pdfWeight + " : 1.)"
                        # The normalisation is never applied on data, so we're safe even when applying DY reweighting
                        plot["normalize-to"] = normalization
                        for weight in weights:
                            plot["weight"] += " * " + available_weights[weight]
                    else:
                        print "No other weight than event_weight for ", plotFamily 
                    plotsToReturn.append(plot)
            
            else:
                
                for plot in getattr(self, plotFamily + "_plot"):
                    if not "Weight" in plotFamily and "sample_weight" not in plot["name"]:
                        plot["weight"] = "event_weight"
                        # The normalisation is never applied on data, so we're safe even when applying DY reweighting
                        plot["normalize-to"] = normalization
                        for weight in weights:
                            plot["weight"] += " * " + available_weights[weight]
                    else:
                        # Divide by sample_weight since we cannot avoid it in histFactory
                        plot["weight"] = "event_weight/__sample_weight"
                        print "No other weight than event_weight for ", plotFamily 
                    plotsToReturn.append(plot)

        # If requested, do NOT force weights to 1 for data
        if allowWeightedData:
            for plot in plotsToReturn:
                plot["allow-weighted-data"] = True

        # Remove possible duplicates (same name => they would be overwritten when saving the output file anyway)
        cleanedPlotList = []
        checkedNames = []
        for p in plotsToReturn:
            if p["name"] not in checkedNames:
                checkedNames.append(p["name"])
                cleanedPlotList.append(p)
        if len(plotsToReturn) - len(cleanedPlotList) < 0:
            print("Warning: removed {} duplicate plots!".format(-len(plotsToReturn) + len(cleanedPlotList)))

        return cleanedPlotList


    def joinCuts(self, *cuts):
        if len(cuts) == 0:
            return ""
        elif len(cuts) == 1:
            return cuts[0]
        else:
            totalCut = "("
            for cut in cuts:
                cut = cut.strip().strip("&")
                if cut == "":
                    continue
                totalCut += "(" + cut + ")&&" 
            totalCut = totalCut.strip("&") + ")"
            return totalCut

