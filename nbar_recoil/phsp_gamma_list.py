#!/usr/bin/env python3

import basf2 as b2
import modularAnalysis as ma
import variables.collections as vc
import variables.utils as vu
from variables import variables as vm

main = b2.Path()

#carico il file del MC
ma.inputMdstList(filelist=["../../root_file/nbar_recoil/my_mdst_output.root"],path=main)

# Ricostruzione delle particelle visibili

ma.fillParticleListFromMC("gamma:MC", "", path=main)

#ma.matchMCTruth("gamma:all", path=main)

#Def some variables

b_vars = vc.kinematics + vc.mc_kinematics + ['mcISR', 'mcPDG', 'genMotherPDG','phi','theta','mcPhi','mcTheta']


ma.variablesToNtuple("gamma:MC",variables=b_vars,filename="../../root_file/nbar_recoil/phsp_list_gamma_MC.root",treename="tree",path=main,)


b2.process(main)

print(b2.statistics)
