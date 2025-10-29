#!/usr/bin/env python3
import ROOT
import basf2 as b2
import generators as ge
#from myphokara import add_phokhara_evtgen_combination
import simulation as si
import reconstruction as re
import mdst
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-channel", "--channel",
    required=True,
    choices=["std", "J/psi"],
    help="Select the desired channel"
)

parser.add_argument(
    "-output", "--output",
    required=True,
    help="Output name"
)
args = parser.parse_args()

output_path = f"../../root_file/isr/{args.output}"
if not output_path.endswith(".root"):
    output_path += ".root

# ****** START ******
SM = ROOT.TStopwatch() 
SM.Start()

main = b2.Path()

# Define number of events (-n number in terminal )and experiment number
main.add_module('EventInfoSetter', expList=[0])

if args.channel == 'std': 
    print("****** CHANNEL e+ e- (isr) --> vpho --> p+ pi- nbar ****** ")
    final_state = ['p+', 'pi-', 'anti-n0']
    decfile = "../dec_file/dec_isr.dec"
    #Generate isr events with phokhara_evt_gen
    ge.add_phokhara_evtgen_combination(path=main,
    final_state_particles = final_state, 
    user_decay_file = decfile,)
    #beam_energy_spread=True,  
    #isr_events=True)
    

if args.channel == 'J/psi':   
    print("****** CHANNEL e+ e- (isr) --> vpho --> J/psi --> p+ pi- nbar ****** ")
    final_state = ['J/psi']
    decfile = "../dec_file/dec_isrVEC_jpsi.dec"
    #Generate isr events with evt_gen_VECTORISR
    #ge.add_evtgen_generator(path=main,finalstate='signal',signaldecfile=b2.find_file(decfile))
    main.add_module(
        'EvtGenInput',
        userDECFile=decfile,
        ParentParticle='vpho'
    )

main.add_module('PrintMCParticles', onlyPrimaries = False)

# Simulate the detector response 
si.add_simulation(path=main)

# Reconstruct the objects
re.add_reconstruction(path=main)
 
# Create the mDST output file
if args.channel == 'std':
    mdst.add_mdst_output(path=main, filename=output_path)
if args.channel == 'J/psi':
    mdst.add_mdst_output(path=main, filename=output_path)

# Process the steering path
b2.process(path=main)

# Finally, print out some statistics about the modules execution
print(b2.statistics)

print("\n Total time:")
SM.Stop()
SM.Print()

'''
if __name__ == "__main__":
    
    my_path = create_path()
    my_path_2 = create_path_2()
    b2.process(my_path)
'''
