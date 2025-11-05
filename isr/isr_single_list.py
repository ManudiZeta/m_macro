#!/usr/bin/env python3

import basf2 as b2
import modularAnalysis as ma
import variables.collections as vc
import variables.utils as vu
from variables import variables as vm
import sys
from variables.MCGenTopo import mc_gen_topo

main = b2.Path()

lista = "MC"
ma.inputMdstList(filelist=["../../root_file/isr/channel_JPsi/isrVEC_output_4S.root"],path=main)

ma.fillParticleListFromMC(f"p+:{lista}", "", path=main)
ma.fillParticleListFromMC(f"pi-:{lista}", "", path=main)
ma.fillParticleListFromMC(f"anti-n0:{lista}", "", path=main)

#ma.fillParticleListFromMC(f"J/psi:{lista}", "", path=main)
ma.reconstructMCDecay(f"J/psi:{lista} -> p+:{lista} pi-:{lista} anti-n0:{lista}",cut="",path=main)

#ma.matchMCTruth("anti-n0:MC", path=main)

#Def some variables

b_vars = vc.kinematics + vc.mc_kinematics + ['mcISR', 'mcPDG', 'genMotherPDG','M','phi','theta','mcPhi','mcTheta']

cuts = "genMotherPDG == 300553"

ma.applyCuts(f"J/psi:{lista}", cuts, path=main)

ma.variablesToNtuple(f"J/psi:{lista}",variables=b_vars,filename=f"../../root_file/isr/channel_JPsi/isrVEC_list_Jpsi_{lista}.root",treename="tree",path=main,)
#ma.variablesToNtuple("gamma:MC",variables=mc_gen_topo(200),filename=f"../../root_file/isr/isr_TOPO/isrVEC_list_gamma_MC_Jpsi.root",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)
