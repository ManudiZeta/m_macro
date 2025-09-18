#!/usr/bin/env python3

import sys 
import basf2 as b2 
import modularAnalysis as ma #permette di fare analisi, creare particelle etc...
import variables.collections as vc
import variables.utils as vu


main = b2.Path()

#carico il file del MC
ma.inputMdstList(filelist=["root_file/my_mdst_output_Jpsi.root"],path=main)

# Ricostruzione delle particelle visibili
ma.fillParticleList("p+:all", "", path=main) 
ma.fillParticleList("pi-:all", "", path=main)
ma.fillParticleList("gamma:all", "", path=main)
ma.fillParticleList("anti-n0:all", "", path=main)
#ma.fillParticleListFromMC("anti-n0:mc", "", path=main) 

# combine final state particles to form composite particles--->combino gli e-e+ dello stato finale per ricondurli al decadimento di una J/psi

ma.reconstructDecay("vpho:list_rec ->  p+:all pi-:all", cut=" ", path=main)
ma.reconstructDecay("J/psi:list_rec ->  vpho:list_rec anti-n0:all", cut=" ", path=main)
ma.reconstructDecay("Upsilon(4S):list_rec -> J/psi:list_rec gamma:all", cut=" ", path=main)

ma.matchMCTruth("Upsilon(4S):list_rec", path=main)


#Def some variables

b_vars = vc.kinematics + vc.mc_kinematics + ['isSignal'] #+ vc.recoil_kinematics

daug_vars = ['isSignal','PDG','mcPDG', 'genMotherPDG','genMotherID','M','p','E','phi','theta','mcPhi','mcTheta','mcP','mcE', 'clusterE','clusterUncorrE']

b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, "Upsilon(4S) -> ^J/psi  ^gamma")
b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, "Upsilon(4S) -> [J/psi -> vpho ^anti-n0] gamma")
b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, "Upsilon(4S) -> [J/psi -> [vpho -> ^p+ ^pi-] anti-n0] gamma")
b_vars = b_vars + vu.create_aliases_for_selected(vc.recoil_kinematics, "J/psi -> [^vpho -> p+ pi-] anti-n0")

#b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, "J/psi -> [vpho -> ^p+ ^pi-]  ^anti-n0")
#b_vars = b_vars + vu.create_aliases_for_selected(vc.recoil_kinematics, "J/psi -> [^vpho -> p+ pi-] anti-n0")

print(b_vars)
sig_cuts = "Jpsi_genMotherPDG == 300553 and gamma_genMotherPDG == 300553" 
pdg_cuts = "Jpsi_vpho_p_mcPDG == 2212 and Jpsi_vpho_pi_mcPDG == -211 "
dad_cuts = "Jpsi_vpho_p_genMotherPDG == 443 and Jpsi_vpho_pi_genMotherPDG == 443 "
n0_cuts = "Jpsi_n0_genMotherPDG == 443"
#cuts= sig_cuts + " and " + dad_cuts #+ " and " + n0_cuts
#cuts= sig_cuts + " and " + n0_cuts + " and " + dad_cuts + " and " + pdg_cuts
cuts= n0_cuts + " and " + dad_cuts
#print(" *** ", cuts, " *** ")

ma.applyCuts("Upsilon(4S):list_rec",cuts, path=main)

ma.variablesToNtuple("Upsilon(4S):list_rec",variables=b_vars,filename="root_file/vpho_Jpsi_gamma.root",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)
