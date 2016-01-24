

class options_():

    '''
    ### Define 2D mapping for the search in the M(bb) - M(llbb) plane ###
    rangeMassA = []
    mbb=10
    sigma=1.0
    for i in range(1,36):
      dmbb=0.15*mbb*1.5
      step_mbb = sigma*0.15*mbb
      rangeMassA.append([int(mbb-dmbb),int(mbb+dmbb),int(mbb)])
      mbb+=step_mbb

    rangeMassH = []
    mllbb=10
    for i in range(1,36):
      dmllbb=0.15*mllbb*1.5
      step_mllbb = dmllbb/1.5
      rangeMassH.append([int(mllbb-dmllbb),int(mllbb+dmllbb),int(mllbb)])
      mllbb+=step_mllbb
    '''

    mbb_list = {50,100,200,300}
    mllbb_list = {150,300,500,800}

    rangeMassA = []
    rangeMassH = []

    for mbb in mbb_list :
      dmbb=0.15*mbb*1.5
      rangeMassA.append([int(mbb-dmbb),int(mbb+dmbb),int(mbb)])

    for mllbb in mllbb_list :
      dmllbb=0.15*mllbb*1.5
      rangeMassH.append([int(mllbb-dmllbb),int(mllbb+dmllbb),int(mllbb)])
        

    # creating cuts 

    cut = {}
    mA_list = {}
    mA_list_down = {}
    mA_list_up = {}
    mH_list = {}
    mH_list_down = {}
    mH_list_up = {}

    for mA in rangeMassA:
        for mH in rangeMassH:
            key = "mA"+str(mA[0])+"to"+str(mA[1])+"_mH"+str(mH[0])+"to"+str(mH[1])
            cut[key] = "( Length$(za_diJets) > 0 && Length$(za_diLepDiJets) > 0 && za_diJets[0].p4.M() >= "+str(mA[0])+" && za_diJets[0].p4.M() < "+str(mA[1])+" && za_diLepDiJets[0].p4.M() >= "+str(mH[0])+" && za_diLepDiJets[0].p4.M() < "+str(mH[1])+" )"
            mA_list[key] = mA[2]
            mA_list_down[key] = mA[0]
            mA_list_up[key] = mA[1]
            mH_list[key] = mH[2]
            mH_list_down[key] = mH[0]
            mH_list_up[key] = mH[1]
