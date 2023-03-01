## Meet w/ worshop folks

https://indico-jsc.fz-juelich.de/event/266/program
https://juchat.fz-juelich.de/channel/jsc-jwb-ts-22
Jayesh Badwaik, Jan-Oliver Mirus

## Juwels Booster

We get some compute time, 200 nodes, GPUs. A100

juwels-gpu: use cuda 70
juwels-booster: cuda 80

* you must compile onthe partition you wanna run on.
* Does it matter if you build on login-nodes?

## Use case: busy rings

Busy ring is many rings connected with weight zero connections. Zero weight between rings, nonzero within the local rings.

Use Allen in the busyring. Current cell only has HH. NSuite lets you change morpho? Generate random locations and connections. Locally connected soma to soma (or center, midway first branch of morpho).

Arbor is shipping spikes which don't do anything (between rings).

## NSuite

* https://github.com/arbor-sim/nsuite/blob/master/benchmarks/engines/busyring/arbor/ring.cpp
* https://nsuite.readthedocs.io/en/latest/

```
git clone https://github.com/thorstenhater/nsuite
cd nsuite
bash ./install-local.sh --env=systems/juwels-gpu.sh arbor
```

## Goal

Goal: bench more realistic workload, see if bottlenecks appear.

We have a tunable benchmark, we'd like to see how it performs. So far, very simple cell, and see how far we can strecht it, benchmark de communications overhead. 2019 paper shows we did this well. Next thing: more realistic workload: a more complex cell. The Allen cell.

Describe use case (busy rings).

Measure, find bottlenecks.

See scaling, some GPU profiles on different scales.

## Remarks

* Arbor struggles with low GPU occupation
    * reason is ion channel are compiled to kernel, that are not gpu filling.
    * Launch a lot of small kernels.
    * Launch overhead low, packed well.
    * Taskbranch: launch overhead goes up 2-3 orders of magnitude.
* Now: 1 process per node, any number of GPUs
    * Maybe: process per GPU?
    * MPS: https://docs.nvidia.com/deploy/mps/index.html

## Prep

* 6 min presentation
    * when
        * mo 7 march 13:30/14:30
    * who's there?
        * everyone in the workshop
    * in broad sense the application
    * the goal
    * the data structures you're using
        * arrays
    * the algorithms
        * tri-diagonal solver over a matrix.
        * solving many matrices, or one big?
            * one per cell
            * size: number of compartments
                * so 5k cvs is 5k x 5k matrix
        * in THs profile
            * blocks are epochs of half Tmin_delay
            * grey is kernel launches
                * Jan-Oliver would like to look at the kernels
            * some of the kernels expect to be run sequentially.
* give them the use case
    * see block that TH shared.
    * they are satisfied ATM
* give them one benchmark profile
    * can also do them on monday
* final request:
    * sketch of algorithm.

## where is stuff

Integration step: https://github.com/arbor-sim/arbor/blob/master/arbor/fvm_lowered_cell_impl.hpp#L192
Solver (CUDA): https://github.com/arbor-sim/arbor/blob/master/arbor/backends/gpu/matrix_fine.cu#L168
Ion channel kernels: catalogs. there will be a subdir in CMAKE build dir where the ion channel kernels are generated (from nmodl).

## How to share work
/p/project/training2204/arbor


 
