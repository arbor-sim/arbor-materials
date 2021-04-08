Agenda FIPPA Check-in
=======================

Seb presentation
----------------

* Arbor docs: do not require NRN knowledge. NMODL. But there's no way around it.
* Complex network examples: missing
    -> higher level network description: who takes responsibility, NeuroML, Arbor?
    -> Have an Arbor recipe based on populations and connections between them
* I/O formats/containers is up to user: not ideal!
* Arbors LIF cell is incomplete
    -> Let's have a ticket with specific requirements
* FIPPA Roadmap
    * Voltage/calcium based plasticity (as opposed to event-based plasticity?)
    * No radial diffusion required (?)
    * Needed: an order/timeline

FIPPA HBP Milestones
--------------------

(https://drive.ebrains.eu/lib/22a9a2b5-51d6-4138-a64c-c9a62fef82ae/file/Roadmap/WP5%20Internal%20Milestones.xlsx):
- **M18 (10/2021)** SC3 T5.16: The Functional Interplay between Plasticity Processes for Arbor (FIPPA) Extension of Arbor for initial support of plasticity and beta-release of code Arbor running with test plasticity rules.
    - Pretty much achieved, add small networks and analysis to example?
- **M27 (07/2022)** SC3 T5.16: The Functional Interplay between Plasticity Processes for Arbor (FIPPA) Full implementation of plasticity processes in Arbor and integration into upstream Arbor code base Arbor running with plasticity processes and release of source code.
    - What is a full implementation?
- **M34 (02/2023)** SC3 T5.16: The Functional Interplay between Plasticity Processes for Arbor (FIPPA) Simulation of full-scale, learning networks on HPC and release of code Plastic networks running on HPC and release of source code
    - Relies on the former MS
- **M24 (04/2022)** MS5.3: Simulation/analysis workflows for each simulation scale & cosimulation, including integration in EBRAINS infrastructure, documentation, validation, visualization where appropriate, integration testing and user support workflows (SC3). Implementation available in a public repository, CI on appropriate systems where applicable, user and developer documentation available, workflows including example models/data accessible from the web.
    - Have what we have on Ebrains

FIPPA Outputs
-------------

(https://plus.humanbrainproject.eu/outputs?task=1175):
- **OP5.32** Open-source software release of ready-to-use blueprints, e.g. code examples, for other scientists to build upon in open standard network description languages compatible with the Arbor simulator
- **OP5.33** Open-source software release of code, tools and working examples based on the Arbor simulator
- **OP5.34** Open-source software release of Arbor-based network framework implemented on neuromorphic hardware
- Due date for all: 31 mar 2023

Questions to the FIPPA team:
----------------------------

- Is the `POST_EVENTS` functionality for supporting spike-time dependent plasticity ([PR 1255](https://github.com/arbor-sim/arbor/pull/1255)) sufficient for the initial deliverable on M18 (October 2021)? If not, what else is required?
    - It's sufficient for M18.
- What other kinds of plasticity models does Arbor need to support? Are there any resources (papers, mathermatical models, any other resource) that we can refer to?
    - See FIPPA roadmap.
- Would it be possible to publish the models obtained as a result of the collaboration on Ebrains?
    - Yes
- Is the Arbor team keeping up with the collaboration requirements so far, if not how can we improve?
    - -
- Extracellular?
    - Not 3D in space, along dendrites
- Long term funding for FIPPA (German science foundation, collab. research of synapses at Goettingen).
    - Applied for additional 4 years
        - High chance of getting it, May definitive answer. July the 4 years funding period would start.
    - Can be extend by another 4 years.
    - Plan: Abstract model of synapse dynamics
- Any Arbor papers planned?
    - WIP
    - Another project started on dendritic processes.
        - Network level is where not much publications have been done.
    - Technical publication?
        - Maybe meet three way with FIPPA/Arborio for this?

Questions to the Arbor team:
----------------------------



Minutes
=======

Date: 2021 04 08
Presence: Christian, Sebastian, Sam, Nora, Thorsten, Brent, Ben


