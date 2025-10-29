#!/usr/bin/env python3
import sys
import ROOT
import basf2 as b2
import generators as ge
#from myphokara import add_phokhara_evtgen_combination
import simulation as si
import reconstruction as re
import mdst

SM = ROOT.TStopwatch() 
SM.Start()

N_ev = int(sys.argv[1]) #number of events
choice = int(sys.argv[2]) # 0 = classic channel (phokhara evt_gen), 1 = J/psi channel (vector_ISR)

# Create the steering path
main = b2.Path()

# Define number of events and experiment number
main.add_module('EventInfoSetter', evtNumList=[N_ev], expList=[0])

if choice == 0: 
    print("****** CHANNEL e+ e- (isr) --> vpho --> p+ pi- nbar ****** ")
    final_state = ['p+', 'pi-', 'anti-n0']
    decfile = "../dec_file/dec_isr.dec"
    #Generate isr events with phokhara_evt_gen
    ge.add_phokhara_evtgen_combination(path=main,
    final_state_particles = final_state, 
    user_decay_file = decfile,)
    #beam_energy_spread=True,  
    #isr_events=True)

    #min_inv_mass_vpho=2.1, max_inv_mass_vpho=10.6)
    

if choice == 1:  
    print("****** CHANNEL e+ e- (isr) --> vpho --> J/psi --> p+ pi- nbar ****** ")
    final_state = ['J/psi']
    decfile = "../dec_file/dec_isrVEC_jpsi.dec"
    #Generate isr events with evt_gen_VECTORISR
    ge.add_evtgen_generator(path=main,finalstate='signal',signaldecfile=b2.find_file(decfile))
    

# Simulate the detector response 
si.add_simulation(path=main)

# Reconstruct the objects
re.add_reconstruction(path=main)
 
# Create the mDST output file
if choice == 0:
    mdst.add_mdst_output(path=main, filename='../../root_file/isr/isr_output_test_False.root')
if choice == 1:
    mdst.add_mdst_output(path=main, filename='../../root_file/isr/isrVEC_output_Jpsi.root')

# Process the steering path
b2.process(path=main)

# Finally, print out some statistics about the modules execution
print(b2.statistics)

print("\n Total time:")
SM.Stop()
SM.Print()