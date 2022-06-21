# Arbor Vision Meet 2022 06 21

Presence: BH, FB, TH, BC, SF

## Round table

### Ben

- Focus on an essential science feature @ scale that is not-available/non-performant/awful with NEURON
    - implement it well and demonstrate it @ scale
    - BC suggests distributed gap junctions (there might be others?)
- Arblang is nice to have: maybe not as high a priority as other more impactful science features

### Fabian

 - Arbor becomes the best software for large-scale brain simulations, and advances the field of Neurobiology.
 - How
    - Strive towards a full-scale brain simulation.
    - Make it fast, scalable and versatile.
    - Win Gordon Bell Price.
    - Onboard Neurobiologists.
- Focus: scalability
    - distributed gap junctions
    - time stepping
    - GPU performance

### Thorsten

Neuron's killer feature is the ecosystem that surrounds it
- a convenient toolbox that looks nice and works nice is require to get users to invest in the "ecosystem"
- you get scientists on board to build models that we can scale up
    - Arbor can scale up & gap junctions are on the way: the building models is missing

### Simon


### Brent

Want to get scientists on board. This means: dragging them in by their hairs, and attracting them with an ecosystem.

0. We may have won Robin for the cause. He has his own and a shared poster presentation at CNS in Australia.
1. In cahoots with Mario on Lennarts PhD. We have offered a 6 month project in meantime.
2. Allen Institute: discuss Arbor NMODL/NML support. Work with Stefan Mihalas: get some of his models ported, see if this gets him interested, and in turn Allen on board with Arbor/interop
3. Fippa: not getting a lot of feedback there lately.

### Summary

There were some recurring themes between the visions:

- Focus on ecosystem-tooling for getting scientists to buy in (see below for suggestions on what is in such an ecosystem).
- Focus on big science feature running at scale on pre-exascale/exascale HPC systems (mostly GPUs) - double down on performance and scale benefits of Arbor over other tools
    - ensure that GPU version is as well tested as cpu -> GPU CI
    - focus on testing and improving GPU performance and seeking out use cases that benefit GPU.
    - Distributed gap junctions were a common choice for such a feature.
- Focus on quality of user-community interactions
    - retain users and advertise
    - close collaboration: personal relationships.

## Other remarks

### PRs

- Diffusion PR is ready to merge
    - TH can update the commit message, then it can merge
- A64FX CI has been dropped due to unresolved SLURM issues on Ault
    - We will test on ARM dev kits.
- 


### On Ecosystems

What are essential tools for a "detailed cell model toolkit/ecosystem"?
- BC: Single cell parameter optimisation in framework like BluePyOpt
- BC: visual single cell model building tool
- BC: Network building tooling
    - support for NeuroML-lite
    - network description DSL
- BH: File format / model database compat
    - More ready-to-run models
    - NeuroML
- BC: consistent representation for single cell models using ACC format:
    - sample models available online in consistent format
    - ensure that tools like ArborGUI and parameter optimization
    - **note** we are not far from an all-in-one solution. Some remaining issues to work out
        - catalogues are not in ACC
        - probes are not in ACC

A key point is that much of the ecosystem tooling is ad-hoc and in house
    - a focus on tooling that encourages more consistent model representations with a well defined set of tools and workflows.

### Action Points

- [ ] Next meet: other meeting software 
