Arblang Meeting 12.07.2021
==========================

## Examples from last week, corrected: 
### BBP catalogue/ CaDynamics_E2
- Concentrations: switching to flux: 
    - Is this a change from storing the concentrations in `M` to `M/area`?
    - How is it related to charge? Non-specific concentrations? 
    - Currently: the ioninc current used in ion concentration calculations is a current density, so it is already per unit area. But the concentrations are not. How do the units work out? 
        - unit confusion: 1 M = 1 mol/L = 1000 mol/m^3;
```
interface concentration_process "CaDynamics" {
    constant charge faraday = 96485.3321233100184 C*mol^-1;
    parameter scalar gamma = 0.05;
    parameter time decay = 80 ms; 
    parameter length depth = 0.1 um;
    parameter amount minCai = 1e-4 mM
    # parameter amount initCai = 5e-5 mM;   # initialized arbor-side

    # Units only work is concentrations are amount, not amount/area
    # -5000*i*gamma/(faraday*depth) - (c - minCai)/decay;
    # (mA/m^2)/(C*mol^-1*um) - (mM - mM)/ms
    # (mA*mol)/(m^2*um*C) - mM/ms
    # (mA*mol)/(10^-6*m^3*A*s) - M/s
    # (10^3*mol)/(m^3*s) - M/s
    # M/s - M/s 
    # M/s
    def evolution(amount/area c, current/area i) -> amount/area/time {
        -5*i*gamma/(faraday*depth) - (c - minCai)/decay;
    }

    bind ica = ionic_current("ca");
    bind cai = process_state; 

    evolve evolution(cai, ica);
    internal_concentration("ca") = cai;
}
```

### Default catalogue/ Nernst
```
# **Nernst and all other reversal potential calculations will be
# absorbed into mechanism descriptions, and removed from arbor. 
# Ions that need the reversal potential calculated by a rev_pot 
# mechanism can import the module of a that mechanism and call the 
# `erev` function.**
module nernst {
constant R = 8.31446261815324 J*k^-1*M^-1;
constant F = 96485.3321233100184 C*M^-1;

def erev(temperature t, amount ci, amount co, scalar valence) -> voltage {
    R*t/valence*F
}
} # module nernst
```

## The compiler
- [NA] thinks we will soon have a good enough first version of the language to start desigining the compiler. 
- We can limit the initial version of the compiler to cover the current capabilities of modcc. That is, mechanisms that: 
    - have internal state variables and update them using ODEs or kinetic reactions only. No direct assignment except at initialization.
    - contribute to ionic current densities.
    - use internal and external ionic concentration densities (fluxes) and reversal potentials.
    - contriute to internal and external concentration fluxes using ODEs or kinetic reactions only. 
    - Can not set the ionic internal or external concentration fluxes. 
    - Can update state variables and perhaps ionic concentration fluxes on receipt of external or internal spikes (for point mechanisms).
- Next step is to de-sugar the language and continue writing our specifications document. 

## Other:
- 19/07/2021 meeting conflict. Can we move till 14:00? [TH] should be back, [NA] can check with him too.
