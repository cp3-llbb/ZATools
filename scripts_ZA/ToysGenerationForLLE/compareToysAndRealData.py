import ROOT
import argparse


parser = argparse.ArgumentParser(description='Generate toys from smoothed histogram') 
parser.add_argument('-cat', '--category', action='store', type=str, help='Category that you want to process. Can be either MuMu, ElEl, or MuEl.')
options = parser.parse_args()

cat = options.category

for partIndex in range(1,2): #9 parts

    print "Opening file"
    #f_data = ROOT.TFile.Open("haddedDataToTest/data_all_{0}_part{1}_pointsOfPvalueScan.root".format(cat, partIndex)) #WRONG, you should compare to data but to the smoothed MC, because this is where all the toys are generated from
    #f_data = ROOT.TFile.Open("haddedDataToTest/data_all_{0}_part{1}_pointsOfPvalueScan.root".format(cat, partIndex))
    f_data = ROOT.TFile.Open("haddedDataToTest/bkg_all_part{0}.root".format(partIndex))
    print "File opened"
    for i in range(20):
        f_data.Get("rho_steps_histo_{0}_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{1}".format(cat,i)).Scale(35922)

    for toyindex in range(2,3):
        f_nonRandom = ROOT.TFile.Open("{0}/toys/pointsOfPvalueScan/nonRandomHisto_toy{1}_part{2}.root".format(cat,toyindex,partIndex)) #not dependent on the toy, always the same
        print "toyIndex: ", toyindex
        #f_toy = ROOT.TFile.Open("haddedDataToTest/bkg_all_part{0}.root".format(partIndex))
        f_toy = ROOT.TFile.Open("{0}/toys/pointsOfPvalueScan/toy{1}_part{2}_histos.root".format(cat,toyindex, partIndex))
        #f_toy = ROOT.TFile.Open("TOYS_pointsOfPvalueScan/TOY_{0}/part{1}/MuonEG_toy{0}_part{1}.root".format(toyindex, partIndex))
        #f_toy = ROOT.TFile.Open("/nfs/scratch/fynu/asaggio/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA/ToysGenerationForLLE/TOYS_pointsOfPvalueScan/TOY0_ONLYFORPLOT/DoubleEG_toy{0}_part{1}.root".format(toyindex, partIndex)) #CORRECT
        #f_toy = ROOT.TFile.Open("{0}/toys/207_sim_masspoints/toy{1}_part{2}.root".format(cat, toyindex, partIndex))
        #f_toy = ROOT.TFile.Open("{0}/toys/toy{1}_part{2}_histosTEST.root".format(cat, toyindex, partIndex))
        h_toys = []
        h_data = []

        n_ellipses = 20 #Plot first 10 ellipses

        for j in range(n_ellipses):
            print "Ellipse # ", j
            h_toys.append(f_toy.Get("rho_steps_histo_{0}_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{1}".format(cat,j)))
            h_data.append(f_data.Get("rho_steps_histo_{0}_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{1}".format(cat,j)))

            print "base: ", f_nonRandom.Get("rho_steps_histo_{0}_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{1}".format(cat,j)).GetBinContent(5)
            print "toy: ", f_toy.Get("rho_steps_histo_{0}_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{1}".format(cat,j)).GetBinContent(5)
            print "MC: ", f_data.Get("rho_steps_histo_{0}_hZA_lljj_deepCSV_btagM_mll_and_met_cut_{1}".format(cat,j)).GetBinContent(5)
            print "----"

        for i in range(n_ellipses):
            print "Draw ellipse # ", i
            c = ROOT.TCanvas("c","c",800,600)
            h_toys[i].Draw("")
            h_toys[i].SetMaximum(1000 if cat=="MuMu" else 400)
            h_toys[i].SetLineColor(ROOT.kRed)
            h_data[i].Draw("same")
            h_data[i].SetMaximum(1000 if cat=="MuMu" else 400)
            h_data[i].SetLineColor(ROOT.kBlack)
            print "bkg: ",h_data[i].Integral(1,7), "toy: ", h_toys[i].Integral(1,7)
            c.SaveAs("compareToysAndData_ell{0}_toyNumber{1}_part{2}_{3}.png".format(i,toyindex,partIndex,cat))  #FIXME go back to this
            #c.SaveAs("compareToysAndData_ell{0}_part{1}.png".format(i,partIndex))
            del c

        del h_toys[:]
        del h_data[:]


