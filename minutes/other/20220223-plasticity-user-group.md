# han

hippocampel tissue culture

model what she sees in experiments.

# sebastian

plasticity is often some variant of time dep spike timing plasticity

is far from biological reality. no real notion of spike of singular pount in time, thats modules in reaction chains, often mediated by calcium, long term potentiation.

bring different ___ in simulation

heterosynaptic plasticity. how if and by which mechs morphology influences plasticity. move away from point neurons.

# han

does imaging, colleagues to ___ recordings. apical, distal, ___ dendrite show different activity. before used point neurons with dendritic elements. would be interesting if with arbor more detailed modelling structural plasticity .... differentiated ....

homeostatic is w respect to firing.

# sandra

in nest, just point neuron, but can create dendritic 'elements', abstract 'morph', different growth rules for diff elements. In NEST, no positions in space, rules are position agnostic.

spines along morph, and relationship to other cells in space, using delays and other abstract properties.

have stdp in arbor.

# seb

has rate based homeostatis model in arbor, will send link. https://github.com/tetzlab/FIPPA/tree/main/spike_based_homeostasis

# sandra

extend this to the whole morph, exploit other features. interested in stimulation. how to model stim protocols?

# han
 
will send video of dynamics later (video link here: https://drive.google.com/drive/folders/13N4T49fPu4t2_-OVY0P2AKW9V6BNDsEe?usp=sharing) green signal is calium signal, red is tdTomato to label transfected neurons. 

# thorsten

dynamically probe ca conc and see if matches up with Han's video.

use a virus ... to extract ca conc in experiment

slow wave of ca signal. perturb of culture with magnetic field, slow wave osc is gone. instead, indiviual neurons get very active. timescale of few minutes, then osc recoveres. 

slab? cellular compartments.

# th

were thinking of ca diffusion on the dendrite in arbor

we have a gui tool to show this in 3D. might add conc viewer to gui

# sandra

local rules for this, spine growth, maybe form new connec with neurons 'around'

# han

firing activity maintains spines. may be (pre)synaptic activity. post synaptic may react locally. 

use calcium based homeostatic rule.

# th 

do you have some of these models already?

# sandra

no. growth rules can dep on ca conc.

take look at what seb has done, look at his link

changes weight of the synapse. next step: create or remove the synapse.

# seb

first iter an be to have change many potential synapses. (zero weight or no synapse has no diff). need a bench to investigate performance impact.

# th

check weight, if zero, bail.

# sandra

couple thousands synapses per neuron, maybe 10k. network size: couple thou as well. (TH can be on 1 gpu). then couple million! (few thou gpus).

# th

10 thousands cells: more then gpu is favorable.

do you have an application for computation power?

# sandra

we applied at jewels, proj related to learning. could be used. can think of dedicated prop, next period.

# th

ICEI also possible, lighter weight. JUSUF also has gpus.

# sandra

how to move forward?

what can we do? what need from us?

we'd appreciate workshop. 

we could have sth bigger than one tutorial: we could gather a group interested in plasticity in morph neurons, building a community. intro to Arbor. then brainstorming session. what's there, what's needed. potential usecases, users?

seb might also know some people, some hans colleagues also. Arborio?

* Gather some names
* intro arbor
* plasticity intro/arbor demo
    * https://github.com/tetzlab/FIPPA/tree/main/spike_based_homeostasis
* brainstorm plasticity.
    * come up with todo, use case, more?

maybe ask cns workshop (Melbourne), bernstein (berlin), hbp (anywhere), https://forum.fens.org/ satelite event (paris)?

# ACTION items

* brent and sandra setup tutorial in two/three weeks.
    * who: seb might also know some people, some han's colleagues also. Arborio?
* setup shared doc with ideas on workshop, keep in mind deadline april fens.










 
