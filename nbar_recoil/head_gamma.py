#!/usr/bin/env python3

import basf2 as b2
import modularAnalysis as ma
import variables.collections as vc
import variables.utils as vu

main = b2.Path()

#carico il file del MC
ma.inputMdstList(filelist=["../../root_file/nbar_recoil/my_mdst_output.root"],path=main)

# Ricostruzione delle particelle visibili
ma.fillParticleList("p+:all", "", path=main) 
ma.fillParticleList("pi-:all", "", path=main)
ma.fillParticleList("gamma:all", "", path=main)
ma.fillParticleList("gamma:rec", "", path=main) #neutral list with gamma hp
#ma.fillParticleListFromMC("anti-n0:mc", "", path=main) 

# Ricostruzione vpho 
ma.reconstructDecay("vpho:list_rec -> p+:all pi-:all gamma:all",cut="",path=main)

# Ricostruzione U(4S)
ma.reconstructDecay("Upsilon(4S):list_rec -> vpho:list_rec gamma:rec ",cut="",path=main)

ma.matchMCTruth("Upsilon(4S):list_rec", path=main)

#Def some variables

b_vars = vc.kinematics + vc.mc_kinematics + ['isSignal'] + vc.recoil_kinematics

daug_vars = ['isSignal','PDG','mcPDG', 'genMotherPDG','genMotherID','M','p','E','phi','theta','mcPhi','mcTheta','mcP','mcE', 'clusterE','clusterUncorrE']

# Guardo le grandezze di (p, pi-,gamma, gamma) relative al decadimento della 4S
b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, "Upsilon(4S) -> [vpho -> ^p+ ^pi- ^gamma] ^gamma:rec")
# Guardo le grandezze di vpho per trovare le variabili di recoil
b_vars = b_vars + vu.create_aliases_for_selected(vc.recoil_kinematics, "Upsilon(4S) -> [^vpho -> p+ pi- gamma] gamma:rec")

#cmskinematics = vu.create_aliases(vc.kinematics + ['InvM','mRecoil','eRecoil'], "useCMSFrame({variable})", "CMS")
#b_vars = b_vars + cmskinematics

print(b_vars)

sig_cuts = "vpho_p_isSignal == 1 and vpho_pi_isSignal == 1 and vpho_gamma_isSignal == 1" 
dad_cuts = "vpho_p_genMotherPDG == 300553 and vpho_pi_genMotherPDG == 300553 and vpho_gamma_genMotherPDG== 300553"
gamma_cuts = "gamma_isSignal == 1 and gamma_genMotherPDG == 300553"
cuts= sig_cuts + " and " + dad_cuts + " and " + gamma_cuts
print(" *** ", cuts, " *** ")

ma.applyCuts("Upsilon(4S):list_rec", cuts, path=main)

ma.variablesToNtuple("Upsilon(4S):list_rec",variables=b_vars,filename="../../root_file/nbar_recoil/vpho_p_pi_gamma.root",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)
