#!/usr/bin/env python3

import basf2 as b2
import modularAnalysis as ma
import variables.collections as vc
import variables.utils as vu
import kinfit
from variables import variables as vm
from variables.MCGenTopo import mc_gen_topo

main = b2.Path()
ma.inputMdstList(filelist="",path=main)
lista = "REC"

# Ricostruzione delle particelle visibili
ma.fillParticleList(f"p+:{lista}", "", path=main) 
ma.fillParticleList(f"pi-:{lista}", "", path=main) 
ma.fillParticleList(f"anti-n0:{lista}", "", path=main)

ma.reconstructDecay(f"vpho:list_rec -> p+:{lista} pi-:{lista}",cut="",path=main)
ma.reconstructDecay(f"vpho:gen -> vpho:list_rec anti-n0:{lista}",cut="",path=main)

ma.matchMCTruth("vpho:gen", path=main)
#kinfit.MassfitKinematic1CRecoil(list_name = "vpho:list_rec", recoilMass = 0.939565, path=main)
ma.getNeutralHadronGeomMatches(f"anti-n0:{lista}", addKL=False, addNeutrons=True, efficiencyCorrectionKl=0.83, efficiencyCorrectionNeutrons=1.0, path=main)
ma.buildRestOfEvent("vpho:gen", fillWithMostLikely=True, path=main)

#Variables
b_vars = vc.kinematics + vc.mc_kinematics + vc.recoil_kinematics

daug_vars = ['isSignal','isPrimarySignal','mcPrimary','isSignal','PDG','mcErrors', 'mcPDG', 'mcISR','mcFSR', 'genMotherPDG','isFromECL','isFromTrack','M','p','E','phi','theta','mcPhi','mcTheta','mcP','mcE']

cluster_vars = ['clusterE','clusterUncorrE','clusterNHits','clusterLAT','clusterE1E9','clusterAbsZernikeMoment40','clusterAbsZernikeMoment51','clusterE9E21','clusterDeltaLTemp','clusterHighestE','clusterNumberOfHadronDigits','clusterPulseShapeDiscriminationMVA','clusterSecondMoment','distanceToMcNeutron']

b_vars = vu.create_aliases_for_selected(daug_vars, f"^vpho:gen -> [^vpho:list_rec -> ^p+ ^pi-] ^anti-n0", prefix = ["mum","vpho_r","p", "pi", "nbar"])
b_vars = b_vars + vu.create_aliases_for_selected(vc.recoil_kinematics, f"vpho:gen -> [^vpho:list_rec -> p+ pi-] anti-n0", prefix = ["vpho_r"])
b_vars = b_vars + vu.create_aliases_for_selected(cluster_vars, f"vpho:gen -> [vpho:list_rec -> p+ pi- ] ^anti-n0", prefix = ["nbar"])
    
#ROE vars
roe_kinematics = ["roeE()", "roeM()", "roeP()", "roeMbc()", "roeDeltae()"]
roe_multiplicities = [
    "nROE_Charged()",
    "nROE_Photons()",
    "nROE_NeutralHadrons()",
]
b_vars = b_vars + roe_kinematics + roe_multiplicities 

#alpha variable
vm.addAlias("fir_arg","formula(sin(vpho_r_pRecoilTheta)*sin(nbar_theta)*cos(vpho_r_pRecoilPhi-nbar_phi))")
vm.addAlias("sec_arg","formula(cos(vpho_r_pRecoilTheta)*cos(nbar_theta))")
vm.addAlias("alpha","formula(acos(fir_arg + sec_arg))")
ma.rankByLowest("vpho:gen", "alpha", numBest=1, path=main)
b_vars = b_vars + ['alpha']

sig_cuts = "vpho_r_mRecoil > 0 and vpho_r_mRecoil <2 and alpha < 0.35 and nbar_isFromECL == 1" 
sig_select = "p_mcPDG == 2212 and pi_mcPDG == -211"
dad_cuts = "p_genMotherPDG == 10022 and pi_genMotherPDG == 10022"

cuts= sig_cuts + " and "  + sig_select + " and "  + dad_cuts

ma.applyCuts("vpho:gen", sig_select, path=main)

ma.variablesToNtuple("vpho:gen",variables=b_vars,filename= "grid_out_nog_19122025.root",treename="tree",path=main,)
#ma.variablesToNtuple("vpho:gen",variables=mc_gen_topo(200),filename=f"grid_topo_12122025.root",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)
