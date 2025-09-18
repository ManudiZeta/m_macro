#!/usr/bin/env python3

import sys
import basf2 as b2
import generators as ge
import simulation as si
import reconstruction as re
import mdst


N_ev = int(sys.argv[1])
decfile = sys.argv[2]

# Create the steering path
main = b2.Path()

# Define number of events and experiment number
main.add_module('EventInfoSetter', evtNumList=[N_ev], expList=[0])

# Generate U(4S) events
ge.add_evtgen_generator(path=main,finalstate='signal',signaldecfile=b2.find_file(decfile))

# Simulate the detector response 
si.add_simulation(path=main)

# Reconstruct the objects
re.add_reconstruction(path=main)
 
# Create the mDST output file
mdst.add_mdst_output(path=main, filename='../../root_file/my_mdst_output_Jpsi.root')

# Process the steering path
b2.process(path=main)

# Finally, print out some statistics about the modules execution
print(b2.statistics)
