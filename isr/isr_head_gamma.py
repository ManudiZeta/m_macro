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
ma.inputMdstList(filelist=["../../root_file/isr/isr_output.root"],path=main)

lista = "REC"

# Ricostruzione delle particelle visibili
ma.fillParticleList(f"p+:{lista}", "", path=main) 
ma.fillParticleList(f"pi-:{lista}", "", path=main)
ma.fillParticleList(f"gamma:nb", "", path=main)

if choice == 0:
    title = "gamma"
    print("*** ISR events WITH gamma in RecDecay *** \n")

    ma.fillParticleList(f"gamma:{lista}", "", path=main) # "tutti" because "all" is protected from further cuts
    ma.reconstructDecay(f"vpho:list_rec -> p+:{lista} pi-:{lista} gamma:{lista}",cut="",path=main)
else:
    title = "no_gamma"
    print("*** ISR events WITHOUT gamma in RecDecay *** \n")

    ma.reconstructDecay(f"vpho:list_rec -> p+:{lista} pi-:{lista}",cut="",path=main)

ma.reconstructDecay(f"vpho:gen -> vpho:list_rec gamma:nb",cut="",path=main)

ma.matchMCTruth("vpho:gen", path=main)

#Variables
g_vars = vc.kinematics + vc.mc_kinematics + ['mcISR', 'mcPDG', 'genMotherPDG','phi','theta','mcPhi','mcTheta' , 'mcPrimary']

b_vars = vc.kinematics + vc.mc_kinematics + ['isSignal'] + vc.recoil_kinematics

daug_vars = ['isSignal','PDG','mcPDG', 'genMotherPDG','genMotherID','M','p','E','phi','theta','mcPhi','mcTheta','mcP','mcE', 'clusterE','clusterUncorrE']

if choice == 0: 
    b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, f"vpho:gen -> [vpho:list_rec -> ^p+ ^pi- ^gamma:{lista}] ^gamma:nb", prefix = ["p", "pi", "gamma", "nb_gamma"])

    b_vars = b_vars + vu.create_aliases_for_selected(vc.recoil_kinematics, f"vpho:gen -> [^vpho:list_rec -> p+ pi- gamma:{lista}] gamma:nb", prefix = ["vpho"])

    b_vars = b_vars + vu.create_aliases_for_selected(g_vars, "vpho:gen -> [vpho:list_rec -> p+ pi- ^gamma:{lista] gamma:nb", prefix = ["gamma"])

else:
    b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, "vpho:gen -> [vpho:list_rec -> ^p+ ^pi-] ^gamma:nb", prefix = ["p", "pi", "nb_gamma"])

    b_vars = b_vars + vu.create_aliases_for_selected(vc.recoil_kinematics, "vpho:gen -> [^vpho:list_rec -> p+ pi-] gamma:nb", prefix = ["vpho"])

vm.addAlias("fir_arg","formula(sin(vpho_pRecoilTheta)*sin(nb_gamma_theta)*cos(vpho_pRecoilPhi-nb_gamma_phi))")
vm.addAlias("sec_arg","formula(cos(vpho_pRecoilTheta)*cos(nb_gamma_theta))")
vm.addAlias("alpha","formula(acos(fir_arg + sec_arg))")

ma.rankByLowest("vpho:gen", "alpha", numBest=1, path=main)

b_vars = b_vars + ['alpha']


#cmskinematics = vu.create_aliases(vc.kinematics + ['InvM','mRecoil','eRecoil'], "useCMSFrame({variable})", "CMS")
#b_vars = b_vars + cmskinematics
#print(b_vars)

if choice == 0: 
    sig_cuts = "vpho_mRecoil>0 and vpho_mRecoil <2 and p_mcPDG == 2212 and pi_mcPDG == -211 and gamma_mcPDG == 22" 
else:
    sig_cuts = "vpho_mRecoil>0 and vpho_mRecoil <2 and p_mcPDG == 2212 and pi_mcPDG == -211" 

dad_cuts = "p_genMotherPDG == 10022 and pi_genMotherPDG == 10022"
n0_cuts = "nb_gamma_genMotherPDG == 10022"
cuts= sig_cuts + " and " + dad_cuts + " and " + n0_cuts
#print(" *** ", cuts, " *** ")

ma.applyCuts("vpho:gen", cuts, path=main)


ma.variablesToNtuple("vpho:gen",variables=b_vars,filename=f"../../root_file/isr/vpho_isr_nbg_{title}_{lista}.root",treename="tree",path=main,)
ma.variablesToNtuple("vpho:gen",variables=mc_gen_topo(200),filename=f"../../root_file/isr/test_TOPO/vpho_isr_nbg_{title}_{lista}_TOPO.root",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)
