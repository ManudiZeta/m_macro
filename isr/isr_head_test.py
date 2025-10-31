#!/usr/bin/env python3

import basf2 as b2
import modularAnalysis as ma
import variables.collections as vc
import variables.utils as vu
import sys
from variables import variables as vm
from variables.MCGenTopo import mc_gen_topo

choice = int(sys.argv[1]) # 0 = original channel, 1 = J/psi channel

main = b2.Path()
if choice == 0: 
    ma.inputMdstList(filelist=["../../root_file/isr/isr_output.root"],path=main)
if choice == 1:  
    ma.inputMdstList(filelist=["../../root_file/isr/isrVEC_output_Jpsi.root"],path=main) # -i input da keyboard

lista = "REC"

# Ricostruzione delle particelle visibili
ma.fillParticleList(f"p+:{lista}", "", path=main) 
ma.fillParticleList(f"pi-:{lista}", "", path=main)
ma.fillParticleList(f"gamma:{lista}", "", path=main) 
ma.fillParticleList(f"anti-n0:{lista}", "", path=main)

if choice == 0:
    ma.reconstructDecay(f"vpho:gen -> p+:{lista} pi-:{lista} gamma:{lista} anti-n0:{lista} ",cut="",path=main)

if choice == 1:
    ma.reconstructDecay(f"J/psi:{lista} -> p+:{lista} pi-:{lista} anti-n0:{lista}",cut="",path=main)
    ma.reconstructDecay(f"vpho:gen -> J/psi:{lista} gamma:{lista}",cut="",path=main)

ma.matchMCTruth("vpho:gen", path=main)

#Variables
#g_vars = vc.kinematics + vc.mc_kinematics + ['mcISR', 'mcPDG', 'genMotherPDG','phi','theta','mcPhi','mcTheta' , 'mcPrimary']

b_vars = vc.kinematics + vc.mc_kinematics + ['isSignal'] + vc.recoil_kinematics

daug_vars = ['isSignal','PDG','mcErrors', 'mcPDG', 'mcISR','mcFSR', 'genMotherPDG','genMotherID','isFromECL','isFromTrack',
            'clusterNHits','clusterLAT','clusterE1E9','clusterAbsZernikeMoment40','clusterAbsZernikeMoment51','clusterE9E21',
            'M','p','E','phi','theta','mcPhi','mcTheta','mcP','mcE', 'clusterE','clusterUncorrE']

b_vars = vu.create_aliases_for_selected(daug_vars, "^vpho:gen ->  ^p+ ^pi- ^gamma ^anti-n0", prefix = ["vpho_g","p", "pi", "gamma", "nbar"])

if choice == 1:
    b_vars = b_vars + vu.create_aliases_for_selected(daug_vars, "^J/psi -> p+ pi- anti-n0", prefix = ["JPsi"])


#Recoil variable
vm.addAlias("mRecoil_three","daughterCombination(mRecoil, 0, 1)")
vm.addAlias("pRecoil_three","daughterCombination(pRecoil, 0, 1)")
vm.addAlias("pRecoilPhi_three","daughterCombination(pRecoilPhi, 0, 1)")
vm.addAlias("pRecoilTheta_three","daughterCombination(pRecoilTheta, 0, 1)")
b_vars = b_vars +['mRecoil_three','pRecoil_three','pRecoilTheta_three','pRecoilPhi_three']

#Personal variable alpha
vm.addAlias("fir_arg","formula(sin(pRecoil_three)*sin(nbar_theta)*cos(pRecoilPhi_three-nbar_phi))")
vm.addAlias("sec_arg","formula(cos(pRecoilTheta_three)*cos(nbar_theta))")
vm.addAlias("alpha","formula(acos(fir_arg + sec_arg))")
ma.rankByLowest("vpho:gen", "alpha", numBest=1, path=main)
b_vars = b_vars + ['alpha']

#Personal variable nbarE_buona
vm.addAlias("numE","formula(nbar_clusterE*nbar_clusterE - 2*nbar_M*nbar_M)")
vm.addAlias("denE","formula(2*nbar_M)")
vm.addAlias("nbarE_buona","formula(numE/denE)")
b_vars = b_vars +['nbarE_buona']


#cmskinematics = vu.create_aliases(vc.kinematics + ['InvM','mRecoil','eRecoil'], "useCMSFrame({variable})", "CMS")
#b_vars = b_vars + cmskinematics

print(b_vars)

sig_cuts = "mRecoil_three>0 and p_mcPDG == 2212 and pi_mcPDG == -211 and gamma_mcPDG == 22 and alpha < 0.35" 

if choice == 0:
    dad_cuts = "p_genMotherPDG == 10022 and pi_genMotherPDG == 10022"
    #n0_cuts = "nbar_genMotherPDG == 300553"

else:
    dad_cuts = "p_genMotherPDG == 443 and pi_genMotherPDG == 443 and JPsi_genMotherPDG == 10022" #è giusto o provengono da vpho (10022) a livello di generatore? giusto 443, infatti non vi sono entries per 10022 quando non applico i tagli
    #n0_cuts = "nbar_genMotherPDG == 443" #stesso discorso qui

cuts= sig_cuts + " and " + dad_cuts 
print(" *** ", cuts, " *** ")
ma.applyCuts("vpho:gen", cuts, path=main)

if choice == 0:
    ma.variablesToNtuple("vpho:gen",
        variables=b_vars,
        filename=f"../../root_file/isr/vpho_isr_{lista}.root",
        treename="tree",
        path=main,)
        #ma.variablesToNtuple("vpho:gen",variables=mc_gen_topo(200),filename=f"../../root_file/isr/isr_TOPO/vpho_isr_{lista}.root",treename="tree",path=main,)

else:
    ma.variablesToNtuple("vpho:gen",
        variables=b_vars,
        filename=f"../../root_file/isr/vpho_Jpsi_isrVEC_{lista}.root",
        treename="tree",
        path=main,)
    #ma.variablesToNtuple("vpho:gen",variables=mc_gen_topo(200),filename=f"../../root_file/isr/isrVEC_TOPO/vpho_Jpsi_isr_{lista}.root",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)
