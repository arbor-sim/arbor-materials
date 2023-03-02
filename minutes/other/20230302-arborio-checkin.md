Agenda Arborio Check-in
=======================

Arborio HBP Milestones
--------------------

- **M18 (10/2021)** SC3 T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) Arbor IO v.3 with glomeruli Arbor IO v.3 running on EBRAINS.
    - Arbor IO v.3 with glomeruli
        - Done.
        - Compartments were gonna be small.
        - Requires 1e-5 ms timesteps.
        - 
    - Arbor has voltage processes, ext of what NRN allows. Can write directly to voltage. Used for voltage clamps. Not tested beyond that.
    - Writing this up.
- **M18	(10/2021)** SC3	T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) MultiGPU feasibility study Implementation strategy in place.
    - MultiGPU gap juncs was hacked by Max.
        - Max & Lennart have to write a report.
            - [ ] Come back later: Preserve Max's mGPU branch, share this lesson. 
        - Have category in documentation: user experience.
    - (other impl: waveform relaxation. Initial plan was to race these, but not done.)
    - We can pas this to Fabian
- **M24 (04/2022)** SC3 T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) Arbor IO v.3 parameter space analysis Parameter space analysis notebook in EBRAINS.
    - Was about network balancing, but is done dynamically.
    - Yes. https://wiki.ebrains.eu/bin/view/Collabs/io-clusters/Lab
- **M24 (04/2022)** SC3 T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) Arbor seeding functionality Validated seeding for stochastic sources.
    - Challenge: mGPU _sharing_ noise sources. Didn't get around to this.
    - Literal text: reached. But desired functionality: not reached.
    - This wasn't well specified: should have said 'correlated noise', not poisson process. This was not implemented (only uncorrelated noise).
    - For IO, correlated noise is essential, because that's the signals from eg muscularskeletal coming into it.
    - [ ] Fabian: create a noise source cell (current source cell), that communicaties over gjs.
    - [ ] Move beyond trees in space: electrical fields.
- **M30 (10/2022)** SC3 T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) CEREB v.2 (with DCN) Notebook with CEREB v.2 in EBRAINS.
    - In the works.
    - (Discussion)
    - [ ] Possibly new point neurons needed. 
        - Existing issue: https://github.com/arbor-sim/arbor/issues/1832
        - Example of LIF, AdEx through mech (pre voltage processes):
            - https://github.com/arbor-contrib/FIPPA/tree/main/STDP
            - https://github.com/arbor-contrib/FIPPA/tree/main/AdEx
        - Clock cell?
    - Ion (eg Ca) diffusion: https://github.com/arbor-sim/arbor/pull/1729
- **M30 (10/2022)** SC3 T5.18: Arbor Implementation of the Inferior Olive Network (ArborIO) (SC3) OCC v.1 Integrated cerebellum and IO models.
    - 

Outputs
-------

- [ ] Brent: should be one output. Find it.
    - Mario: had exchange with Anne Elfgen on this last year.

Points in Mario's email
-----------------------

0. [x] Hooking up Pavia’s cerebellum with our IO. @Robin, @Lennart, @Claudia, @Alice. We had a nice document 
   <https://docs.google.com/document/d/1JkbLvlswfjwI7o_zmAXIfGdDylKp18_P/edit?usp=sharing&ouid=114308445511154268444&rtpof=true&sd=true> 
   where we began but did not continue. 
   Shall we meet to decide on the number of cells and connectivity? 
   We would like a scaleable network (so we can put a upload and curate a running version in EBRAINS). 
   @Pavia: can you propose some numbers in that document and we move from there?
2. We need a curated version of Arbor' inferior olive in EBRAINS in Arbor. 
   - How is pip doing? 
   - Does it support all required features? 
   - How about scale: what is the maximum size of IO net that we can run without requesting extra computational resources?
4. Same for the olivo-cerebellum @Robin, @Lennart
5. Validation of stochastic sources updates: @Amo, @Michele, @Lennart
    - [ ] Report by Amo

Questions to the Arborio team: 
----------------------------

- What are the results of Arborio?
    - Apart from the above milestones and outputs, have your goals been reached?
    - How do you see further cooperation?
        - If the IO model is in Arbor, lots of science possible!
        - Mario got convergence grant Delft<>Rotterdam, can hire a PhD.
            - Experimental Recordings
            - NML mech descriptions lack effectic currents
            - So Arbor is logical choice for this PhD.
            - ASAP
- Lennart Landsmeer
    - Starts PhD 15 March
    - Are further Arbor studies foreseen?

Questions to the Arbor team:
----------------------------



Ebrains Collab link
-------------------

https://wiki.ebrains.eu/bin/view/Collabs/io-clusters/Lab

Minutes
=======

Action points
=============

- [ ] Brent: https://wiki.ebrains.eu/bin/view/Collabs/io-clusters/Lab in docs?
- [ ] Robin travels to Rotterdam
- [ ] Brent sets new meet last week of august
- [ ] Preserve Max's mGPU branch, have his report, share this lesson.
- [ ] Fabian: create a noise source cell (current source cell), that communicaties over gjs.
- [ ] Possibly new point neurons needed. 
- [ ] Report by Amo on validation of stochastic sources.

Date: 2023-03-02 12:00
Presence: MN, RdS, BH, TH, CC

 
