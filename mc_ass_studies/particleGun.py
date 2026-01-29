import basf2 as b2
import simulation as si
import reconstruction as re
from simulation import add_simulation
from reconstruction import add_reconstruction
import mdst
import sys
import os
import argparse
import numpy as np

main = b2.Path()

# specify number of events to be generated
main.add_module("EventInfoSetter", evtNumList=[10000], skipNEvents=0)
main.add_module("EventInfoPrinter")

# Determine if variations are to be done, for Particle Gun
thetaGeneration = "uniform"
thetaParams = [0, 360]
momentumGeneration = "normal"
momentumParams = [3.44,1.285]

# Particle gun
main.add_module(
                "ParticleGun",
                pdgCodes=[-2112],  #anti-n0
                nTracks=0,
                momentumGeneration=momentumGeneration,
                momentumParams=momentumParams,
                thetaGeneration=thetaGeneration,
                thetaParams=thetaParams,
                phiGeneration="uniform",
                phiParams=[0, 360],
                vertexGeneration="fixed",
                xVertexParams=[0],
                yVertexParams=[0],
                zVertexParams=[0],
                independentVertices=False,
                ).set_name("AntiNeutronGun")
                
# detector and L1 trigger simulation and reco
si.add_simulation(path=main)
#re.add_reconstruction(path=main, reconstruct_cdst="rawFormat")
re.add_reconstruction(path=main)

# will be overwritten by basf2 -o if used directly
# rather than calling create_path(outname='outname')

mdst.add_mdst_output(path=main, mc=True, filename='')
b2.process(main)
print(b2.statistics)




