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
    ma.inputMdstList(filelist=["../../root_file/nbar_recoil/my_mdst_output.root"],path=main)
else: 
    ma.inputMdstList(filelist=["../../root_file/nbar_recoil/my_mdst_output_Jpsi.root"],path=main)

lista = "REC"

ma.fillParticleList("p+:all", "", path=main) 
ma.fillParticleList("pi-:all", "", path=main)
ma.fillParticleList("gamma:all", "", path=main)
ma.fillParticleList("anti-n0:all", "", path=main)


ma.reconstructDecay("vpho:list_rec -> p+:all pi-:all gamma:all",cut="",path=main)
ma.reconstructDecay("Upsilon(4S):list_rec -> vpho:list_rec anti-n0:all ",cut="",path=main)

ma.matchMCTruth("Upsilon(4S):list_rec", path=main)

daug_vars = ['isSignal','PDG','mcErrors', 'mcPDG', 'genMotherPDG','genMotherID','M','p','E','phi','theta','mcPhi','mcTheta','mcP','mcE', 'clusterE','clusterUncorrE']

b_vars = vu.create_aliases_for_selected(daug_vars, "Upsilon(4S) -> [vpho -> ^p+ ^pi- ^gamma] ^anti-n0", prefix = ["p", "pi", "gamma", "nbar"])

b_vars = b_vars + vu.create_aliases_for_selected(vc.recoil_kinematics, "Upsilon(4S) -> [^vpho -> p+ pi- gamma] anti-n0", prefix = ["vpho"])

vm.addAlias("fir_arg","formula(sin(vpho_pRecoilTheta)*sin(nbar_theta)*cos(vpho_pRecoilPhi-nbar_phi))")
vm.addAlias("sec_arg","formula(cos(vpho_pRecoilTheta)*cos(nbar_theta))")
vm.addAlias("alpha","formula(acos(fir_arg + sec_arg))")

ma.rankByLowest("Upsilon(4S):list_rec", "alpha", numBest=1, path=main)

#vm.addAlias("rank", "extraInfo(alpha_rank)") #what is this??

b_vars = b_vars + ['alpha']


#cmskinematics = vu.create_aliases(vc.kinematics + ['InvM','mRecoil','eRecoil'], "useCMSFrame({variable})", "CMS")
#b_vars = b_vars + cmskinematics

print(b_vars)

sig_cuts = "vpho_mRecoil>0 and vpho_mRecoil <2 and p_mcPDG == 2212 and pi_mcPDG == -211 and gamma_mcPDG == 22" 

if choice == 0:
    dad_cuts = "p_genMotherPDG == 300553 and pi_genMotherPDG == 300553 and gamma_genMotherPDG== 300553"
    n0_cuts = "nbar_genMotherPDG == 300553"

else:
    dad_cuts = "p_genMotherPDG == 443 and pi_genMotherPDG == 443 and gamma_genMotherPDG== 300553 " #è giusto o provengono da vpho (10022) a livello di generatore? giusto 443, infatti non vi sono entries per 10022 quando non applico i tagli
    n0_cuts = "nbar_genMotherPDG == 443" #stesso discorso qui

cuts= sig_cuts + " and " + dad_cuts + " and " + n0_cuts
print(" *** ", cuts, " *** ")
ma.applyCuts("Upsilon(4S):list_rec", cuts, path=main)

if choice == 0:
    ma.variablesToNtuple("Upsilon(4S):list_rec",variables=b_vars ,filename=f"../../root_file/nbar_recoil/vpho_p_pi_n_{lista}.root",treename="tree",path=main,)
    ma.variablesToNtuple("Upsilon(4S):list_rec",variables=mc_gen_topo(200),filename=f"../../root_file/nbar_recoil/phsp_TOPO/vpho_p_pi_n_{lista}TOPO.root",treename="tree",path=main,)

else:
    ma.variablesToNtuple("Upsilon(4S):list_rec",variables=b_vars,filename=f"../../root_file/nbar_recoil/vpho_Jpsi_{lista}.root",treename="tree",path=main,)
    ma.variablesToNtuple("Upsilon(4S):list_rec",variables=mc_gen_topo(200),filename=f"../../root_file/nbar_recoil/phsp_TOPO/vpho_Jpsi_phsp_{lista}_TOPO.root",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)
