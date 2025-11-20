#!/usr/bin/env python3
import ROOT
import basf2 as b2
import generators as ge
import simulation as si
import reconstruction as re
import mdst

main = b2.Path()

# Define number of events (-n number -o output in terminal)and experiment number
main.add_module('EventInfoSetter', expList=[0])


print("****** CHANNEL e+ e- (isr) --> vpho --> p+ pi- nbar ****** ")
final_state = ['p+', 'pi-', 'anti-n0']
decfile = "../dec_file/dec_isr.dec"
#Generate isr events with phokhara_evt_gen
ge.add_phokhara_evtgen_combination(path=main,
                                   final_state_particles = final_state, 
                                   user_decay_file = decfile,)

    
main.add_module('PrintMCParticles', onlyPrimaries = False)

# Simulate the detector response 
si.add_simulation(path=main)

# Reconstruct the objects
re.add_reconstruction(path=main)

mdst.add_mdst_output(path=main)
# Process the steering path
b2.process(path=main)

# Finally, print out some statistics about the modules execution
print(b2.statistics)


