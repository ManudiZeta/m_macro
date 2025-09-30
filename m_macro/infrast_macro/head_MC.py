#!/usr/bin/env python3

import basf2 as b2
import modularAnalysis as ma
import variables.collections as vc
import variables.utils as vu

main = b2.Path()

#carico il file del MC
ma.inputMdstList(filelist=[b2.find_file("../root_file/my_mdst_output.root")],path=main)

sig_cuts = "mRecoil>0 and mRecoil <2 and p_isSignal == 1 and pi_isSignal == 1 and gamma_isSignal == 1" 
dad_cuts = "p_genMotherPDG == 300553 and pi_genMotherPDG == 300553 and gamma_genMotherPDG== 300553"
cuts= sig_cuts + " and " + dad_cuts
print(" *** ", cuts, " *** ")

# Ricostruzione delle particelle visibili
ma.fillParticleListFromMC("p+:mc", "", path=main)
ma.fillParticleListFromMC("pi-:mc", "", path=main)
ma.fillParticleListFromMC("gamma:mc", "", path=main)
#ma.fillParticleListFromMC("anti-n0:all", "", path=main)

# Ricostruzione vpho con particella mancante (cioè senza n0-bar)
ma.reconstructDecay("vpho -> p+:mc pi-:mc gamma:mc",cut="",path=main)
#ma.reconstructDecay("vpho:gen -> vpho:all anti-n0:all ",cut="",path=main)

ma.matchMCTruth("vpho", path=main)

b_vars = vc.kinematics + vc.mc_kinematics + ['isSignal'] + vc.recoil_kinematics

daug_vars = ['isSignal','PDG', 'genMotherPDG','genMotherID','mcPhi','mcTheta','p']

#b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, "vpho:gen -> ^vpho ^anti-n0")
b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, "vpho -> ^p+ ^pi- ^gamma ")

#cmskinematics = vu.create_aliases(vc.kinematics + ['InvM','mRecoil','eRecoil'], "useCMSFrame({variable})", "CMS")
#b_vars = b_vars + cmskinematics

print(b_vars)

ma.applyCuts("vpho", cuts, path=main)

ma.variablesToNtuple("vpho",variables=b_vars,filename="../root_file/vpho_p_pi_n_MC.root",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)
