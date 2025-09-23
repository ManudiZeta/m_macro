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
ma.fillParticleList("p+:all", "", path=main) 
ma.fillParticleList("pi-:all", "", path=main)
ma.fillParticleList("gamma:all", "", path=main)
ma.fillParticleList("anti-n0:all", "", path=main)
#ma.fillParticleListFromMC("anti-n0:mc", "", path=main) 

# Ricostruzione vpho con particella mancante (cioè senza n0-bar)
ma.reconstructDecay("vpho:list_rec -> p+:all pi-:all gamma:all",cut="",path=main)

# Ricostruzione U(4S) con n0-bar_rec
ma.reconstructDecay("Upsilon(4S):list_rec -> vpho:list_rec anti-n0:all ",cut="",path=main)

ma.matchMCTruth("Upsilon(4S):list_rec", path=main)

#Def some variables

b_vars = vc.kinematics + vc.mc_kinematics + ['isSignal'] + vc.recoil_kinematics

daug_vars = ['isSignal','PDG','mcPDG', 'genMotherPDG','genMotherID','M','p','E','phi','theta','mcPhi','mcTheta','mcP','mcE', 'clusterE','clusterUncorrE']

# Guardo le grandezze di (p, pi-,gamma, n0bar) relative al decadimento della 4S
b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, "Upsilon(4S) -> [vpho -> ^p+ ^pi- ^gamma] ^anti-n0")
# Guardo le grandezze di vpho per trovare le variabili di recoil
b_vars = b_vars + vu.create_aliases_for_selected(vc.recoil_kinematics, "Upsilon(4S) -> [^vpho -> p+ pi- gamma] anti-n0")

vm.addAlias("fir_arg","formula(sin(vpho_pRecoilTheta)*sin(n0_theta)*cos(vpho_pRecoilPhi-n0_phi))")
vm.addAlias("sec_arg","formula(cos(vpho_pRecoilTheta)*cos(n0_theta))")
vm.addAlias("alpha","formula(acos(fir_arg + sec_arg))")

ma.rankByLowest("Upsilon(4S):list_rec", "alpha", numBest=1, path=main)

#vm.addAlias("rank", "extraInfo(alpha_rank)") #what is this??

b_vars = b_vars + ['alpha']


#cmskinematics = vu.create_aliases(vc.kinematics + ['InvM','mRecoil','eRecoil'], "useCMSFrame({variable})", "CMS")
#b_vars = b_vars + cmskinematics

print(b_vars)

sig_cuts = "vpho_mRecoil>0 and vpho_mRecoil <2 and vpho_p_mcPDG == 2212 and vpho_pi_mcPDG == -211 and vpho_gamma_mcPDG == 22" 
dad_cuts = "vpho_p_genMotherPDG == 300553 and vpho_pi_genMotherPDG == 300553 and vpho_gamma_genMotherPDG== 300553"
n0_cuts = "n0_genMotherPDG == 300553"
cuts= sig_cuts + " and " + dad_cuts + " and " + n0_cuts
print(" *** ", cuts, " *** ")

ma.applyCuts("Upsilon(4S):list_rec", cuts, path=main)

ma.variablesToNtuple("Upsilon(4S):list_rec",variables=b_vars,filename="../../root_file/nbar_recoil/vpho_p_pi_n.root",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)
