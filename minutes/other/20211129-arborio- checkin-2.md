# Arborio Check-in (26.11.21)

Presence: Alice G., Christos S., Egidio D'A., Mario N., Max E., Michele G., Robin G., Lennart L., Claudia C., Nora A.A., Anne K., Amo(Ali Hosseini),

## Arborio HBP Milestones

- **M18 (10/2021)** SC3 T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) Arbor IO v.3 with glomeruli Arbor IO v.3 running on EBRAINS.
- **M18	(10/2021)** SC3	T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) MultiGPU feasibility study Implementation strategy in place.
- **M24 (04/2022)** SC3 T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) Arbor IO v.3 parameter space analysis Parameter space analysis notebook in EBRAINS.
- **M24 (04/2022)** SC3 T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) Arbor seeding functionality Validated seeding for stochastic sources.
- **M30 (10/2022)** SC3 T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) CEREB v.2 (with DCN) Notebook with CEREB v.2 in EBRAINS.
- **M30 (10/2022)** SC3 T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) OCC v.1 Integrated cerebellum and IO models.

## Arbor team status update

- User-defined gap junction mechanisms: 
    - https://github.com/arbor-sim/arbor/pull/1682
    - Gap junctions can now be represented using NMODL.
    - Available on the Arbor main branch since October. Will be part of Arbor v0.6 release (Jan 2022).
- Stochastic differential equations in the mechanisms:
    - https://github.com/arbor-sim/arbor/issues/1655
    - Issue details the implementation plan for representing SDEs in nmodl, utilizing the random123 CBRNG library, and seeding it through the simulation. It has been assigned to a new Arbor developer. It is planned for Arbor v0.7 release (April 2022). 
    - In the meantime, the mechanism ABI can be used to insert randomness into the mechanisms. 
    - [MG] Be aware variance of the input noise and the numerical solutions must scale with dt.
    - [ME] problem is that we do not use dt --> [MN] how to generalize dt/rng generation
    - [NA] further build-in rng for easy usage
- ODE descriptions of AMPA, GABA and NMDA synapses: 
    - https://github.com/arbor-sim/arbor/issues/1764
    - Sam was working on an ODE description of these mechanisms: 
    > The chief problem is that the physical model of what is going on with the diffusion remains unclear: it’s comprised of a burst phase (a square wave pulse of neurotransmitter) and a diffusion phase, one per spike event (which add up over time). Are multiple pre-synaptic emission sites being modeled, or one? Why does it saturate the synaptic cleft in the burst phase? That is, why isn’t it also governed by diffusion?
If the physical model can be pinned down, then we can make a discretized approximation to the diffusion PDE and we should then be good to go.

    - [NA] suggests to discuss with nmod file creator; SY joined 
    - [EdA, MN] model of AMPA etc. as used now (standard conductance based methods), [MN] simplify and average? [EdA] base model on experimentation, [MN] use same mechanism, [EdA] sends notes on pulse-wave model of neurotransmitter diffusion via mail
    - [NA] model not directly portable to Arbor; [SY] maybe use differential eqns; nmod problems with different states; diffusion uses approximation which we could use
    - [MN] literal solution copying model; simplified solution requires analytical work to fit --> [SY] pre-synaptic or ion specific (relies on discretization); [MN] there should be a parameterized solution; recast in phenomenological model? else summarize as standard AMPA
    - [EdA] counter-check with experimental data
    - [NA] for Arbor glutamate concentration over time, different states over time are issues; no way to simplify; discuss internally with [SY] and add [EdA, RG] into discussion
    - [MN] fallback/placeholder: use standard AMPA, NMDA, GABA, then look at differences in network; since no detailed description of model in deliverables; glutamate pre/post synapses should be least solution
    - **Summary: schedule meeting between NA, SY, RG And EdA to discuss the physical model of synapses. Papers and nmodl mechanism used by [SY] for analysis**
        - **LTP Regulates Burst Initiation and Frequency at Mossy Fiber–Granule Cell  Synapses of Rat Cerebellum:: https://pubmed.ncbi.nlm.nih.gov/16207782/**
        - **Spillover of glutamate onto synaptic AMPA receptors enhances fast transmission at a cerebellar synapse: https://pubmed.ncbi.nlm.nih.gov/12165473/**
         - **AMPA synapse: https://senselab.med.yale.edu/ModelDB/ShowModel?model=128446&file=%2fShortTermPlasticityMFGRC_Nieus2006%2fAmpa.mod**
    
```
    Michele does suggest looking at (extensive) literature on the topic and specifically:
    - Destexhe, Mainen & Sejnowski (1994) simplest Markov scheme for (any) synaptic receptor modelling  (https://doi.org/10.1007/BF00961734)
    - Lytton (1996) computationally efficient implementation (https://doi.org/10.1162/neco.1996.8.3.501.)
    - Giugliano et al. (1999) for a "fast-computation" method, generalising the above paper to short-term depression (https://doi.org/10.1162/089976699300016296)
    - Giugliano (2000) for a furthe generalisation to any Markov model and any short-term dynamics (https://doi.org/10.1162/089976600300015646) 
```

- Distributed Gap-junctions: 
    - https://github.com/arbor-sim/arbor/issues/1766
    - Leah Kanzleiter (Arbor team intern) is studying the feasilbility of using waveform relaxation to solve the problem. 
    - Max is working on a solution based on communicating the voltages at every timestep. 
    - [MN] not trivial to do WR using asymmetrical complex gap junctions as used in inferior olive (WR was only tested in Nest on symmetrical, linear GJ); concern is on level on charge exchange; [NA] will forward to [LK,TH]
    - [ME] will send [LL] a paper on WR: https://arxiv.org/abs/2105.06404
    - [SY] was looking at doi:10.1016/s0896-6273(02)00787-0 (glutamate-mediated synapses)
- Radial diffusion: 
    - Already available using NMODL annuli.
- Frontiers paper (Comparison of Arbor and Neuron performance): 
    - Robin visited Zurich offices last week.
    - Good progress was made on verifying the single cell models. 
    - We have started running some simulations with different setups on Piz-Daint. 
    - Good performance on GPU (with 1000 cells)

## Arborio team status update
- [LL] Youtube: https://www.youtube.com/watch?v=lnR_vHftwEk
    - [LL] sharing presentation notes, please share via email
- [RG] please share slides via email; 
    - validating single cell models with NA, differences in interpretations of numerical models; 
    - problems of accuracy of commands; 
    - speedup numbers x35, x10 (single cell), x300; 
    - next steps: integrate IO (meet with [LL] on 6th Dec); CC-IO-DCN loops
    - [MN] need AMPA, GABA models; problem will be memory; how to handle input to fibers? 
        - [RG] using localized simulation; spatially: in layer in 3D (column or cylinder); 
        - [MN] noise sources allows distributing input; we want: combination of different sources; [RG] agrees; 
        - [MN] connect CC with IO; [RG] do so immediately by first simulations (see [RRs] slides on 13 connection types)
        - [AG] missing spatial integration 
        - [AG] developing full scale model mapped on real shape (taken from atlas); can be interfaced into Arbor
        - [AG] work on conditioning with [CS]
        - [MN] make plan on which and when we add synapses

## Questions to the Arborio team

- [Arbor-design document](https://docs.google.com/document/d/1Amg6pIDxIh_D3ZYJwobF3vh8qNEVtrgkbOWsfytMPaw/edit)
    - Can we extract some feature requests or specific To-Dos for the Arbor team? 
- AMPA/NMDA/GABA synapses 
    - Who do we contact for discussions on the physical model? 
- Zero-delay synaptic connections in the network
    - Arbor (as well and Neuron and Nest) take advantage of delays in the synaptic connections to perform an important optimization, limiting the frequency of MPI communication to once every `min_delay` period. Zero-delay connections will incur performance penalties. If these kinds of connections are common and necessary, we may need a different communication model for them.
    - bring up next time with [EdA]
    - [SY] model as gap junction? [NA] connection are everywhere, thus no scaling (due to non-existing distributing GJs); [RG] create connections from soma; [NA] keep communication in mind 
- How far do your branches (for example the [gj_feature+emc_catalogue branch](https://github.com/max9901/arbor/tree/nora/gj_feature+emc_catalogue)) diverge from arbor master? What do we need to merge into Arbor-main to facilitate your work?
    - please open issues and tag us
    - [ME] not using branch anymore ([LL] agrees), instead using arbor master; no extra features needed; only issue with distribution of gap junctions
- Can we have access to the benchmark sources used in the Eden paper? Was the NMODL optimized or as-is from jNML? 

## Questions to the Arbor team

- Kindly keep and use an updated mailing list of the Arborio team members and share email alert and event invitation with them all. (M. Giugliano)

## State of the collaboration

- Are we on track for meeting the deliverables? 
- Are there any major blockers that are not being addressed by the Arbor team? 
-  Was the open developers meeting useful? Do we need to increase the frequency of the check-ins?
-  Is the Arbor team keeping up with the collaboration requirements so far, if not how can we improve?


