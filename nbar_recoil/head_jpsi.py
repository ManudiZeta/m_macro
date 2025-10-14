#!/usr/bin/env python3

import basf2 as b2
import modularAnalysis as ma
import variables.collections as vc
import variables.utils as vu
import sys
from variables import variables as vm
from variables.MCGenTopo import mc_gen_topo


choice = int(sys.argv[1]) # 0 = with photon, otherwise = without photon

main = b2.Path()
ma.inputMdstList(filelist=["../../root_file/nbar_recoil/my_mdst_output_Jpsi.root"],path=main)

lista = "REC"

ma.fillParticleList(f"p+:{lista}", "", path=main) 
ma.fillParticleList(f"pi-:{lista}", "", path=main)
ma.fillParticleList(f"anti-n0:{lista}", "", path=main)

ma.reconstructDecay(f"vpho:list_rec ->  p+:{lista} pi-:{lista}", cut=" ", path=main)
ma.reconstructDecay(f"J/psi:list_rec ->  vpho:list_rec anti-n0:{lista}", cut=" ", path=main)

if choice == 0:
    title = "gamma"
    print("*** PHSP events WITH gamma in RecDecay *** \n")
    ma.fillParticleList(f"gamma:{lista}", "", path=main)
    ma.reconstructDecay(f"Upsilon(4S):list_rec -> J/psi:list_rec gamma:{lista}", cut=" ", path=main)

else:
    title = "no_gamma"
    print("*** PHSP events WITHOUT gamma in RecDecay *** \n")
    ma.reconstructDecay(f"Upsilon(4S):list_rec -> J/psi:list_rec", cut=" ", path=main)


ma.matchMCTruth("Upsilon(4S):list_rec", path=main)

g_vars = vc.kinematics + vc.mc_kinematics + ['mcISR', 'mcPDG', 'genMotherPDG','phi','theta','mcPhi','mcTheta' , 'mcPrimary']

daug_vars = ['isSignal','PDG','mcPDG', 'genMotherPDG','genMotherID','M','p','E','phi','theta','mcPhi','mcTheta','mcP','mcE', 'clusterE','clusterUncorrE']

b_vars = vc.kinematics + vc.mc_kinematics + ['isSignal'] + vc.recoil_kinematics
if choice == 0:

    b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, "Upsilon(4S) -> [^J/psi -> [^vpho -> ^p+ ^pi-] ^anti-n0] ^gamma", prefix = ["Jpsi", "vpho", "p", "pi", "nbar", "gamma"] )

    #b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, "Upsilon(4S) -> [J/psi -> [vpho -> ^p+ ^pi-] anti-n0] gamma", prefix = ["p", "pi"] )
else:
    b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, "Upsilon(4S) -> [^J/psi -> [^vpho -> ^p+ ^pi-] ^anti-n0]", prefix = ["Jpsi", "vpho", "p", "pi", "nbar"] )

    #b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, "Upsilon(4S) -> [J/psi -> [vpho -> ^p+ ^pi-] anti-n0]", prefix = ["p", "pi"] )

b_vars = b_vars + vu.create_aliases_for_selected(vc.recoil_kinematics, "Upsilon(4S) -> [J/psi -> [^vpho -> p+ pi-] anti-n0]", prefix = ["vpho"] )

'''
vm.addAlias("fir_arg","formula(sin(vpho_pRecoilTheta)*sin(nbar_theta)*cos(vpho_pRecoilPhi-nbar_phi))")
vm.addAlias("sec_arg","formula(cos(vpho_pRecoilTheta)*cos(nbar_theta))")
vm.addAlias("alpha","formula(acos(fir_arg + sec_arg))")

ma.rankByLowest("vpho:gen", "alpha", numBest=1, path=main)

b_vars = b_vars + ['alpha']
'''

if choice == 0:
    sig_cuts = "Jpsi_genMotherPDG == 300553 and gamma_genMotherPDG == 300553 and p_mcPDG == 2212 and pi_mcPDG == -211 and gamma_mcPDG == 22" 
else:
    sig_cuts = "Jpsi_genMotherPDG == 300553 and p_mcPDG == 2212 and pi_mcPDG == -211"  

dad_cuts = "p_genMotherPDG == 443 and pi_genMotherPDG == 443 " #è giusto o provengono da vpho (10022) a livello di generatore? giusto 443, infatti non vi sono entries per 10022 quando non applico i tagli
n0_cuts = "nbar_genMotherPDG == 443" #stesso discorso qui
cuts= sig_cuts + " and " + dad_cuts + " and " + n0_cuts
#cuts= n0_cuts + " and " + dad_cuts
#print(" *** ", cuts, " *** ")

ma.applyCuts("Upsilon(4S):list_rec",cuts, path=main)


ma.variablesToNtuple("Upsilon(4S):list_rec",variables=b_vars,filename=f"../../root_file/nbar_recoil/vpho_Jpsi_{title}_{lista}.root",treename="tree",path=main,)
ma.variablesToNtuple("Upsilon(4S):list_rec",variables=mc_gen_topo(200),filename=f"../../root_file/nbar_recoil/phsp_TOPO/vpho_Jpsi_phsp_{title}_{lista}_TOPO.root",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)
