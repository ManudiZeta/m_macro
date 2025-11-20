#!/usr/bin/env python3

import basf2 as b2
import modularAnalysis as ma
import variables.collections as vc
import variables.utils as vu
from variables import variables as vm
import sys
from variables.MCGenTopo import mc_gen_topo

main = b2.Path()

part= "gamma"
lista = "MC"

ma.inputMdstList(filelist=["../../root_file/isr/channel_std/isrPhok_output_F100k.root"],path=main)

'''
ma.fillParticleListFromMC(f"p+:{lista}", "", path=main)
ma.fillParticleListFromMC(f"pi-:{lista}", "", path=main)
ma.fillParticleListFromMC(f"anti-n0:{lista}", "", path=main)
'''

ma.fillParticleListFromMC(f"{part}:{lista}", "", path=main)
#ma.reconstructMCDecay(f"J/psi:{lista} -> p+:{lista} pi-:{lista} anti-n0:{lista}",cut="",path=main)

#ma.matchMCTruth("anti-n0:MC", path=main)

#Def some variables

b_vars = vc.kinematics + vc.mc_kinematics + ['mcISR', 'mcPDG', 'genMotherPDG','M','phi','theta','mcPhi','mcTheta']
vm.addAlias("p_CMS","useCMSFrame(p)")
b_vars = b_vars + ["p_CMS"]

cuts = "mcISR == 1"

ma.applyCuts(f"{part}:{lista}", cuts, path=main)

ma.variablesToNtuple(f"{part}:{lista}",variables=b_vars,filename=f"../../root_file/isr/channel_JPsi/isrVEC_list_{part}_{lista}.root",treename="tree",path=main,)
ma.variablesToNtuple(f"{part}:{lista}",variables=mc_gen_topo(200),filename=f"../../root_file/isr/isr_TOPO/isrVEC_list_Jpsi_{lista}.root",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)
