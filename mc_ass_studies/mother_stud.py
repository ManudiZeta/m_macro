#!/usr/bin/env python3

import basf2 as b2
import modularAnalysis as ma
import variables.collections as vc
import variables.utils as vu
import kinfit
from variables import variables as vm
from variables.MCGenTopo import mc_gen_topo


main = b2.Path()

ma.inputMdstList(filelist=["../../root_file/isr/channel_std/isrPhok_output_merge100k.root"],path=main)

# Ricostruzione delle particelle visibili
ma.fillParticleList(f"p+:myl", "", path=main) #protonID > 0.9 and dr < 1 and abs(dz) < 3 se serve
ma.fillParticleList(f"pi-:myl", "", path=main) #pionID > 0.9 and dr < 1 and abs(dz) < 3 se serve
ma.fillParticleList(f"gamma:myl", "", path=main) 
ma.fillParticleList(f"anti-n0:myl", "", path=main)

ma.reconstructDecay(f"vpho:list_rec -> p+:myl pi-:myl gamma:myl",cut="thetaInECLAcceptance",path=main)
ma.reconstructDecay(f"vpho:gen -> vpho:list_rec anti-n0:myl",cut="",path=main)

ma.matchMCTruth("vpho:gen", path=main)
ma.buildRestOfEvent("vpho:gen", fillWithMostLikely=True, path=main)

#Variables
base_vars = ["PDG","mcPDG","genMotherPDG"]

cluster_vars = ["clusterE","clusterE1E9","clusterE9E21", "clusterLAT",
                "clusterAbsZernikeMoment40","clusterAbsZernikeMoment51","clusterE9E21","clusterSecondMoment",
                "clusterNHits"]

other_vars = ["p","theta","phi","mcP","mcTheta","mcPhi","isFromECL","hasAncestor(-2112, 1)","hasAncestor(22, 1)","hasAncestor(211, 0)",
              "varForFirstMCAncestorOfType(anti-n0, p)","varForFirstMCAncestorOfType(anti-n0, mcP)"]

n_vars = cluster_vars + other_vars

b_vars = vu.create_aliases_for_selected(base_vars, f"^vpho:gen -> [^vpho:list_rec -> ^p+ ^pi- ^gamma] ^anti-n0", prefix = ["mum","vpho_r","p","pi","gamma","nbar"])
b_vars = b_vars + vu.create_aliases_for_selected(n_vars, f"vpho:gen -> [vpho:list_rec -> p+ pi- gamma] ^anti-n0", prefix = ["nbar"])
b_vars = b_vars + vu.create_aliases_for_selected(vc.recoil_kinematics, f"vpho:gen -> [^vpho:list_rec -> p+ pi- gamma] anti-n0", prefix = ["vpho_r"])
    
#ROE vars
roe_kinematics = ["roeE()", "roeM()", "roeP()", "roeMbc()", "roeDeltae()"]
roe_multiplicities = [
    "nROE_Charged()",
    "nROE_Photons()",
    "nROE_NeutralHadrons()",
]
b_vars = b_vars + roe_kinematics + roe_multiplicities 


#Personal variable alpha
vm.addAlias("fir_arg","formula(sin(vpho_r_pRecoilTheta)*sin(nbar_theta)*cos(vpho_r_pRecoilPhi-nbar_phi))")
vm.addAlias("sec_arg","formula(cos(vpho_r_pRecoilTheta)*cos(nbar_theta))")
vm.addAlias("alpha","formula(acos(fir_arg + sec_arg))")
ma.rankByLowest("vpho:gen", "alpha", numBest=1, path=main)
b_vars = b_vars + ["alpha"]

sig_cuts = "vpho_r_mRecoil > 0 and vpho_r_mRecoil < 2 and alpha < 0.35 and nbar_isFromECL == 1" 
sig_select = "p_mcPDG == 2212 and pi_mcPDG == -211"

dad_cuts = "p_genMotherPDG == 10022 and pi_genMotherPDG == 10022"

cuts= sig_cuts + " and " + sig_select + " and " + dad_cuts 
print(" *** ", cuts, " *** ")
ma.applyCuts("vpho:gen", cuts, path=main)

#kinfit.MassfitKinematic1CRecoil(list_name = "vpho:list_rec", recoilMass = 0.939565, path=main)

ma.variablesToNtuple("vpho:gen",variables=b_vars,filename=f"../../root_file/mc_ass_stud/mother_stud.root",treename="tree",path=main,)
ma.variablesToNtuple("vpho:gen",variables=mc_gen_topo(200),filename=f"../../root_file/mc_ass_stud/topoana/mother_stud.root",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)




'''
b_vars = vc.kinematics + vc.mc_kinematics + ["isSignal"] + vc.recoil_kinematics
daug_vars = ["isSignal","PDG","mcErrors", "mcPDG", "mcISR","mcFSR", "genMotherPDG","genMotherID","isFromECL","isFromTrack","M","p","E","phi","theta","mcPhi","mcTheta","mcP","mcE", "clusterE","clusterUncorrE"]
cluster_vars = ["clusterNHits","clusterLAT","clusterE1E9","clusterAbsZernikeMoment40","clusterAbsZernikeMoment51","clusterE9E21","clusterDeltaLTemp","clusterHighestE","clusterNumberOfHadronDigits","clusterPulseShapeDiscriminationMVA","clusterSecondMoment","distanceToMcNeutron"]
'''