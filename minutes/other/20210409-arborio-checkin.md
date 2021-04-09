Agenda Arborio Check-in
=======================

Arborio HBP Milestones
----------------------

- **M18 (10/2021)** SC3 T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) Arbor IO v.3 with glomeruli Arbor IO v.3 running on EBRAINS.
- **M18	(10/2021)** SC3	T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) MultiGPU feasibility study Implementation strategy in place.
    - blocker is gap junctions
    - we discussed that Sam, Nora, Max would keep working on distributed GJ implementation.
    - point was made that both the Cerebellum and Olive networks will need distribute gap junctions at scale.
- **M24 (04/2022)** SC3 T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) Arbor IO v.3 parameter space analysis Parameter space analysis notebook in EBRAINS.
- **M24 (04/2022)** SC3 T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) Arbor seeding functionality Validated seeding for stochastic sources.
- **M30 (10/2022)** SC3 T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) CEREB v.2 (with DCN) Notebook with CEREB v.2 in EBRAINS.
- **M30 (10/2022)** SC3 T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) OCC v.1 Integrated cerebellum and IO models.

Questions to the Arborio team:
------------------------------

- Are we on track for the first deliverable on M18 (October 2021)? What does the network look like: specifically are there non-linear gap junctions, and will complex synapses with large state (such as the AMPA, NMDA and GABA synapses) be needed?
    - v0.1 (starfish model) **already ported**
    - v0.2 stochastic sources will be required
        - references: Ornstein-Uhlenbeck.
        - Amo is the contact person for this.
    - v0.3 glomeruli will be required
        - requires asymmetric gj conductances (rectified)
        - radial diffusion required
- Can we have more details about the validated seeding for stochastic sources requirement?
    - A paper link was provided: https://journals.aps.org/pre/pdf/10.1103/PhysRevE.54.2084
- Regarding the AMPA, NMDA and GABA synapses: [This paper](https://journals.physiology.org/doi/pdf/10.1152/jn.00696.2005) indicates that the synapses can be represented by a 4-variable ODE system for the pre-synaptic model and a 3 or 5-state linear kinetic scheme for the postsynaptic conductance model. If we can confirm that the mathematical model is correct, we can re-write the synamics in terms of ODEs.
    - Go ahead: Robin will be our point of contact; also consider contacting Stefano Masoli (original author of the mechanisms)
    - Schedule another meeting to discuss common AMPA, GABA, NMDA mechanism models between olive and scaffold models.
    - References for calculations re: Markov schemes for reaction networks: doi:10.1162/089976600300015646 and doi:10.1162/089976699300016296 provided by Michele.
-  Is the Arbor team keeping up with the collaboration requirements so far, if not how can we improve?
    -  Positive feedback about interactions
    -  Optimizers running in Eden, deployed in Juelich. Eden parses NeuroML. Does not use Arbor though!
    -  Sandra/Alper working on Eden/L2L, talk to them about Arbor
    -  NeuroML outputs shoddy nmodl
        - Better support in Arbor would be great
        - (direct NeuroML support)
-  There is a [call for papers](https://www.frontiersin.org/research-topics/19349/neuroscience-computing-performance-and-benchmarks-why-it-matters-to-neuroscience-how-fast-we-can-com) that we could submit an abstract to.
    - Robin has mentioned informally his ability to generate ~1000 cell networks with a mix of cells from the scaffold model.
        - one thing missing: tool has no support for arbor.
    - Could this be used to generate a similar model for Arbor/(Core)Neuron and lead to a small benchmark, which might be submitted to the call?
    - Run on single GPU?
        - See how much we can run on single GPU?
- Second technical publication?
    - Maybe meet three way with FIPPA/Arborio for this?
        - Calcium activated plasticity mech
        - Prolbem: lot of data, long runtimes
        - In 6 months? Maybe have the first meet in july?

Questions to the Arbor team:
-----------------------------
- What is the current state of PRNG implementation?
- Estimate memory footprint of cells
    - Based on cell desc
    - One cell group in multiple local GPUs?

Minutes
=======

Date: 2021 04 09
Presence:

Prioritised TODO list
=====================

1. stochastic processes in mechanisms for v0.2 olive
1. axial diffusion for v0.2 olive (generated from NeuroML)
3. fancy pants gap junctions for v0.3 olive (M18)
4. ODE descriptions of GABA etc. synapses for Scaffold (M18)
5. distributed gap junctions
    - a detailed plan and POC (M18)
