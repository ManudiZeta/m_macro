#!/usr/bin/env python3

import basf2 as b2
import modularAnalysis as ma
import variables.collections as vc
import variables.utils as vu
import sys
import kinfit
from variables import variables as vm
from variables.MCGenTopo import mc_gen_topo

choice = int(sys.argv[1]) # 0 = original channel, 1 = J/psi channel

main = b2.Path()
if choice == 0: 
    ma.inputMdstList(filelist=["../../root_file/isr/channel_std/isrPhok_output_merge100k.root"],path=main)
if choice == 1:  
    ma.inputMdstList(filelist=["../../root_file/isr/channel_JPsi/isrVEC_output_4S.root"],path=main)

lista = "REC"
cand_hp = "gamma"
lista_n = "nbar"

if cand_hp == "anti-n0":
    part = "n"
else: 
    part = "g"
    
# Ricostruzione delle particelle visibili
ma.fillParticleList(f"p+:{lista}", "protonID > 0.9 and dr < 1 and abs(dz) < 3", path=main) 
ma.fillParticleList(f"pi-:{lista}", "pionID > 0.1", path=main)
ma.fillParticleList(f"gamma:{lista}", "", path=main) 
ma.fillParticleList(f"{cand_hp}:{lista_n}", "", path=main)

ma.reconstructDecay(f"vpho:list_rec -> p+:{lista} pi-:{lista} gamma:{lista}",cut="thetaInECLAcceptance",path=main)
ma.reconstructDecay(f"vpho:gen -> vpho:list_rec {cand_hp}:{lista_n}",cut="",path=main)

ma.matchMCTruth("vpho:gen", path=main)
#kinfit.MassfitKinematic1CRecoil(list_name = "vpho:list_rec", recoilMass = 0.939565, path=main)
ma.getNeutralHadronGeomMatches(f"{cand_hp}:{lista_n}", addKL=False, addNeutrons=True, efficiencyCorrectionKl=0.83, efficiencyCorrectionNeutrons=1.0, path=main)

#Variables
#g_vars = vc.kinematics + vc.mc_kinematics + ['mcISR', 'mcPDG', 'genMotherPDG','phi','theta','mcPhi','mcTheta' , 'mcPrimary']

b_vars = vc.kinematics + vc.mc_kinematics + ['isSignal'] + vc.recoil_kinematics

daug_vars = ['isSignal','PDG','mcErrors', 'mcPDG', 'mcISR','mcFSR', 'genMotherPDG','genMotherID','isFromECL','isFromTrack','M','p','E','phi','theta','mcPhi','mcTheta','mcP','mcE', 'clusterE','clusterUncorrE']

cluster_vars = ['clusterNHits','clusterLAT','clusterE1E9','clusterAbsZernikeMoment40','clusterAbsZernikeMoment51','clusterE9E21','clusterDeltaLTemp','clusterHighestE','clusterNumberOfHadronDigits','clusterPulseShapeDiscriminationMVA','clusterSecondMoment','distanceToMcNeutron','fakePhotonSuppression']

b_vars = vu.create_aliases_for_selected(daug_vars, f"^vpho:gen -> [^vpho:list_rec -> ^p+ ^pi- ^gamma] ^{cand_hp}", prefix = ["mum","vpho_r","p", "pi", "gamma", "nbar"])
b_vars = b_vars + vu.create_aliases_for_selected(vc.recoil_kinematics, f"vpho:gen -> [^vpho:list_rec -> p+ pi- ^gamma] {cand_hp}", prefix = ["vpho_r","gamma"])
b_vars = b_vars + vu.create_aliases_for_selected(cluster_vars, f"vpho:gen -> [vpho:list_rec -> p+ pi- gamma] ^{cand_hp}", prefix = ["nbar"])
    
#Personal variable alpha
vm.addAlias("fir_arg","formula(sin(vpho_r_pRecoilTheta)*sin(nbar_theta)*cos(vpho_r_pRecoilPhi-nbar_phi))")
vm.addAlias("sec_arg","formula(cos(vpho_r_pRecoilTheta)*cos(nbar_theta))")
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

sig_cuts = "vpho_r_mRecoil > 0 and alpha < 0.35 and nbar_isFromECL == 1" 
#sig_select = "p_mcPDG == 2212 and pi_mcPDG == -211 and gamma_mcPDG == 22"
sig_select = "p_PDG == 2212 and pi_PDG == -211 and gamma_PDG == 22"

if choice == 0:
    dad_cuts = "p_genMotherPDG == 10022 and pi_genMotherPDG == 10022"
    #n0_cuts = "nbar_genMotherPDG == 300553"

else:
    dad_cuts = "p_genMotherPDG == 443 and pi_genMotherPDG == 443" #and JPsi_genMotherPDG == 10022"
    #n0_cuts = "nbar_genMotherPDG == 443" 

cuts= sig_cuts + " and "  + sig_select + " and " + dad_cuts 
print(" *** ", cuts, " *** ")
ma.applyCuts("vpho:gen", cuts, path=main)

if choice == 0:
    ma.variablesToNtuple("vpho:gen",variables=b_vars,filename=f"../../root_file/isr/channel_std/vpho_std_isr_{part}_{lista}_merge100k.root",treename="tree",path=main,)
    ma.variablesToNtuple("vpho:gen",variables=mc_gen_topo(200),filename=f"../../root_file/isr/isr_TOPO/vpho_std_isr_{part}_{lista}_merge100k.root",treename="tree",path=main,)

else:
    ma.variablesToNtuple("vpho:gen",variables=b_vars,filename=f"../../root_file/isr/channel_JPsi/vpho_Jpsi_isr_{part}_{lista}_kin_50k.root",treename="tree",path=main,)
    #ma.variablesToNtuple("vpho:gen",variables=mc_gen_topo(200),filename=f"../../root_file/isr/isrVEC_TOPO/vpho_Jpsi_isr_{lista}.root",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)
