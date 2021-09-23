## present: BH, TH, NA, RDS

#### Goal: perf comp between Arbor and Neuron

#### Tool: scaffold

* 31k cell model runs now.
    * missing, no technical work needed
        * gap junc
            * ohmic ones
        * only soma-soma connections, not placed correctly
        * 
    * missing, technical work needed
        * (some) synapse models

* Performance
    * Nora makes a fix today for range vars
    * Nora takes look at all mechs looking for optimizations
    * profiler should record which mechs take longest.

* paper
    * which models
        * 31k one = {cerebellar scaffold model}
            * 8000s/150ms in Arbor, w/o vectorization, w/o range vars
            * 6.5hrs/8000ms in Neuron
                * bluepyopt method, max 40um compartments
            * Arbor is 13x slower.
            * TODO: same dt, compartmentalization?
              * CV policy
                ```py
                arborize/arborize/core.py
                387: dflt_policy = arbor.cv_policy_max_extent(40.0)
                388: soma_policy = arbor.cv_policy_fixed_per_branch(1, '(tag 1)')
                ```
               * dt, default = 0.0025
                 ```py
                 bsb/bsb/simulators/arbor/adapter.py
                 159: simulation.run(tfinal=5000)
                 ```
            * Repo?
                * https://github.com/dbbs-lab/catalogue/pull/1/files
                * will we publish this?
                    * submit as model?
        * other models?
            * the above model can be scaled in number in cells
            * generate new models?
        * How to compare them?
            * CPU, GPU (Nora can arrange this)
            * scale cell nbr
            * 
* Question for Robin
    * turn on profiler and send results to Nora/Thorsten
    * send link to scaffold paper on bioarxiv
        * https://www.biorxiv.org/content/10.1101/2021.07.30.454314v1.full
    * try to scale mpi processes with (NUMA) node (socket), not core. have arbor thread within the node.
        * for neuron there is no other way.
    * scale down to 1k cells
    * check discretization, dt

#### Political background

* Author lists?
    * 
* Running = enough for Egidio (prof. of RDS), optimizing is job for team Arbor

#### Paper source

https://www.overleaf.com/8987799378zvbyxqhzsjdj 
