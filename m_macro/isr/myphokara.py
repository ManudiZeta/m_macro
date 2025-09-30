import basf2 as b2
import generators as ge
import pdg

def add_phokhara_evtgen_combination(
        path, final_state_particles, user_decay_file,
        beam_energy_spread=True, isr_events=False, min_inv_mass_vpho=0.0,
        max_inv_mass_vpho=0.0, eventType=''):
    """
    Add combination of PHOKHARA and EvtGen to the path. Phokhara is
    acting as ISR generator by generating e+ e- -> mu+ mu-, the muon pair is
    then replaced by a virtual photon. Finally, the virtual photon is
    decayed by EvtGen.

    Parameters:
        path (basf2.Path): Path where the generator should be added.
        final_state_particles (list): List of final-state particles of
            the virtual-photon decay. It is necessary to define the correct
            mass threshold in PHOKHARA. For example, for the process
            e+ e- -> J/psi eta_c, the list should be ['J/psi', 'eta_c'];
            it does not depend on subsequent J/psi or eta_c decays.
        user_decay_file (str): Name of EvtGen user decay file. The initial
            particle must be the virtual photon (vpho).
        beam_energy_spread (bool): Whether beam-energy spread should be
            simulated
        isr_events (bool): If true, then PHOKHARA is used with ph0 (LO in
            basf2) = 0, i.e. generation of processes with one photon.
        min_inv_mass_hadrons(float): Minimum invariant mass of the virtual
            photon. This parameter is used only if isr_events is true,
            otherwise the minimum mass is computed from the masses of
            the final-state particles.
        max_inv_mass_hadrons(float): Maximum invariant mass of the virtual
            photon. This parameter is used only if isr_events is true,
            otherwise the maximum mass is not restricted.
        eventType (str) : event type information
    """

    phokhara = path.add_module('PhokharaInput')
    phokhara.param('eventType', eventType)

    # Generate muons and replace them by a virtual photon.
    phokhara.param('FinalState', 0) # lo 0 genera muoni in phokara, che vengono subito rimpiazzati da vpho
    phokhara.param('ReplaceMuonsByVirtualPhoton', True) #<-- attiva la sostituzione dei mu con vpho

    # Simulate beam-energy spread. This performs initialization for every
    # event, and, thus, very slow, but usually necessary except for testing.
    phokhara.param('BeamEnergySpread', beam_energy_spread)

    # Soft photon cutoff.
    phokhara.param('Epsilon', 0.0001)

    # Maximum search.
    phokhara.param('SearchMax', 5000)

    # Number of generation attempts for event.
    phokhara.param('nMaxTrials', 25000)

    # Use NNLO.
    if isr_events:
        phokhara.param('LO', 0)
    else:
        phokhara.param('LO', 1)
    phokhara.param('NLO', 1)

    # Use ISR only.
    phokhara.param('QED', 0) #correzione in QED con solo ISR (ISR only(0), ISR+FSR(1), ISR+INT+FSR(2)) 

    # No interference.
    phokhara.param('IFSNLO', 0)

    # Vacuum polarization by Fred Jegerlehner.
    phokhara.param('Alpha', 1) #accesa

    # Do not include narrow resonances.
    phokhara.param('NarrowRes', 0) # no narrow resonances (0), j/psi (1) OR psi2s (2)

    # Angular ragnes.
    phokhara.param('ScatteringAngleRangePhoton', [0., 180.]) # angolo del gamma di isr
    phokhara.param('ScatteringAngleRangeFinalStates', [0., 180.]) # angolo delle particelle finali

    # Minimal invariant mass of the muons and tagged photon combination.
    phokhara.param('MinInvMassHadronsGamma', 0.)

    #Ho eliminato tutto l'if, se l'argomento isr_events=True

    mass = 0
    for particle in final_state_particles:
        p = pdg.get(particle)
        mass = mass + p.Mass()
    phokhara.param('MinInvMassHadrons', mass * mass)
    phokhara.param('ForceMinInvMassHadronsCut', True)
    # Maximum squared invariant mass of muons (final state).
    # It is set to a large value, resulting in unrestricted mass.
    phokhara.param('MaxInvMassHadrons', 200.0)

    # Minimal photon energy/missing energy, must be larger than 0.01*(CMS energy) [GeV]
    # Minimal photon energy.
    phokhara.param('MinEnergyGamma', 0.12)

    # EvtGen.
    evtgen_decay = path.add_module('EvtGenDecay')
    evtgen_decay.param('UserDecFile', user_decay_file)
