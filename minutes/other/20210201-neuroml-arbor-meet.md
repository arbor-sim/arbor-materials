Arbor, Openworm, NeuroMLlite
============================

https://github.com/OpenSourceBrain/ArborShowcase

# Agenda

--

## Arbor v0.5
* new: decor
* maps well to NeuroML.


## Mechs
* spatially variant descriptions (mmeee)
    * Currently Arbor don't have spatially variant descriptions
    * NeuroML has support for varying params like conductance density. Not a very tested feature?
        * No magical state vars
    * H. Model? Source?
        * Publication? Heyertal? 
        * Used by Bluebrain, Allen
    * In the meantime, a converter could discretize until Arbor has support.
* Inhomogeneous parameters in NeuroML docs
    * https://neuroml.org/NeuroML2CoreTypes/Cells.html#inhomogeneousParameter

* netpyne
    * Generate mod files from NeuroML

* Is there an Arbor native way to write mechanisms?
    * Soon: load user provided mod files
        * https://github.com/arbor-sim/arbor/pull/1287
    * Arbor supports a subset of NMODL
        * https://gist.github.com/noraabiakar/7149650c4b9bffefaad7b2c235ed91f6
        * These are also in the Arbor docs: https://arbor.readthedocs.io/en/latest/internals/nmodl.html?highlight=nmodl#nmodl but I've just added a few changes to the gist. 
    * Should be able to produce diffs of OpenWorm .mod against the Arbor variants

* Status of Calcium dynamics (compared to bluebrain scale)?
    * Cross ion dep we can do
    * Intermediate messenger (mRNA) for CA homoeostatis
        [1] S. Gorur-Shandilya, E. Marder, and T. O’Leary. 
            Activity-dependent compensation of cell size is vulnerable to
            targeted deletion of ion channels. 
            Scientific Reports, 10, 2020.
        [2] T. O’Leary, A. Williams, A. Fraci, and E. Marder. 
            Cell types, network homeostasis and pathological compensation
            from a biologically plausible ion channel expression model. 
            Neuron, 82:809–821, May 2014.
            
## Network
* What does Arbor support?
    * No I/O atm

## NeuroMLlite
* is high level template description of network (JSON compat format)
    * can be mapped into NeuroML, netpyne, Brain 
* TODO: Recipe-converter.

## GUIs
* Arbor-GUI
    * https://github.com/thorstenhater/arbor-gui
* Open source brain
    * https://www.opensourcebrain.org
    * v2 in pipeline
        * UI from Metacell re-used (Netpyne Simulator UI)
        * Map to NeuroML.

## User loadable mech
* Fastest way to get a mech (HH3?) into Arbor?
