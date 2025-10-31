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
    ma.inputMdstList(filelist=["../../root_file/isr/isrVEC_output_4S.root"],path=main)

lista = "REC"

# Ricostruzione delle particelle visibili
ma.fillParticleList(f"p+:{lista}", "", path=main) 
ma.fillParticleList(f"pi-:{lista}", "", path=main)
ma.fillParticleList(f"gamma:{lista}", "", path=main) 
ma.fillParticleList(f"anti-n0:{lista}", "", path=main)

ma.reconstructDecay(f"vpho:list_rec -> p+:{lista} pi-:{lista} gamma:{lista}",cut="",path=main)

if choice == 0:
    ma.reconstructDecay(f"Upsilon(4S):gen -> vpho:list_rec anti-n0:{lista} ",cut="",path=main)
if choice == 1:
    ma.reconstructDecay(f"J/psi:list_rec -> vpho:list_rec anti-n0:{lista}",cut="",path=main)
    ma.reconstructDecay(f"Upsilon(4S):gen -> J/psi:list_rec",cut="",path=main)

ma.matchMCTruth("Upsilon(4S):gen", path=main)

#Variables
#g_vars = vc.kinematics + vc.mc_kinematics + ['mcISR', 'mcPDG', 'genMotherPDG','phi','theta','mcPhi','mcTheta' , 'mcPrimary']

b_vars = vc.kinematics + vc.mc_kinematics + ['isSignal'] + vc.recoil_kinematics

daug_vars = ['isSignal','PDG','mcErrors', 'mcPDG', 'mcISR','mcFSR', 'genMotherPDG','genMotherID','clusterNHits','clusterLAT','clusterE1E9','clusterAbsZernikeMoment40','clusterAbsZernikeMoment51','clusterE9E21','isFromECL','isFromTrack','M','p','E','phi','theta','mcPhi','mcTheta','mcP','mcE', 'clusterE','clusterUncorrE']

if choice == 0:
    b_vars = vu.create_aliases_for_selected(daug_vars, "^Upsilon(4S):gen -> [^vpho:list_rec -> ^p+ ^pi- ^gamma] ^anti-n0", prefix = ["vpho_g","vpho_r","p", "pi", "gamma", "nbar"])
    b_vars = b_vars + vu.create_aliases_for_selected(vc.recoil_kinematics, "Upsilon(4S):gen -> [^vpho:list_rec -> p+ pi- gamma] anti-n0", prefix = ["vpho_r"])
if choice == 1:
    b_vars = vu.create_aliases_for_selected(daug_vars, "^Upsilon(4S):gen -> [^J/psi -> [^vpho:list_rec -> ^p+ ^pi- ^gamma] ^anti-n0]", prefix = ["vpho_g","JPsi","vpho_r","p", "pi", "gamma", "nbar"])
    b_vars = b_vars + vu.create_aliases_for_selected(vc.recoil_kinematics, "Upsilon(4S):gen -> [J/psi -> [^vpho:list_rec -> p+ pi- gamma] anti-n0]", prefix = ["vpho_r"])
    
#Personal variable alpha
vm.addAlias("fir_arg","formula(sin(vpho_r_pRecoilTheta)*sin(nbar_theta)*cos(vpho_r_pRecoilPhi-nbar_phi))")
vm.addAlias("sec_arg","formula(cos(vpho_r_pRecoilTheta)*cos(nbar_theta))")
vm.addAlias("alpha","formula(acos(fir_arg + sec_arg))")
ma.rankByLowest("Upsilon(4S):gen", "alpha", numBest=1, path=main)
b_vars = b_vars + ['alpha']

#Personal variable nbarE_buona
vm.addAlias("numE","formula(nbar_clusterE*nbar_clusterE - 2*nbar_M*nbar_M)")
vm.addAlias("denE","formula(2*nbar_M)")
vm.addAlias("nbarE_buona","formula(numE/denE)")
b_vars = b_vars +['nbarE_buona']

#cmskinematics = vu.create_aliases(vc.kinematics + ['InvM','mRecoil','eRecoil'], "useCMSFrame({variable})", "CMS")
#b_vars = b_vars + cmskinematics

print(b_vars)

sig_cuts = "vpho_r_mRecoil>0 and p_mcPDG == 2212 and pi_mcPDG == -211 and gamma_mcPDG == 22" #and alpha < 0.35" 

if choice == 0:
    dad_cuts = "p_genMotherPDG == 10022 and pi_genMotherPDG == 10022"
    #n0_cuts = "nbar_genMotherPDG == 300553"

else:
    dad_cuts = "p_genMotherPDG == 443 and pi_genMotherPDG == 443" #and JPsi_genMotherPDG == 10022"
    #n0_cuts = "nbar_genMotherPDG == 443" 

cuts= sig_cuts + " and " + dad_cuts 
print(" *** ", cuts, " *** ")
ma.applyCuts("Upsilon(4S):gen", cuts, path=main)

if choice == 0:
    ma.variablesToNtuple("Upsilon(4S):gen",variables=b_vars,filename=f"../../root_file/isr/vpho_isr_{lista}.root",treename="tree",path=main,)
    #ma.variablesToNtuple("vpho:gen",variables=mc_gen_topo(200),filename=f"../../root_file/isr/isr_TOPO/vpho_isr_{lista}.root",treename="tree",path=main,)

else:
    ma.variablesToNtuple("Upsilon(4S):gen",variables=b_vars,filename=f"../../root_file/isr/vpho_Jpsi_isrVEC_{lista}_4S.root",treename="tree",path=main,)
    #ma.variablesToNtuple("vpho:gen",variables=mc_gen_topo(200),filename=f"../../root_file/isr/isrVEC_TOPO/vpho_Jpsi_isr_{lista}.root",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)
