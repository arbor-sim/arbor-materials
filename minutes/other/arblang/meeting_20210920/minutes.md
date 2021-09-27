Arblang Team Meeting 2021 09 20
===============================

Presence: NA, SY

- [NA] Had some suggestions on how to change the syntax of arblang to make the language more regular and hopefully more attractive to users. [SY] agreed with and helped decide on an alternative syntax, but maintained that we should keep the original format and specifications of the language, thereby allowing users to write their mechanisms in one of multiple ways (for example for defining functions and records). 
- Discussed topics: 
    - Parameter declaration split from parameter export. This is more verbose but is ultimately neater. A declared parameter can be set an used in the mechanism, but only an exported parameter can be overriden from the simulator code. 
    - Pre-declaration of state parameters. These are the internal parameters of the mechanism that can be altered during the course of the simulation. They are defined using the keyword `state`; they are initialized in the `initial` expression; they evolve according to a system of differential equations defined in the `evolve` expression; they are directly assigned to when `on_event` and `on_post` events occur, or when a regime change happens which is captured with `when` expressions. 
    - `state` no longer a bindable. 
    - Formalizing semicolon usage. They are optional after "declarations" (top-level statements in the interface). They are mandatory after assignment expressions. They are forbidden in record type definitions (swapped out for commas).
    - Sugar for declaraing function and record types to make them more like mainstream programming languages. 
    - Changes to `steadystate` and `evolve_for` syntax to accomodate the changes to `state` parameters.
    - Using underscore instead of keywords separated by space (`current density` -> `current_density`).
    - When do we use quoted string-literals? With the current syntax, it is limited to the `interface` and `module` names, as well as ion names. The reason these are string-literal is because they are values either set by or accessible by the simulator. However, by that logic exported parameter names should also be quoted, which they aren't. 

## Examples 
- Original examples written in the agreed upon arblang syntax can be sound here: https://github.com/arbor-sim/arblang/pull/6.
- The examples are annotated with more suggestions. 

### CaDynamics

```
# Suggestion: use `mechanism` instead of `interface`.
mechanism concentration "CaDynamics" {
    # Declare parameters
    parameter gamma = 0.05;    # Proportion of unbuffered calcium.
    parameter decay = 80 ms;   # Calcium removal time constant.
    parameter minCai = 1e-4 mM;
    parameter depth = 0.1 µm;  # Depth of shell.

    # Declare bindings
    bind flux = molar_flux("ca");
    bind cai = internal_concentration("ca");
    
    # Define mechanism callbacks
    effect molar_flow_rate("ca") = -gamma*flux - (cai - minCai)/decay;
    
    # Declare exports (Only for parameters. Only exported parameters can be 
    # set by the users from the simulation.)
    export gamma; 
    export decay; 
    export minCai;
    export depth; 
}
```

### expsyn_stdp

```
mechanism discrete "expsyn_stdp" {
    # Declare parameters
    parameter A     =  1 μS;    # pre-synaptic event contribution factor
    parameter Apre  =  0.01 μS; # pre-synaptic event plasticity contribution
    parameter Apost = -0.01 μS; # post-synaptic event plasticity contribution

    parameter τ      = 2 ms;    # synaptic time constant
    parameter τpre  = 10 ms;    # pre-synaptic plasticity contrib time constant
    parameter τpost = 10 ms;    # post-synaptic plasticity contrib time constant

    parameter gmax  = 10 μS;    # maximum synaptic conductance
    parameter e = 0 mV;         # reversal potential

    # Define record type (use commas here)
    record state_rec {
        g:         conductance,
        apre:      conductance,
        apost:     conductance,
        w_plastic: conductance,
    }
    
    # Declare state
    state expsyn: state_rec;
    
    # Declare bindings 
    bind v = membrane_potential;
    
    # Define helper functions
    function external_spike(s: state_rec, weight: real): state_rec {
       let x = s.g + s.w_plastic + weight*A;
       let g = if      x < 0 S then 0S
               else if x > gmax then gmax
               else    x;
       let apre = s.apre + Apre; 
       let w_plastic = S.w_plastic + S.apost;
       state_rec {
           g = g;
           apre = apre; 
           apost = s.apost; 
           w_plastic = w_plastic;
       }
    }
    
    function local_spike(s: state_rec) -> state_rec {
       let apost = S.apost + Apost;
       let w_plastic = S.w_plastic + S.apre;
       state_rec {
           g = s.g;
           apre = s.apre;
           apost = apost;
           w_plastic = w_plastic
       };
    }
    
    # Define mechanism callbacks
    initial expsyn = state_rec {
        g         = 0 μS;
        apre      = 0 μS;
        apost     = 0 μS;
        w_plastic = 0 μS;
    }
    
    evolve expsyn' = state_rec' {
        g'    = -expsyn.g/τ;
        apre' = -expsyn.apre/τpre;
        apost'= -expsyn.apost/τpost;
    };
    
    effect current = state.g*(v - e);
    
    # [NA] Is the `on` syntax confusing? 
    on w = event; expsyn = external_spike(state, w);
    on t = post;  expysn = local_spike(state);
    
    # Maybe this instead?
    # on_event(w) expsyn = external_spike(state, w);
    # on_post(t)  expysn = local_spike(state);
    
    # Declare exports
    export A;
    export Apre;
    export Apost; 
    export τ;
    export τpre;
    export τpost;
    export gmax;
    export e;
}
```

### Kd
```
module "Kd" {
    # Declare parameters
    density parameter gbar = 10^-5 S/cm^2;
    
    # Define types
    record state_rec {
        m: real,
        h: real,
    };

    # Define helper functions
    function mInf(v: voltage) -> real {
        1 - 1/(1 + exp((v + 43 mV)/8 mV))
    };

    function hInf(v: voltage) -> real {
        1/(1 + exp((v + 67 mV)/7.3 mV));
    }

    function state0(v: voltage) -> state_rec {
        state_rec {
            m = mInf(v);
            h = hInf(v);
        };
    };

    function rate(s: state_rec, v: voltage) -> state_rec' {
        state_rec'{
            m' = (s.m - mInf(v))/1 ms;
            h' = (s.h - hInf(v))/1500 ms;
        };
    }

    function current(s: state_rec, v_minus_ek: voltage) -> current/area {
        gbar*s.m*s.h*v_minus_ek;
    }
}

mechanism density "Kd" {
    # Declare imports
    import Kd
    
    # Declare parameters
    parameter ek = -77 mV;
    
    # Declare state
    state Kd_state: Kd.state_rec;
    
    # Declare bindings 
    bind v = membrane_potential;

    # Define mechanism callbacks
    initial Kd_state = state0(v);
    evolve Kd_state' = rate(Kd_state, v);
    effect current_density("k") = current(Kd_state, v - ek);
    
    # Declare exports
    export Kd.gbar as gbar;
    export ek;
}

mechanism density "Kd_nernst" {
    import Kd
    state Kd_state: Kd.state_rec;
    bind v = membrane_potential;
    bind ek = nernst_potential("k");

    initial Kd_state = state0(v);
    evolve Kd_state' = rate(Kd_state, v);
    effect current_density("k") = current(Kd_state, v - ek);
    
    export Kd.gbar as gbar;
}

# Kd_nernst is equivalent to:
#
# mechanism density "Kd_nernst" {
#     import Kd
#
#     state Kd_state = Kd.state_rec;
#     bind v = membrane_potential;
#     bind T = temperature;
#     bind ki = internal_concentration("k");
#     bind ko = external_concentration("k");
#     bind kz = charge("k");
#
#     initial Kd_state = state0(v);
#     evolve Kd_state' = rate(Kd_state, v);
#     effect current_density("k") =
#         let ek = nernst(kz, T, ki, ko);
#         current(state, v - ek);
# }

```

### NaTs
```
mechanism density "NaTs" {
    # Define types
    type rate = real/time;
    
    # Declare bindings
    bind T = temperature;
    bind v = membrane_potential;
    bind ena = nernst_potential("na");
    
    # Declare parameters
    density parameter gbar    = 10^-5 S/cm^2;

    parameter maF: rate       = 0.182 ms⁻¹;
    parameter mbF: rate       = 0.124 ms⁻¹;
    parameter mvh: voltage    = -40 mV;
    parameter mk:  voltage    = 6 mV;

    parameter haF: rate       = 0.015 ms⁻¹;
    parameter hbF: rate       = 0.015 ms⁻¹;
    parameter hvh: voltage    = -66 mV;
    parameter hk:  voltage    = 6 mV;
    
    # qt can't be exported. How will the compiler deal with it? 
    parameter qt = 2.3^((T-296.15 K)/10 K);

    # Declare state
    state m: real;
    state h: real;
    
    # Define helper functions 
    # These functions have complex return types 
    # which are inferred by the compiler
    function rate_m(v: voltage) {
        let ma = maF*mk/exprel((mvh-v)/mk);
        let mb = mbF*mk/exprel((v-mvh)/mk);
        {
            mi = ma/(ma + mb);
            mt = 1/(ma + mb)/qt;
        };
    }
    
    function rate_h(v: voltage) {
        let ha = haF*hk/exprel((v-hvh)/hk);
        let hb = hbF*hk/exprel((hvh-v)/hk);
        {
            hi = ha/(ha + hb);
            ht = 1/(ha + hb)/qt;
        };
    }

    # Define mechanism callbacks.
    initial m = rate_m(v).mi;
    initial h = rate_h(v).hi;
    
    evolve m' = 
       let rate = rate_m(v); 
       m' = (rate.mi - m)/rate.mt;
       
   evolve h' = 
       let rate = rate_h(v); 
       h' = (rate.hi - m)/rate.ht;

    effect current_density("na") = gbar*m*m*m*h*(v - ena);
    
    # Declare exports
    export gbar;
    export maF, haF;
    export mbF, hbF;
    export mvh, hbh;
    export mk,  hk;
}

```

## Nav
```
mechanism density "NaV" {
    # Declare parameters
    density parameter gbar = 0.015 S/cm²;

    parameter Con  =  0.01 ms⁻¹; # closed C1 → inactivated I1 transition
    parameter Coff =  40   ms⁻¹; # inactivated I1 → closed C1 transitions
    parameter Oon  =  8    ms⁻¹; # open O → inactivated I6 transition
    parameter Ooff =  0.05 ms⁻¹; # inactivated I6 → open O transition
    parameter a =   400    ms⁻¹; # closed Cx right transitions (activation)
    parameter b =    12    ms⁻¹; # closed Cx left transitions (deactivation)
    parameter g =   250    ms⁻¹; # closed → open transition
    parameter d =    60    ms⁻¹; # open → closed transition

    parameter a_f = 2.51;        # factor for right Ix transitions
    parameter b_f = 5.32;        # inverse factor for left Ix transitions

    parameter avdep =  24 mV;    # Vdep of activation
    parameter bvdep = -24 mV;    # Vdep of deactivation

    # Define type and declare state
    record state_rec = {
        C1: real;
        C2: real;
        C3: real;
        C4: real;
        C5: real;
        O:  real;
        I1: real;
        I2: real;
        I3: real;
        I4: real;
        I5: real;
        I6: real;
    };
    state Nav_state: state_rec;
    
    # Declare bindings
    bind v = membrane_potential;
    bind T = temperature;
    bind ena = nernst_potential("na");

    # Define helper functions
    function kinetics (s: state_rec, v: voltage, Q: real) -> state_rec' {
        let Con  = Q*Con;
        let Coff = Q*Coff;
        let Oon  = Q*Oon;
        let Ooff = Q*Ooff;
        let a    = Q*a*exp(v/avdep);
        let b    = Q*b*exp(v/bvdep);
        let g    = Q*g;
        let d    = Q*d;

        with s; 
        {
            C1 <-> C2  ( 4*s,   b );
            C2 <-> C3  ( 3*s, 2*b );
            C3 <-> C4  ( 2*s, 3*b );
            C4 <-> C5  (   s, 4*b );
            C5 <-> O   (   g,   d );

            I1 <-> I2  ( 4*a_f*a,   b/b_f );
            I2 <-> I2  ( 3*a_f*a, 2*b/b_f );
            I3 <-> I4  ( 2*a_f*a, 3*b/b_f );
            I4 <-> I5  (   a_f*a, 4*b/b_f );
            I5 <-> I6  (     g,   d   );

            C1 <-> I1  (     Con, Coff    );
            C2 <-> I2  (    a_f*Con, Coff/b_f  );
            C3 <-> I3  (  a_f^2*Con, Coff/b_f^2 );
            C4 <-> I4  (  a_f^3*Con, Coff/b_f^3 );
            C5 <-> I5  (  a_f^4*Con, Coff/b_F^4 );
            O  <-> I6  (     Oon, Ooff    );
        };
    }

    function qt(T: temperature) → real {
        2.3^((T - 310.15 K)/10 K);
    }

    # Define mechanism callbacks
    parameter steady = steadystate kinetics(s, v, qt(T)) from s = 
       { C1 = 1; C2 = 0; C3 = 0; C4 = 0; C5 = 0; O = 0;
         I1 = 0; I2 = 0; I3 = 0; I4 = 0; I5 = 0; I6 = 0; };
         
    # OR
    # parameter steady = evolve_for 30ms kinetics(s, v, qt(T)) from s = 
    #    { C1 = 1; C2 = 0; C3 = 0; C4 = 0; C5 = 0; O = 0;
    #      I1 = 0; I2 = 0; I3 = 0; I4 = 0; I5 = 0; I6 = 0; };
         
    initial Nav_state = steady;
        
    evolve Nav_state' = kinetics(Nav_state, v, qt(T));

    effect current_density("na") = gbar*Nav_state.O*(v - ena);
    
    # Declare exports 
    export gbar, Con, Coff, Oon, Ooff;
    export a, b, g, d; 
    export a_f, b_f, avdep, bvdep;
    
}
```

## SK
```
mechanism density "SK" {
    parameter gbar = 10^-5 S/cm^2;
    parameter zTau = 1 ms;
    
    state SK_state: real;
    
    bind v = voltage;
    bind cai = internal concentration "ca";
    
    function zInf(v: voltage; c: concentration) {
        if c==0 then 0 else 1/(1 + (0.00043 mM/c)^4.8);
    }

    initial SK_state = zInf(v, cai);
    evolve SK_state' = (zInf(v, cai) - SK_state)/zTau;
    effect current_density("k") = gbar*SK_state*(v - ek);
    
    export gbar, zTau;
}
```


