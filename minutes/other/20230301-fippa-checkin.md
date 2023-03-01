Agenda FIPPA Check-in
=======================

FIPPA HBP Milestones
--------------------

(https://drive.ebrains.eu/lib/22a9a2b5-51d6-4138-a64c-c9a62fef82ae/file/Roadmap/WP5%20Internal%20Milestones.xlsx): 
- **M18 (10/2021)** SC3 T5.16: The Functional Interplay between Plasticity Processes for Arbor (FIPPA) Extension of Arbor for initial support of plasticity and beta-release of code Arbor running with test plasticity rules.
    - Done
- **M27 (07/2022)** SC3 T5.16: The Functional Interplay between Plasticity Processes for Arbor (FIPPA) Full implementation of plasticity processes in Arbor and integration into upstream Arbor code base Arbor running with plasticity processes and release of source code.
    - Done
- **M34 (02/2023)** SC3 T5.16: The Functional Interplay between Plasticity Processes for Arbor (FIPPA) Simulation of full-scale, learning networks on HPC and release of code Plastic networks running on HPC and release of source code
    - Done, release of code not yet. In the next weeks.
- **M24 (04/2022)** MS5.3: Simulation/analysis workflows for each simulation scale & cosimulation, including integration in EBRAINS infrastructure, documentation, validation, visualization where appropriate, integration testing and user support workflows (SC3). Implementation available in a public repository, CI on appropriate systems where applicable, user and developer documentation available, workflows including example models/data accessible from the web.
    - 

FIPPA Outputs
-------------

(https://plus.humanbrainproject.eu/outputs?task=1175):
- **OP5.32** Open-source software release of ready-to-use blueprints, e.g. code examples, for other scientists to build upon in open standard network description languages compatible with the Arbor simulator
- **OP5.33** Open-source software release of code, tools and working examples based on the Arbor simulator
- **OP5.34** Open-source software release of Arbor-based network framework implemented on neuromorphic hardware
- Due date for all: 31 mar 2023

Questions to the FIPPA team: 
----------------------------

- DFG grant
    - Brief update
- What are the results of FIPPA?
    - Apart from the above milestones and outputs, have your goals been reached?
    - How do you see further cooperation?
    - Jannik Luboeinski: 
      * has reproduced the results of simulations of complex point-neuron networks
      * next extending the neurons to finite size and exploring the impact of protein transport on network effects
      * should have everything he needs to finish when the particle diffusion works properly
        - Network simulation should be public soon, great. 
        - Jannik will prep the simulation and release on GH
        - Brent will gladly fork any Github repo under https://github.com/arbor-contrib
        - This adds Arbor to the 2021 paper, planned to be published.
            - Possibly collab on this, and highlight plasticity dev in Arbor?
            - Or consider make this a separate publication.
                - BH: list what is new in Arbor since last pub.
        - SS: break down into 3 models, for educational and debugging purposes.
            - single cell
            - network ( <-minimum level for publication. )
            - diffusion/multicompartment
- Some issues with Arbor
    - Arbor roughly 10x slower than own code.
        - TH+JL will setup a meet to look into where the cycles are going.
    - diffusion units
    - summary document is in prep, Arbor Team will get this ASAP.
        - ETA end of march
        - diffusion and multicompartment: later.
        - Let's meet early april on how our progress is. (UMG paper, and our update 'paper')

Questions to the Arbor team:
----------------------------

- Offline.

Future grants, publications
---------------------------

- Possibly collab on the paper of Jannik.
    - We are in touch.

Minutes
=======

Date: 2023-03-01 09:00
Presence: BH, CT, TH, JL, SS

 
