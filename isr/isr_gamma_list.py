#!/usr/bin/env python3

import basf2 as b2
import modularAnalysis as ma
import variables.collections as vc
import variables.utils as vu
from variables import variables as vm
import sys
from variables.MCGenTopo import mc_gen_topo

main = b2.Path()

#carico il file del MC
ma.inputMdstList(filelist=["../../root_file/isr/isr_output_Jpsi_test.root"],path=main)

# Ricostruzione delle particelle visibili

ma.fillParticleListFromMC("p+:MC", "", path=main)

#ma.matchMCTruth("anti-n0:MC", path=main)


#Def some variables

b_vars = vc.kinematics + vc.mc_kinematics + ['mcISR', 'mcPDG', 'genMotherPDG','phi','theta','mcPhi','mcTheta']

cuts = "genMotherPDG == 443"

ma.applyCuts("p+:MC", cuts, path=main)

ma.variablesToNtuple("p+:MC",variables=b_vars,filename="../../root_file/isr/isr_list_n_MC_Jpsi.root",treename="tree",path=main,)
ma.variablesToNtuple("p+:MC",variables=mc_gen_topo(200),filename=f"../../root_file/isr/isr_TOPO/isr_list_n_MC_Jpsi.root",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)
