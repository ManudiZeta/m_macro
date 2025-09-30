#!/usr/bin/env python3

import basf2 as b2
import modularAnalysis as ma
import variables.collections as vc
import variables.utils as vu
from variables import variables as vm

main = b2.Path()

ma.inputMdstList(filelist=["../../root_file/isr/isr_output.root"],path=main)

# Ricostruzione delle particelle visibili
ma.fillParticleListFromMC("p+:MC", "", path=main) 
ma.fillParticleListFromMC("pi-:MC", "", path=main)
ma.fillParticleListFromMC("anti-n0:MC", "", path=main)
ma.fillParticleListFromMC("gamma:MC", "", path=main) # "tutti" because "all" is protected from further cuts


ma.reconstructDecay("vpho:list_rec -> p+:MC pi-:MC gamma:MC",cut="",path=main)
ma.reconstructDecay("vpho:gen -> vpho:list_rec anti-n0:MC ",cut="",path=main)

ma.matchMCTruth("vpho:gen", path=main)

#Variables
g_vars = vc.kinematics + vc.mc_kinematics + ['mcISR', 'mcPDG', 'genMotherPDG','phi','theta','mcPhi','mcTheta' , 'mcPrimary']

b_vars = vc.kinematics + vc.mc_kinematics + ['isSignal'] + vc.recoil_kinematics

daug_vars = ['isSignal','PDG','mcPDG', 'genMotherPDG','genMotherID','M','p','E','phi','theta','mcPhi','mcTheta','mcP','mcE', 'clusterE','clusterUncorrE']


b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, "vpho:gen -> [vpho:list_rec -> ^p+ ^pi- ^gamma] ^anti-n0", prefix = ["p", "pi", "gamma", "nbar"])

b_vars = b_vars + vu.create_aliases_for_selected(vc.recoil_kinematics, "vpho:gen -> [^vpho:list_rec -> p+ pi- gamma] anti-n0", prefix = ["vpho"])

b_vars = b_vars + vu.create_aliases_for_selected(g_vars, "vpho:gen -> [vpho:list_rec -> p+ pi- ^gamma] anti-n0", prefix = ["gamma"])


"""
vm.addAlias("fir_arg","formula(sin(vpho_pRecoilTheta)*sin(n0_theta)*cos(vpho_pRecoilPhi-n0_phi))")
vm.addAlias("sec_arg","formula(cos(vpho_pRecoilTheta)*cos(n0_theta))")
vm.addAlias("alpha","formula(acos(fir_arg + sec_arg))")

ma.rankByLowest("Upsilon(4S):list_rec", "alpha", numBest=1, path=main)

b_vars = b_vars + ['alpha'] 
"""

#cmskinematics = vu.create_aliases(vc.kinematics + ['InvM','mRecoil','eRecoil'], "useCMSFrame({variable})", "CMS")
#b_vars = b_vars + cmskinematics
#print(b_vars)

sig_cuts = "vpho_mRecoil>0 and vpho_mRecoil <2 and p_mcPDG == 2212 and pi_mcPDG == -211 and gamma_mcPDG == 22" 
dad_cuts = "p_genMotherPDG == 10022 and pi_genMotherPDG == 10022"
n0_cuts = "nbar_genMotherPDG == 10022"
cuts= sig_cuts + " and " + dad_cuts + " and " + n0_cuts
print(" *** ", cuts, " *** ")

ma.applyCuts("vpho:gen", cuts, path=main)


ma.variablesToNtuple("vpho:gen",variables=b_vars,filename="../../root_file/isr/vpho_isr.root",treename="tree",path=main,)


b2.process(main)

print(b2.statistics)
