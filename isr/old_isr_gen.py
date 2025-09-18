#!/usr/bin/env python3
import sys
import basf2 as b2
import generators as ge
import simulation as si
import reconstruction as re
import mdst


N_ev = int(sys.argv[1])
#decfile = sys.argv[2]

# Create the steering path
main = b2.Path()

# Define number of events and experiment number
main.add_module('EventInfoSetter', evtNumList=[N_ev], expList=[0])

ge.add_phokhara_evtgen_combination(path=main,
final_state_particles = ['p+', 'pi-', 'anti-n0'], 
user_decay_file = "../dec_file/dec_isr.dec")

#beam_energy_spread=True, isr_events=True,min_inv_mass_vpho=2.1)

# Simulate the detector response 
si.add_simulation(path=main)

# Reconstruct the objects
re.add_reconstruction(path=main)
 
# Create the mDST output file
mdst.add_mdst_output(path=main, filename='../../root_file/isr_output.root')

# Process the steering path
b2.process(path=main)

# Finally, print out some statistics about the modules execution
print(b2.statistics)
