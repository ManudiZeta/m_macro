#!/usr/bin/env python3

import basf2 as b2
import modularAnalysis as ma
import variables.collections as vc
import variables.utils as vu
from variables import variables as vm
import sys
from variables.MCGenTopo import mc_gen_topo

main = b2.Path()

ma.inputMdstList(filelist = '' ,path=main)

ma.fillParticleList("anti-n0:mylist", "", path=main)

ma.matchMCTruth("anti-n0:mylist", path=main)

#Def some variables
base_vars = ["PDG","mcPDG","genMotherPDG"]

cluster_vars = ["clusterE","clusterE1E9","clusterE9E21", "clusterLAT",
                "clusterAbsZernikeMoment40","clusterAbsZernikeMoment51","clusterE9E21","clusterSecondMoment",
                "clusterNHits"]

other_vars = ["p","theta","phi","mcP","mcTheta","mcPhi","isFromECL","hasAncestor(-2112, 1)","hasAncestor(22, 1)","hasAncestor(211, 0)",
              "varForFirstMCAncestorOfType(anti-n0, p)","varForFirstMCAncestorOfType(anti-n0, mcP)",
              "varForFirstMCAncestorOfType(anti-n0, theta)","varForFirstMCAncestorOfType(anti-n0, mcTheta)"]

vertex_vars = [ "distance", "mcDecayVertexFromIPDistance", "mcDecayVertexFromIPRho",
                "mcDecayVertexX", "mcDecayVertexY", "mcDecayVertexZ",
                "mcProductionVertexX","mcProductionVertexY","mcProductionVertexZ",
                "prodVertexX","prodVertexY","prodVertexZ"]

n_vars = base_vars + cluster_vars + other_vars + vertex_vars

ma.variablesToNtuple("anti-n0:mylist",variables=n_vars,filename=f"",treename="tree",path=main,)

b2.process(main)

print(b2.statistics)
